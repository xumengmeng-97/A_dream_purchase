【重要，用前必看！！！】
搭建python3+pip环境，可使用anaconda、pycharm等集成环境（https://www.runoob.com/w3cnote/pycharm-windows-install.html）
或纯python环境 （Windows下的环境搭建流程可参考https://www.jianshu.com/p/2f1acc6ff2c6）
chromedriver和chrome匹配，参考https://blog.csdn.net/BinGISer/article/details/88559532
最后成功测试运行时间：2021-04-23。
使用前请将待抢票者的姓名、手机、地址设为默认，如存在多名实名者，请提前保存相关信息。
此方法太过于依赖大麦网页面源码的元素的title、Xpath、class name、tag name等，若相应的绝对路径寻找不到则代码无法运行。
具体定位方案请参见https://github.com/Entromorgan/Autoticket/wiki/%E5%AE%9A%E4%BD%8D%E6%96%B9%E5%BC%8F

买票流程：
1，　安装python和pycharm，根据环境需求配置相应的环境
2，　安装google chrome和chromedriver
3，　运行cookies_save.py，输入帐号和验证码，保存cookies
4，　配置config.json文件，根据自己的需求
5，　运行Autoticket.py文件
6，　手动付款
7，　买票完成
