import pymysql
import pandas as pd

host = "localhost"
id = "root"
pw = "root"
db_name = "quiz"

#connection 객체 생성
conn = pymysql.connect(host=host, user=id, password=pw, db=db_name, charset='utf8')

curs = conn.cursor()
#cursor 객체 생성
def attatch_score(name,score):
    sql = "INSERT INTO quiz(name, score) VALUES(" + "'" + name + "'," + str(score) +")"

    curs.execute(sql)
    conn.commit()


def search_score():
    curs.execute("select * from quiz")
    rows = curs.fetchall()
    database_name = []
    database_score = []
    for i in range(len(rows)):
        database_name.append(rows[i][0])
        database_score.append(rows[i][1])

    result_df = pd.DataFrame({"name":database_name, "score":database_score})

    rank = result_df['score'].rank(ascending=False)
    rank=rank.astype(int)

    result_df['rank']=rank

    result_df = result_df.sort_values(by=['rank'], axis=0)
    result_df = result_df.values.tolist()

    curs.close()

    return result_df