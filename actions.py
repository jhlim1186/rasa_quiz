from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

import quiz
import pandas as pd
import sql
import fuzzywuzzy

class ActionSearchScore(Action):

    def name(self) -> Text:
        return "Action_search_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = sql.search_score()
        dispatcher.utter_message(str(result[0][2]) + "위" + " " + result[0][0] + " " +str(result[0][1]) + "점\n" +
                                str(result[1][2]) + "위" + " " + result[1][0] + " " +str(result[1][1]) + "점\n" +
                                str(result[2][2]) + "위" + " " + result[2][0] + " " +str(result[2][1]) + "점\n" + 
                                str(result[3][2]) + "위" + " " + result[3][0] + " " +str(result[3][1]) + "점\n" + 
                                str(result[4][2]) + "위" + " " + result[4][0] + " " +str(result[4][1]) + "점")

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "Action_warning"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="그럼 지금부터 주의할점을 알려드리겠습니다.\n 1.모든 정답은 단답으로 말해주시길 바랍니다.\n 2.모든 정답은 띄어쓰기를 제외하고 말해주시길 바랍니다.\n 3.정답을 모르겠다면 모른다고 얘기해줘야 합니다. \n 4. 위의 주의사항을 지키지 않으면 오류가 생길 수 있으니 반드시 확인해주시고 문제를 풀어주시길 바랍니다. \n 그럼 화이팅!\n")
        return []

class Actionfindname(FormAction):

    def name(self) -> Text:
        return "Action_name"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        return ["name"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"name": self.from_entity(entity="name",
                                        intent="name")}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global score
        name_entity = tracker.get_slot("name")
        sql.attatch_score(name_entity,score)
        
        return [FollowupAction("Action_search_score")]

class ActionQuiz(Action):
    
    def name(self) -> Text:
        return "Action_Quiz"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global number
        global select_quiz
        global score
        score = 0 
        subject_entity = tracker.get_slot("subject") 
        select_quiz= pd.read_csv(subject_entity + '.csv', header=None, encoding="CP949")
        select_quiz = select_quiz.dropna()
        number = quiz.GetQuiz(select_quiz)
        dispatcher.utter_message("{}문제를 선택하셨습니다. \n 그럼 지금부터 퀴즈를 시작하겠습니다".format(subject_entity))

        return [FollowupAction("Action_problem")]

class ActionProblem(Action):

    def name(self) -> Text:
        return "Action_problem" 

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if(len(number)==0):
            dispatcher.utter_message("모든 문제를 완료하였습니다. \n 점수저장을 위해 이름을 입력해주세요")
            
            return [SlotSet("name","테스트"),FollowupAction("Action_name")]

        problem = quiz.Getproblem(number[0],select_quiz)
        dispatcher.utter_message(problem)

        return [FollowupAction("Action_answer")]
        

class ActionAnswer(FormAction):
    def name(self) -> Text:
        return "Action_answer"

    @staticmethod
    def required_slots(tracker:Tracker) -> List[Text]:
        return ["answer"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {"answer": self.from_entity(entity="answer",
                                        intent="answer")}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global score
        answer  = quiz.Getanswer(number[0],select_quiz)
        answer_entity = tracker.get_slot("answer")

        FollowupAction('actions_listen')

        if(answer == answer_entity):
            dispatcher.utter_message("정답입니다. 축하드려요!")
            score =+ 10

        else:
            dispatcher.utter_message("틀렸습니다.\n 문제의 정답은 {}입니다. 다음에 더 잘해봐요!".format(answer))

        del number[0]
   
        return [SlotSet("answer",None),FollowupAction("Action_problem")]

class Actions_wrong(Action):
    def name(self) -> Text:
        return "Action_wrong"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        answer  = quiz.Getanswer(number[0],select_quiz)

        dispatcher.utter_message("틀렸습니다.\n 문제의 정답은 {}입니다. 다음에 더 잘해봐요!".format(answer))

        del number[0]
   
        return [SlotSet("answer",None),FollowupAction("Action_problem")]