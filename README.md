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
- 录制与回放 Done
- 后台界面查看 Done
- 根据域名进行过滤(在配置文件白名单中维护) Done
- 多种过滤方法(静态文件,请求方法,有返回的接口,MIME类型) Done
- 多线程请求 Done
- 接口黑名单(在配置文件白名单中维护) Done
- 接口去重 Done
- 结果进行return code 与 result字段的检查 Done
- 优化部分依赖路径+参数为区分的接口的显示与去重(在配置文件白名单中维护) Done
- 支持对多个文件进行回放测试 优先级高 Done

- anyproxy支持Mock 优先级中 TBD
- 接口覆盖率检查 优先级中 TBD（先让大数据帮忙看一下可行性）
- XSS跨域脚本攻击检查  优先级中 TBD
- Sqlmap 数据库注入扫描 优先级中 TBD （准备直接提供一个上传文件的页面，然后进行扫描判断，因为此功能只有新接口才会使用）
- fuzz 模糊测试 优先级低 TBD
- 动态参数（比如token）优先级低 TBD
- docker镜像化 优先级低 TBD

