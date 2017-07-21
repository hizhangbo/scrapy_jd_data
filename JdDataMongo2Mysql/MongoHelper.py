import pymongo

def get_db():  
    # 建立连接  
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)  
    db = client['jd_data']  
    #或者 db = client.example  
    return db 

def get_collection(db):  
    # 选择集合（mongo中collection和database都是延时创建的）  
    coll = db['comment']  
    # print(db.collection_names())
    return coll

def insert_one_doc(db):  
    # 插入一个document  
    # coll = db['comment']  
    # obj = {"name": "", "age": ""}  
    # _id = coll.insert(obj)  
    # print(_id)
    pass

def insert_multi_docs(db):  
    # 批量插入documents,插入一个数组  
    # coll = db['comment']  
    # obj = [{"name": "", "age": ""}, {"name": "", "age": ""}]  
    # _id = coll.insert(obj)  
    # print(_id)
    pass

def get_many_docs(db):  
    # mongo中提供了过滤查找的方法，可以通过各种条件筛选来获取数据集，还可以对数据进行计数，排序等处理  
    coll = db['comment']
    result = []
    #ASCENDING = 1 升序;DESCENDING = -1降序;default is ASCENDING  (find().sort("age", pymongo.DESCENDING))
    for item in coll.find({}, {'_id':0}):  
        result.append(item)
    return result
    # count = coll.count()
    # print("集合中所有数据 {}个".format(int(count)))
   
    #条件查询  
    # count = coll.find({"name":["诸神的微笑"]}).count()  
    # print("诸神的微笑: {}".format(int(count)))
