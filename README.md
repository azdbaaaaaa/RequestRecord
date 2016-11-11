# RequestRecord

## Usage():
~~~
    print 'repeat.py usage:'
    print '-h, --help: print help message.'
    print '-v, --version: print script version'
    print '-i, --inputfile: (required) inputfile file recorded by anyproxy.'
    print '-t, --host: (optional) a list of host separated by | , which need to be repeat\
    							if null, read config.py\
                      ex: --host "mobile.mmbang.com|www.mmbang.com"'
~~~

## TodoList:
- XSS跨域脚本攻击检查  优先级中
- Sqlmap 数据库注入扫描 优先级高
- fuzz 模糊测试 优先级低
- 接口覆盖率检查 优先级中
- 动态参数（比如token）优先级低
- anyproxy支持Mock 优先级低
- docker镜像化 优先级低
- 接口白名单 优先级高
