# coding: utf-8
from json import loads
from os.path import exists
from pickle import dump, load
from time import sleep, time
# import io # 用于py2.7时解注释

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions

option__ = ChromeOptions()
option__.add_experimental_option('excludeSwitches', ['enable-automation'])

price_option = [
    'color: rgb(245, 104, 61);', #　红色
    'color: rgb(240, 200, 50);', #　黄色
    'color: rgb(150, 200, 10);', #　浅绿色
    'color: rgb(0,   120, 0 );', #　深绿色
    'color: rgb(100, 190, 24);', #　浅蓝色
    'color: rgb(10, 120, 150);'  #　深蓝色
]

class Concert(object):
    def __init__(self, session, price, date, real_name, tel, id_name, ticket_position, polyt_url, target_url, browser):
        self.session = session  # 场次序号优先级
        self.price = price  # 票价序号优先级
        self.date = date # 日期选择
        self.real_name = real_name  # 收件人姓名
        self.tel = tel # 收件人电话号码
        self.status = 0  # 状态标记
        self.time_start = 0  # 开始时间
        self.time_end = 0  # 结束时间
        self.num = 0  # 尝试次数
        self.type = 0  # 目标购票网址类别
        self.id_name = id_name  # 用户身份信息
        self.ticket_pos = ticket_position  # 购买票位置
        self.damai_url = polyt_url  # polyt网官网网址
        self.target_url = target_url  # 目标购票网址
        self.browser = browser # 0代表Chrome，1代表Firefox，默认为Chrome
        self.total_wait_time = 3 # 页面元素加载总等待时间
        self.refresh_wait_time = 0.3 # 页面元素等待刷新时间
        self.intersect_wait_time = 0.5 # 间隔等待时间，防止速度过快导致问题

        if self.target_url.find("m.polyt.cn") != -1:# polyt.cn
            self.type = 1
        elif self.target_url.find("piao.damai.cn") != -1:
            self.type = 2
        else:
            self.type = 0
            self.driver.quit()
            raise Exception("***Error:Unsupported Target Url Format:{}***".format(self.target_url))

    def isClassPresent(self, item, name, ret=False):
        try:
            result = item.find_element_by_class_name(name)
            if ret:
                return result
            else:
                return True
        except:
            return False

        
    def get_cookie(self):
        self.driver.get(self.damai_url)
        while self.driver.title.find('登录 - 爱演出 爱生活 - 保利票务') != 0:  # 等待网页加载完成
            sleep(1)
        print("###请点击登录###")
        telephone = self.driver.find_elements_by_class_name('van-field__control')
        telephone[0].send_keys('15003890992')
        telephone[1].send_keys('3733384')
        button = self.driver.find_elements_by_id('nc_1_n1z')
        while len(button) == 0:  # 等待网页加载完成
            sleep(1)
            button = self.driver.find_elements_by_id('nc_1_n1z')
        action = ActionChains(self.driver)
        action.click_and_hold(button[0]).perform()
        # action.reset_actions()
        action.move_by_offset(200, 0).perform()
        action.release().perform()
        input_click = self.driver.find_elements_by_class_name('van-button')
        input_click[0].click()
        # print("###请登录###")
        # selection = self.driver.find_elements_by_class_name('van-cell_title')
        # # while self.driver.title == '爱演出 爱生活 - 保利票务':  # 等待扫码完成
        # sleep(1)
        dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")

        
    def set_cookie(self):
        try:
            cookies = load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.polyt.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

            
    def login(self):
        if not exists('cookies.pkl'):  # 如果不存在cookie.pkl,就获取一下
            if self.browser == 0: # 选择了Chrome浏览器
                self.driver = webdriver.Chrome(options=option__)
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                                Object.defineProperty(navigator, 'webdriver', {
                                  get: () => undefined
                                })
                              """
                })
            elif self.browser == 1: # 选择了Firefox浏览器
                self.driver = webdriver.Firefox()
            else:
                raise Exception("***错误：未知的浏览器类别***")
            self.get_cookie()
            self.driver.quit()
        print('###打开浏览器，进入保利网###')
        if self.browser == 0: # 选择了Chrome浏览器，并成功加载cookie，设置不载入图片，提高刷新效率
            options = webdriver.ChromeOptions() # selenium配置浏览器的参数,创建ChromeOptions()类
            prefs = {"profile.managed_default_content_settings.images":2}
            options.add_experimental_option("prefs",prefs) #添加实验性质的设置参数
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """
            })
        elif self.browser == 1: # 选择了火狐浏览器
            options = webdriver.FirefoxProfile()
            options.set_preference('permissions.default.image', 2)  
            self.driver = webdriver.Firefox(options)
        else: 
            raise Exception("***错误：未知的浏览器类别***")
        self.driver.get(self.target_url)
        self.set_cookie()
        # self.driver.maximize_window()
        self.driver.refresh() # 刷新

    def puchase_ticket(self):
        self.login()
        # self.driver.implicitly_wait(self.total_wait_time)
        purchase_click = self.driver.find_elements_by_class_name('btn-show-ticket')
        purchase_click[0].click()
        print('开始购票')
        while len(self.driver.find_elements_by_class_name('show-ticket-show-info')) == 0:
            sleep(1)
        time_click = self.driver.find_elements_by_class_name('show-ticket-tag')
        time_click[self.date].click()
        print('选择日期')
        while len(self.driver.find_elements_by_class_name('buy-btn')) == 0:
            sleep(1)
        buy_click = self.driver.find_elements_by_class_name('buy-btn')
        buy_click[0].click()
        print('开始购票')
        while len(self.driver.find_elements_by_class_name('poly-icon-seat')) == 0:
            sleep(1)
        seat_item = self.driver.find_elements_by_class_name('poly-icon-seat')
        print('查找当前可用座位')
        seat_optim = [(seat_item[i]) for i in range(len(seat_item)) if
                      seat_item[i].get_attribute('style') == price_option[self.price]]
        # seat_optim = []
        # for i in range(len(seat_item)):
        #     if seat_item[i].get_attribute('style') == 'color: rgb(245, 104, 61);':
        #         seat_optim.append(seat_item[i])
        print('当前可挑选座位一共有:', len(seat_optim))
        seat_select = seat_optim[self.ticket_pos]
        seat_select.click()
        while len(self.driver.find_elements_by_class_name('choose-btn')) == 0:
            sleep(1)
        final_choose_btn = self.driver.find_elements_by_class_name('choose-btn')
        final_choose_btn[0].click()
        while len(self.driver.find_elements_by_class_name('pick-btn')) ==0:
            sleep(1)
        p_click = self.driver.find_elements_by_class_name('pick-btn')
        p_click[self.id_name].click()
        # name = self.driver.find_elements_by_class_name('van-field__body')
        # name[0].send_keys('徐萌萌')
        while len(self.driver.find_elements_by_class_name('btn-submit')) == 0:
            sleep(1)
        btn_submit = self.driver.find_elements_by_class_name('btn-submit')
        btn_submit[0].click()
        print('订单生成')
        while len(self.driver.find_elements_by_class_name('van-cell__title')) == 0:
            sleep(1)
        btn_radio = self.driver.find_elements_by_class_name('van-cell__title')
        btn_radio[1].click()
        print('选择支付宝')
        while len(self.driver.find_elements_by_class_name('bottom-btn')) == 0:
            sleep(1)
        bottom_btn = self.driver.find_elements_by_class_name('bottom-btn')
        bottom_btn[0].click()
        sleep(10)
        self.driver.quit()

    def finish(self):
        self.time_end = time()
        if self.status == 6:  # 说明抢票成功
            print("###抢票共耗时%f秒，抢票成功！请确认订单信息###" % (round(self.time_end - self.time_start, 3)))
        else:
            self.driver.quit()


if __name__ == '__main__':

    try:
        # with io.open('./config.json', 'r', encoding='utf-8') as f: # 用于py2.7时解注释
        with open('./config.json', 'r', encoding='utf-8') as f: # 用于py2.7时注释此处
                    config = loads(f.read())
        con = Concert(config['sess'], config['price'], config['date'], config['real_name'], config['tel'], config['id_name'], config['ticket_position'],
                      config['polyt_url'], config['target_url'], config['browser'])
    except Exception as e:
        print(e)
        raise Exception("***错误：初始化失败，请检查配置文件***")
    con.puchase_ticket()
    # while True: # 可用于无限抢票，防止弹窗类异常使抢票终止
    # if True:
    #     try:
    #         if con.type == 1:  # detail.damai.cn
    #             con.choose_ticket_1()
    #             con.check_order_1()
    #         elif con.type == 2:  # piao.damai.cn
    #             con.choose_ticket_2()
    #             con.check_order_2()
    #         # break
    #     except Exception as e:
    #         print(e)
    #         con.driver.get(con.target_url)
    con.finish()
