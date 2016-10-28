#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import codecs
import re
import json


def request_template(method, url, **kwargs):
    # print kwargs
    try:
        if method.lower() == "get":
            r_get = requests.get(url=url, **kwargs)
            if r_get.status_code < 400:
                if r_get.headers:
                    if "application/json" in r_get.headers["Content-Type"]:
                        if json.loads(r_get.text)["success"] is True:
                            print "ok"
            print r_get.url
            print r_get.status_code
            assert r_get.status_code < 400
        if method.lower() == "post":
            r_post = requests.post(url=url, **kwargs)
            print r_post.url
            print r_post.text
            print r_post.status_code
            assert r_post.status_code < 400
    except Exception as e:
        print(e)
        return False


def filter_by_host(req):  # 过滤出请求头中host字段包含mmbang的请求
    try:
        fliter_string = "mmbang"
        r = json.loads(req)
        if fliter_string in r["reqHeader"]["host"]:
            return req
    except Exception as e:
        print(e)
        return False


def filter_by_method(req):  # 过滤出请求方法是get或者post的请求
    try:
        fliter_tuple = ("get", "post")
        r = json.loads(req)
        if r["method"].lower() in fliter_tuple:
            return req
    except Exception as e:
        print(e)
        return False


def filter_by_duration(req):  # 过滤出有返回的请求
    try:
        r = json.loads(req)
        if isinstance(r["duration"], int):
            return req
    except Exception as e:
        print(e)
        return False


def dealwithdata(record):
    pass


with open("demo1.log", "r") as file:
    line = file.readlines()
    line = filter(filter_by_host, line)
    line = filter(filter_by_method, line)
    line = filter(filter_by_duration, line)
    # print len(line)
    for x in xrange(0, len(line)):
        record = json.loads(line[x])
        result = request_template(
            record["method"],
            record["url"],
            headers=record["reqHeader"],
            data=record["reqBody"],
            verify=False
        )
        print("*" * 20)


def filter_null(c):
    if not re.match('[\\x00\\xff\\xfe]', c):
        return True


def unicode2utf8(input_file, output_file):
    with open(output_file, 'w') as save:
        with open(input_file, 'rb') as f:
            for line in open(input_file):
                line = f.readline()
                line = filter(filter_null, line)
                line = line[:-1]  # 去掉多余的换行符
                line = line.encode('utf-8')
                # print line
                save.writelines(line)
    with open(output_file, 'r') as f_utf8:
        print f_utf8.read()


# unicode2utf8("3.txt", "6.txt")


def read_file(file):
    '''
    adsddsa
    '''
    with codecs.open(file, 'r', 'utf-8') as file:
        line = file.readlines()
        if(line):
            print line[3]





# file_path = "demo1.log"
# read_file(file_path)

# for x in xrange(0, 3):
#     method = "get"
#     url = "http://www.baidu.com"
#     request_template(method, url, params={"a": 1}, headers={}, files={})


# def setup_func():
#     "set up test fixtures"


# def teardown_func():
#     "tear down test fixtures"


# @with_setup(setup_func, teardown_func)
# def test():
#     "test ..."
