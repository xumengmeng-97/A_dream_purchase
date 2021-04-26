Description : 如梦之梦话剧自动买票，仅限于保利剧院
Author : Mengmeng Xu
Time : 2021/04/23
Prepare : Chrome, ChromeDriver
Environment : pip install -r xxx
astroid==2.3.3
isort==4.3.21
lazy-object-proxy==1.4.3
mccabe==0.6.1
pylint==2.4.4
selenium==3.141.0
six==1.14.0
typed-ast==1.4.1
urllib3==1.25.8
wrapt==1.11.2

config说明:
'sess' : 0 , google chrome
'price' : 0-6 , 0,红色，　1，黄色，　2，浅绿色，　3，深绿色，　4，浅蓝色，　5，深蓝色
'date' : 0-3, 0,第一天，　1，第二天，　2，第三天，　3，第四天
'real_name' : 'xxx', your name
'tel' : 'xxx', # your telephone number,
'id_name' : 0-2, 0,第一个人，　1，第二个人，　2，第三个人
'ticket_position' : 3, the position of ticket
'baoli_url' : "https://m.polyt.cn/login?redirect=%2Fmine"
'target_url' : "https://m.polyt.cn/detail/50/27847/560791811588227072"
'browser': 0 , google chrome

【重要，用前必看！！！】
搭建python3+pip环境，可使用anaconda、pycharm等集成环境（https://www.runoob.com/w3cnote/pycharm-windows-install.html）
或纯python环境 （Windows下的环境搭建流程可参考https://www.jianshu.com/p/2f1acc6ff2c6）
chromedriver和chrome匹配，参考https://blog.csdn.net/BinGISer/article/details/88559532
最后成功测试运行时间：2021-04-23。
使用前请将待抢票者的姓名、手机、地址设为默认，如存在多名实名者，请提前保存相关信息。
此方法太过于依赖网页面源码的元素的title、Xpath、class name、tag name等，若相应的绝对路径寻找不到则代码无法运行。
具体定位方案请参见https://github.com/Entromorgan/Autoticket/wiki/%E5%AE%9A%E4%BD%8D%E6%96%B9%E5%BC%8F

买票流程：
1，　安装python和pycharm，根据环境需求配置相应的环境
2，　安装google chrome和chromedriver
3，　运行cookies_save.py，输入帐号和验证码，保存cookies
4，　配置config.json文件，根据自己的需求
5，　运行Autoticket.py文件
6，　手动付款
7，　买票完成
