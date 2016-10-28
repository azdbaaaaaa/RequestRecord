#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import codecs
import re


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


def request_template(method, url, **kwargs):
    print kwargs
    if method.lower() == "get":
        r_get = requests.get(url=url, **kwargs)
        print r_get.url
        print r_get.status_code
        assert r_get.status_code < 400
    if method.lower() == "post":
        r_post = requests.post(url=url, **kwargs)
        print r_get.status_code
        assert r_post.status_code < 400


file_path = "6.txt"
read_file(file_path)

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
