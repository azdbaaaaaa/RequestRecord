#! /usr/bin/env python
# -*- coding:utf-8 -*-

# 获取当前脚本路径
# import sys
# import os
# print os.path.dirname(sys.argv[0])

# # 参数argparse
# import argparse
# parser = argparse.ArgumentParser(description='reply the API requests.')
# parser.add_argument('-i', '--input', nargs='+', required=True,
#                     help='a list of the inputfiles.(Required)')
# parser.add_argument('--host', nargs='+',
#                     help='a list of the host.(Default read from config.py)')
# args = parser.parse_args()
# print args.host
# # print args.host
# # print args.test


# # 合并多个文件
# def merge_files(outputfile, *inputfiles):
#     with open(outputfile, 'w') as fo:
#         for name in inputfiles:
#             with open(name) as fi:
#                 while True:
#                     s = fi.read(16 * 1024)
#                     if not s:
#                         break
#                     fo.write(s)
# merge_files("all-2.txt", "all.txt", "1.txt", "2.txt")


# import urlparse
# import json
# white_list_duplicate = {
#     "mobile.mmbang.com/api18/": "do"
# }
# fullurl = "mobile.mmbang.com/api18/"
# a = {'do': ['hello'], 'b': ['world ']}
# api_list = []
# list01 = [
#     {"url": "http://mobile.mmbang.com/api18/?a=1&do=user"},
#     {"url": "http://mobile.mmbang.com/api18/?a=2"},
#     {"url": "http://mobile.mmbang.com/api17/?a=2"},
# ]


# def filter_by_duplicated(r):
#     '''过滤出所有非重复的请求
#     '''
#     try:
#         # r = json.loads(req)
#         url = r["url"]
#         parsed_url = urlparse.urlparse(url)
#         host = parsed_url.netloc
#         path = parsed_url.path
#         fullurl = host + path
#         params = urlparse.parse_qs(parsed_url.query, True)
#         for x in white_list_duplicate:
#             if fullurl == x and white_list_duplicate[x] in params:
#                 fullurl = fullurl + white_list_duplicate[x] + "=" + params[white_list_duplicate[x]][0]
#         if fullurl not in api_list:
#             api_list.append(fullurl)
#             return True
#         return False
#     except Exception as e:
#         print(e)
#         return False

# list01 = filter(filter_by_duplicated, list01)
# print list01
# print api_list

# list01 = [
#     {"url": "http://mobile.mmbang.com/api18/?a=1"},
#     {"url": "http://mobile.mmbang.com/api18/?a=2"},
#     {"url": "http://mobile.mmbang.com/api17/?a=2"},
# ]

# api_list = []


# def filter_by_duplicated(r):
#     try:
#         # r = json.loads(req)
#         url = r["url"]
#         parsed_url = urlparse.urlparse(url)
#         host = parsed_url.netloc
#         path = parsed_url.path
#         fullurl = host + path
#         if fullurl not in api_list:
#             api_list.append(fullurl)
#             return True
#         return False
#     except Exception as e:
#         print(e)
#         return False

# list01 = filter(filter_by_duplicated, list01)
# print list01
# import utils
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


# def count(collection_name, query_data):
#     try:
#         from pymongo import MongoClient
#         client = MongoClient()
#         db = client.data
#         print db.get_collection(collection_name)
#         print dir(db)
#         result = db.get_collection(dbname).find(query_data).count()
#         return result
#     except Exception as e:
#         print(e)
#         return False

# L = ['adam', 'LISA', 'barT']


# def normalize(name):
#     a = name.lower()
#     a = list(a)
#     a[0] = a[0].upper()
#     return ''.join(a)


# # print map(normalize, L)


# from functools import reduce


# def generator_num():
#     for x in xrange(1, 101):
#         yield x
#         x += 1


# def add(x, y):
#     return x + y


# print reduce(lambda x, y: x + y, generator_num())

    # print L[x]
# print L1
# if __name__ == '__main__':
#     print count("users", {})

# def generator_num():
#     n = 1
#     while n < 1000:
#         n += 1
#         yield n


# def filter_by(n):
#     if n < 10:
#         return False
#     s = str(n)
#     li = list(s)
#     li.reverse()
#     k = ""
#     res = int(k.join(li))
#     if res == n:
#         return True
#     else:
#         return False


# def is_palindrome():
#     it = generator_num()
#     it = filter(filter_by, it)
#     for x in it:
#         print x

# is_palindrome()


# for x in generator_num():
#     print x
