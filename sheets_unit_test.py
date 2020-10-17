from pprint import pprint
import sheets

data = sheets.getQuestionRound(3)

pprint(data)

#pprint(data.answers)

pprint("************** Image *******************")

pprint(data["image"])

pprint("************** Answers *******************")

pprint(data["answers"])

pprint("************** Answers A *******************")

pprint(data["answers"]["a"][0])

pprint("************** Answers true or false? *******************")
pprint(data["answers"]["a"][1])

pprint("************** All topics *******************")
data = sheets.getTopics()
pprint(data)

pprint("************** All rows of NLP topic *******************")
pprint("The topic NLP is in following rows")
data = sheets.getTopicRows("NLP")
pprint(data)

pprint("************** All rows *******************")
pprint("These are all rows")
data = sheets.getAllRows()
pprint(data)

pprint("************** Random row *******************")
pprint("The random row is " + str(sheets.getRandomRow()) )