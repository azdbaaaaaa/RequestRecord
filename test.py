#! /usr/bin/env python
# -*- coding:utf-8 -*-
import utils
# def music(func):
#     for i in range(2):
#         print "I was listening to %s. %s" %(func,ctime())
#         sleep(1)

# def move(func):
#     for i in range(2):
#         print "I was at the %s! %s" %(func,ctime())
#         sleep(5)

# threads = []
# t1 = threading.Thread(target=music,args=(u'爱情买卖',))
# threads.append(t1)
# t2 = threading.Thread(target=move,args=(u'阿凡达',))
# threads.append(t2)


def count(collection_name, query_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        print db.get_collection(collection_name)
        print dir(db)
        result = db.get_collection(dbname).find(query_data).count()
        return result
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    print count("users", {})
