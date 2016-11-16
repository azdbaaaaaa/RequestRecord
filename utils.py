#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json


def merge_files(outputfile, inputfiles):
    with open(outputfile, 'w') as fo:
        for name in inputfiles:
            with open(name) as fi:
                while True:
                    s = fi.read(16 * 1024)
                    if not s:
                        break
                    fo.write(s)


def findMaxId(collection_name):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        cursor = (db.get_collection(collection_name)
                    .find({}, {"Iter": 1, "_id": 0})
                    .sort([("Iter", -1)])
                    .limit(1))
        for x in cursor:
            return x["Iter"]
    except Exception as e:
        print(e)
        return False


def queryOne_db(collection_name, query_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        result = db.get_collection(collection_name).find_one(query_data)
        return result
    except Exception as e:
        print(e)
        return False


def queryMany_db(collection_name, query_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        cursor = db.get_collection(collection_name).find(query_data)
        result = []
        for x in cursor:
            result.append(x)
        return result
    except Exception as e:
        print(e)
        return False


def count_db(collection_name, query_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        result = db.get_collection(collection_name).find(query_data).count()
        # result = []
        # for x in cursor:
        #     result.append(x)
        return result
    except Exception as e:
        print(e)
        return False


def insertOne_db(collection_name, insert_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        result = db.get_collection(collection_name).insert_one(insert_data)
        return result.inserted_id
    except Exception as e:
        print(e)
        return False


def updateOne_db(collection_name, query_data, update_data):
    try:
        from pymongo import MongoClient
        client = MongoClient()
        db = client.data
        result = (db.get_collection(collection_name)
                    .update_one(query_data, update_data))
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
            if "Content-Type" in response["resHeader"]:
                mime_type = response["resHeader"]["Content-Type"]
            else:
                mime_type = "unknown"
            text = response["resBody"]
            assert_result = assert400(status_code)
            if assert_result["result"] is "Fail":
                return assert_result
            if "application/json" in mime_type:
                if "success" in json.loads(text):
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
