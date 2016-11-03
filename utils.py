#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json


def queryOne_db(query_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.anyproxy
        result = db.record.find_one(query_data)
        return result
    except Exception as e:
        print(e)
        return False


def queryMany_db(query_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.anyproxy
        cursor = db.record.find(query_data)
        result = []
        for x in cursor:
            result.append(x)
        return result
    except Exception as e:
        print(e)
        return False


def insertOne_db(insert_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.anyproxy
        result = db.record.insert_one(insert_data)
        return result.inserted_id
    except Exception as e:
        print(e)
        return False


def updateOne_db(query_data, update_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.anyproxy
        result = db.record.update_one(query_data, update_data)
        if result.modified_count > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def assert400(status_code):
    if status_code < 400:
        return {"result": "Pass", "desc": "return code is between 200-400"}
    return {"result": "Fail", "desc": "return code is over 400"}


def assertSuccess(response):
    try:
        if isinstance(response, dict):
            status_code = response["statusCode"]
            if response["resHeader"].has_key("Content-Type"):
                mime_type = response["resHeader"]["Content-Type"]
            else:
                mime_type = "unknown"
            text = response["resBody"]
            assert_result = assert400(status_code)
            if assert_result["result"] is "Fail":
                return assert_result
            if "application/json" in mime_type:
                if json.loads(text).has_key("success"):
                    if json.loads(text)["success"] is True:
                        return {"result": "Pass",
                                "desc": "mime is json & success is true"}
            return {
                "result": "Pass",
                "desc": "return code is lt 400 and mime isnt json"
            }
        return {"result": "Fail",
                "desc": response}
    except Exception as e:
        print(e)
        return {"result": "Exception",
                "desc": "Exception:%s" % e}
