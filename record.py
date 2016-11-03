#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import time
import utils
import urlparse
import getopt
import sys
import config
import threading
from time import sleep


def Usage():
    print 'repeat.py usage:'
    print '-h, --help: print help message.'
    print '-v, --version: print script version'
    print '-i, --inputfile [value]: (required) inputfile file recorded by anyproxy.'
    print '-t, --host [value]: (optional) a list of host separated by | , which need to be repeat. \
if null, read config.py ex: --host "mobile.mmbang.com|www.mmbang.com"'


def Version():
    print 'repeat.py 0.0.1'


def filter_by_host_mmbang(req): # 过滤出请求头中host字段包含mmbang的请求
    try:
        r = json.loads(req)
        if "mmbang" in r["reqHeader"]["host"]:
            return req
    except Exception as e:
        print(e)
        return False


def filter_by_host(req):  # 过滤出指定域名的请求，如果没有指定的话读取config文件
    try:
        if 'filter_host' in globals().keys(): # 判断是否传入全局变量filter_host
            filter_host_list = filter_host.split("|") # 读取传入的filter_host转化为filter_host_list
        else:
            filter_host_list = config.filter_host_list # 读取config.py中的filter_host_list
        r = json.loads(req)
        if r["reqHeader"]["host"] in filter_host_list:
            return req
    except Exception as e:
        print(e)
        return False


def filter_by_method(req):  # 过滤出请求方法是get或者post的请求
    try:
        filter_tuple = ("get", "post")
        r = json.loads(req)
        if r["method"].lower() in filter_tuple:
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


def request_template(method, url, headers, **kwargs):
    '''
    '''
    # print kwargs
    try:
        parsed_url = urlparse.urlparse(url)
        protocol = parsed_url.scheme
        host = parsed_url.netloc
        path = parsed_url.path
        params = parsed_url.params
        query = parsed_url.query
        reqBody = kwargs["data"]
        # request
        if method.lower() == "get":
            res = requests.get(url=url, headers=headers, **kwargs)
        if method.lower() == "post":
            res = requests.post(url=url, headers=headers, **kwargs)

        result = {
            "url": url,
            "protocol": protocol,
            "host": host,
            "path": path,
            "params": params,
            "query": query,
            "method": method,
            "reqHeader": headers,
            "reqBody": reqBody,
            "statusCode": res.status_code,
            "duration": res.elapsed.microseconds,
            "resHeader": res.headers,
            "resBody": res.text,
            "length": len(res.content),
            "encoding": res.encoding,
            # "raw": res.raw,
            "reason": res.reason
        }
        return result
        # # assert
        # if res.status_code >= 400:
        #     return utils.assertFail("response code is over 400")
        # if res.headers and ("json" in res.headers["Content-Type"]):
        #     if json.loads(res.text)["success"] is not True:
        #         return utils.assertFail("response json fail")
    except Exception as e:
        print(e)
        return "exception: %s" % e


def do_request(request):
    try:
        record = json.loads(request)

        # 请求之前写入原始数据并返回数据id
        id = utils.insertOne_db({
            "Iter": 1,
            "origin": record,
            "created": time.time()
        })

        # 开始请求
        response = request_template(
            record["method"],
            record["url"],
            record["reqHeader"],
            data=record["reqBody"],
            verify=False,
            timeout=30
        )

        # 请求之后根据之前的数据id写入请求的数据
        utils.updateOne_db(
            {"_id": id},
            {"$set": {"requests": response, "updated": time.time()}}
        )
        # 断言 并写入数据库
        utils.updateOne_db(
            {"_id": id},
            {"$set": utils.assertSuccess(
                utils.queryOne_db({"_id": id})["requests"]
            )}
        )
        sleep(5)
        print("*" * 6 + "%s" + "*" * 6 + "%s" + "*" * 6) % (id,time.ctime())
        return True
    except Exception as e:
        print(e)
        return False


def generateReport():
    pass


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            "hvi:t:",
            ["help", "version", "inputfile=", "host="]
        )
    except getopt.GetoptError:
        Usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            Usage()
            sys.exit(0)
        elif opt in ("-v", "--version"):
            Version()
            sys.exit(0)
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-t", "--host"):
            global filter_host
            filter_host = arg
        else:
            Usage()
            sys.exit(3)
    if 'inputfile' not in locals().keys():
        Usage()
        sys.exit(4)

    with open(inputfile, "r") as file:
        lines = file.readlines()
        lines = filter(filter_by_host_mmbang, lines)
        # line = filter(filter_by_host, line)
        lines = filter(filter_by_method, lines)
        lines = filter(filter_by_duration, lines)
        # 多线程处理请求
        threads = []
        for x in xrange(0, len(lines)):
            t = threading.Thread(target=do_request,args=(lines[x],))
            threads.append(t)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

        # 单线程处理请求
        # for x in xrange(0, len(lines)):
        #     print lines[x]
        #     do_request(lines[x])
    generateReport()


if __name__ == '__main__':
    #The start time 
    start = time.clock()
    #A program which will run for 3 seconds
    main(sys.argv)
    #The End time 
    end = time.clock()
    print("The function run time is : %.03f seconds" %(end-start))
