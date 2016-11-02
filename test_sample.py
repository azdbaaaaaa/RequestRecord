#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import time
import utils
import urlparse


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


def request_template(method, url, headers, **kwargs):
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
            "url": res.url,
            "protocol": protocol,
            "host": host,
            "path": path,
            "params": params,
            "query": query,
            "method": method,
            "reqHeader": res.request.headers,
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
        return False


def do_request(l):
    try:
        for x in xrange(0, len(l)):
            record = json.loads(l[x])

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
            print("*" * 20)
        return True
    except Exception as e:
        print(e)
        return False


def generateReport():
    pass


with open("demo1.log", "r") as file:
    line = file.readlines()
    line = filter(filter_by_host, line)
    line = filter(filter_by_method, line)
    line = filter(filter_by_duration, line)
    do_request(line)
generateReport()
