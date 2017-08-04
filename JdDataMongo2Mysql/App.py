import MongoHelper
import MysqlHelper
import json
import re
from Jd import Jd

from pymysql.err import ProgrammingError
from json.decoder import JSONDecodeError

_db = MongoHelper.get_db()
_collection = MongoHelper.get_collection(_db)
result = MongoHelper.get_many_docs(_db)

for item in result:
    comments = item['comments']
    if comments.find('fetch(') != -1:
        comments = comments.replace("'", "\"") # python 中 json 键名必须用双引号        
        comments = re.sub(r'"content":"([\s\S]*?)<div([\s\S]*?)</div>",', r'"content":"\1",', comments) # (用户评价图片)去除 content 中存在字符干扰json序列化
        comments = comments.replace('<body>fetch(','').replace(');</body>','') # (json头尾)去除 content 中存在字符干扰json序列化
        try:
            obj = json.loads(comments)
        except JSONDecodeError:
            output = open('error.txt', 'a', encoding='utf-8')
            output.writelines('未序列化成功:{}'.format(comments))
            output.close()
            continue        

        for comment in obj['comments']:
            tmp = Jd()
            try:
                tmp.good_id = comment['referenceId']
                tmp.good_name = "".join(item['name'])
                tmp.price = item['price']
                tmp.img = item['img']
                tmp.commit = item['commit']
                tmp.user = comment['nickname']
                tmp.comment = comment['content']
                tmp.url = 'https://club.jd.com/repay/{good_id}_{gguid}_1.html'.format(good_id = comment['referenceId'], gguid = comment['guid'])
                tmp.userlevel = comment['userLevelName']
                tmp.device = comment['userClientShow']
                tmp.kind = comment['productColor']
                tmp.createtime = comment['creationTime']
                tmp.score = comment['score']
                tmp.guid = comment['guid']
                tmp.isbn = item['isbn']

                if 'commentTags'in comment:
                    for tag in comment['commentTags']:            
                        tmp.tag.append('{},'.format(tag['name']))
            except KeyError as e:
                output = open('error.txt', 'a', encoding='utf-8')
                output.writelines('字段读取失败:{}'.format("{}-{}-{}-{}-{}".format(tmp.user, tmp.good_name, tmp.comment, tmp.url, e)))
                output.close()
                continue

            print("{}-{}-{}-{}-{}".format(tmp.user, tmp.good_name, tmp.comment, tmp.url, tmp.isbn))
            try:
                if MysqlHelper.exists(tmp):
                    continue
                else:
                    MysqlHelper.insert(tmp)
            except ProgrammingError:
                output = open('error.txt', 'a', encoding='utf-8')
                output.writelines('写入数据库失败:{}'.format("{}-{}-{}-{}".format(tmp.user, tmp.good_name, tmp.comment, tmp.url)))
                output.close()
                continue
            


