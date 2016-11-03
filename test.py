#! /usr/bin/env python
# -*- coding:utf-8 -*-

import threading
from time import ctime,sleep

def do_request(line):
	print "I was requesting%s. %s" % (line,ctime())
	sleep(5)

threads = []
with open("test.txt", "r") as file:
# for x in xrange(0,3):
    line = file.readlines()
    # line = filter(filter_by_host_mmbang, line)
    # # line = filter(filter_by_host, line)
    # line = filter(filter_by_method, line)
    # line = filter(filter_by_duration, line)

    t = threading.Thread(target=do_request,args=(line,))
    threads.append(t)


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

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print "all over %s" %ctime()