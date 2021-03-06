#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import time
import utils
import urlparse
import sys
import config
import threading
import argparse

# 记录需要请求的路径列表，用来去重过滤
api_list = []


def filter_by_duplicated(req):
    '''过滤出所有非重复的请求
    '''
    try:
        r = json.loads(req)
        url = r["url"]
        parsed_url = urlparse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        fullurl = host + path
        params = urlparse.parse_qs(parsed_url.query, True)
        wl = config.white_list_duplicate
        for x in wl:
            if fullurl == x and wl[x] in params:
                fullurl = fullurl + "?" + wl[x] + "=" + params[wl[x]][0]
        if fullurl not in api_list:
            api_list.append(fullurl)
            return True
        return False
    except Exception as e:
        print(e)
        return False


def filter_by_black_list(req):  # 过滤黑名单中的接口请求
    try:
        r = json.loads(req)
        url = r["url"]
        parsed_url = urlparse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        fullurl = host + path
        # print fullurl
        if fullurl in config.black_list:
            return False
        return True
    except Exception as e:
        print(e)
        return False


def filter_by_mime(req):  # 过滤出所有json格式的请求
    try:
        r = json.loads(req)
        if "mime" in r:
            if "application/json" in r["mime"]:
                return req
        elif "resHeader" in r:
            if "application/json" in r["resHeader"]["content-type"]:
                return req
    except Exception as e:
        print(e)
        return False


def filter_by_static_file(req):  # 过滤出所有静态文件的请求
    try:
        filter_tuple = (".js", ".css", ".jpg", ".jpeg", ".png", ".gif")
        r = json.loads(req)
        for x in xrange(0, len(filter_tuple)):
            if r["path"].endswith(filter_tuple[x]):
                return False
        # print r["path"]
        return req
    except Exception as e:
        print(e)
        return False


def filter_by_host_mmbang(req):  # 过滤出请求头中host字段包含mmbang的请求
    try:
        r = json.loads(req)
        if "mmbang" in r["reqHeader"]["host"]:
            return req
    except Exception as e:
        print(e)
        return False


def filter_by_host(req):  # 过滤出指定域名的请求，如果没有指定的话读取config文件
    try:
        # 判断filter_host_list是否存在，不存在读取config.py
        filter_host_list = config.filter_host_list
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


def do_request(request, Iter, id):
    try:
        record = json.loads(request)
        # 请求之前写入原始数据并返回数据id
        id = utils.insertOne_db("apireplyrecords", {
            "Iter": Iter,
            "origin": record,
            "created": time.time(),
            "id": id
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

        # 针对白名单中的接口进行response的url替换
        parsed_url = urlparse.urlparse(response["url"])
        host = parsed_url.netloc
        path = parsed_url.path
        fullurl = host + path
        params = urlparse.parse_qs(parsed_url.query, True)
        wl = config.white_list_duplicate
        for x in wl:
            if fullurl == x and wl[x] in params:
                response["path"] = path + "?" + wl[x] + "=" + params[wl[x]][0]

        # 请求之后根据之前的数据id写入请求的数据
        utils.updateOne_db(
            "apireplyrecords",
            {"_id": id},
            {"$set": {"requests": response, "updated": time.time()}}
        )
        # 断言 并写入数据库
        utils.updateOne_db(
            "apireplyrecords",
            {"_id": id},
            {"$set": utils.assertSuccess(
                utils.queryOne_db("apireplyrecords", {"_id": id})["requests"]
            )}
        )
        # print("***%s***%s***\n") % (id, time.ctime())
        return True
    except Exception as e:
        print(e)
        return False


def main(argv):
    # The start time
    global start
    start = time.time()

    parser = argparse.ArgumentParser(description='reply the API requests.')
    parser.add_argument('-i', '--input', nargs='+', required=True,
                        help='list of the inputfiles. (Required)')
    # parser.add_argument('--host', nargs='+',
    #                     help='list of the host. (Default read config.py)')
    args = parser.parse_args()
    inputfiles = args.input

    # 判断文件数量是否为1个，如果多于1个的话，先进行合并文件，生产temp，然后再进行请求
    if len(inputfiles) > 1:
        tempfile = str(time.time()).split('.')[0] + "_temp.log"
        utils.merge_files(tempfile, inputfiles)
    else:
        tempfile = inputfiles[0]
    with open(tempfile, "r") as file:
        lines = file.readlines()
        # lines = lines[0]
        # lines = filter(filter_by_host_mmbang, lines)
        lines = filter(filter_by_host, lines)  # 过滤出指定域名的请求，如果没有指定的话读取config文件
        lines = filter(filter_by_static_file, lines)  # 过滤出所有非静态文件的请求
        lines = filter(filter_by_method, lines)  # 过滤出所有GET与POST请求
        lines = filter(filter_by_duration, lines)  # 过滤出所有有返回时间的请求
        lines = filter(filter_by_mime, lines)  # 过滤出所有MIME类型是json的请求
        lines = filter(filter_by_black_list, lines)  # 过滤出所有不是黑名单中接口地址的请求
        lines = filter(filter_by_duplicated, lines)  # 过滤出所有非重复的请求
        # sys.exit(1)
        # 获取当前是第几次测试
        currentIter = utils.findMaxId("apireplysummarys")
        if not currentIter:
            Iter = 1
        else:
            Iter = currentIter + 1
        # 多线程处理请求
        threads = []
        for x in xrange(0, len(lines)):
            t = threading.Thread(
                target=do_request,
                args=(lines[x], Iter, x + 1,)
            )
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
    # The End time
    global end
    end = time.time()
    utils.insertOne_db(
        "apireplysummarys",
        {
            "Iter": Iter,
            "start": start,
            "end": end,
            "totalCount": utils.count_db("apireplyrecords", {"Iter": Iter}),
            "passCount": utils.count_db("apireplyrecords", {
                "Iter": Iter,
                "result": "Pass"}),
            "failCount": utils.count_db("apireplyrecords", {
                "Iter": Iter,
                "result": "Fail"}),
            "exceptionCount": utils.count_db("apireplyrecords", {
                "Iter": Iter,
                "result": "Exception"}),
        }
    )
    # generateReport()


if __name__ == '__main__':
    # The start time
    startTime = time.clock()
    # main program
    main(sys.argv)
    # The End time
    endTime = time.clock()
    print("The function run time is : %.03f seconds" % (endTime - startTime))
