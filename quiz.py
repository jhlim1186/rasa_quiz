import pandas as pd
import numpy as np
import random as rd

## quiz_num : index 번호를 list 형태로 출력
def GetQuiz(quiz):
    problem_total_num = range(0,len(quiz.index))
    quiz_num = rd.sample(problem_total_num,1)
    
    return quiz_num

## problems : quiz_num 인덱스 번호에 따른 문제 출력
def Getproblem(quiz_num,quiz):
    problems = str(quiz.iloc[quiz_num][0])
        
    return problems

## answer : quiz_num 인덱스 번호에 따른 정답 출력
def Getanswer(quiz_num,quiz):
    answer = str(quiz.iloc[quiz_num][1])
    
    return answer

def db_name():
    df_name = pd.read_csv('이름.csv',encoding='CP949',header=None)
    name_list = np.array(df_name[0].tolist())

    return name_list