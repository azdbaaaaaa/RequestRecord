#! /usr/bin/env python
# -*- coding:utf-8 -*-
import utils
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


def main():
    l = [1, 2, 3]
    for x in xrange(1, len(l) + 1):
        print x


if __name__ == '__main__':
    main()
