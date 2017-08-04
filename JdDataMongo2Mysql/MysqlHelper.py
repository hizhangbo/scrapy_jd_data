import pymysql
from Jd import Jd

def insert(comment):
    conn=pymysql.connect(host='ip',port=3306,user='root',passwd='91test.com',db='jd_data',charset='utf8')
    cur=conn.cursor()
    cur.execute("insert into comment(good_id,good_name,price,commit,img,tag,user,comment,url,userlevel,device,kind,createtime,score,guid,isbn) " 
            + "values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}')"
            .format(comment.good_id, comment.good_name, comment.price, comment.commit, comment.img, ','.join(comment.tag),
            comment.user, comment.comment, comment.url, comment.userlevel, comment.device, comment.kind, comment.createtime, comment.score, comment.guid, comment.isbn))

    conn.commit()
    cur.close()
    conn.close()

def exists(comment):
    conn=pymysql.connect(host='ip',port=3306,user='root',passwd='91test.com',db='jd_data',charset='utf8')

    cur=conn.cursor()
    effect_row = cur.execute("select * from comment where guid = '{}' and good_id = '{}'".format(comment.guid, comment.good_id))
    if effect_row > 0:
        return True
    else:
        return False

