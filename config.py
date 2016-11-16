#! /usr/bin/env python
# -*- coding:utf-8 -*-

filter_host_list = [
    "mobile.mmbang.com",
    "go.mmbang.com"
]

#  黑名单--此名单中的接口不会请求
black_list = [
    "mobile.mmbang.com/api10/",
    "mobile.mmbang.com/api11/"
]

#  白名单--通过路径以及参数区分的接口重定义接口地址（作用于过滤以及请求后的接口路径显示）
white_list_duplicate = {
    "mobile.mmbang.com/api18/": "do"
}
