#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests


def func(x):
    '''
    adsddsa
    '''
    return x + 1


def test_request():
    url = "http://www.mmbang.com"
    data = {}
    headers = {}
    files = {}
    r_get = requests.get(url=url, headers=headers, files=files)
    # r_post = requests.post(url=url, data=data, headers=headers, files=files)
    assert r_get.status_code < 400


def setup_func():
    "set up test fixtures"


def teardown_func():
    "tear down test fixtures"


# @with_setup(setup_func, teardown_func)
# def test():
#     "test ..."
