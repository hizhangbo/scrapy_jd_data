import MySQLdb
from Jd import Jd

def insert(comment):
    conn=MySQLdb.connect(host='ip',port=3306,user='root',passwd='pwd',db='jd_data',charset='utf8')
    cur=conn.cursor()
    cur.execute("insert into comment(good_id,good_name,price,commit,img,tag,user,comment,url,userlevel,device,kind,createtime) " 
            + "values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')"
            .format(comment.good_id, comment.good_name, comment.price, comment.commit, comment.img, ''.join(comment.tag),
            comment.user, comment.comment, comment.url, comment.userlevel, comment.device, comment.kind, comment.createtime, comment.score))
    conn.commit()
    cur.close()
    conn.close()
