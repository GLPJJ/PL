import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Http 模块
import http.client
import urllib.parse
# json解析模块
import json

import time
import urllib.request
import cv2
import numpy as np
# 随机数
import random

# 优先在vscode中调试python代码，后期执行可以用sublime，因为vscode有点卡

# For instance, consider this page source:

# <html>
#  <body>
#   <form id="loginForm">
#    <input name="username" type="text" />
#    <input name="password" type="password" />
#    <input name="continue" type="submit" value="Login" />
#    <input name="continue" type="button" value="Clear" />
#   </form>
# </body>
# <html>
# The form elements can be located like this:
# 	login_form = driver.find_element_by_xpath("/html/body/form[1]")
# 	login_form = driver.find_element_by_xpath("//form[1]")
# 	login_form = driver.find_element_by_xpath("//form[@id='loginForm']")

# 如果这个放到闭包中，出了闭包，页面的内容就会消失
Browser = webdriver.Chrome()
# Browser.set_window_size(1280,800)
Browser.maximize_window()
# Browser.refresh()

HEADERS = {"Content-type": "application/json", "Accept": "text/plain"}


def get_tracks(width, type=1):
    v = 0
    tracks = []
    current = 0

    if type == 1:
        while current <= width:
            t = random.random()*0.3+0.05
            v0 = v
            v = v0 + 6 * t
            s = (v0 + v) / 2 * t
            current += s
            tracks.append(round(s))
    elif type == 2:
        mid = width*4/5
        while current <= width:
            t = random.random()*0.3+0.05
            if current < mid:  # 小余这个位置，以加速度a前进(simulate加速过程)
                a = 2
            else:  # 大于这个位置了，以加速度a前进(simulate减速过程)
                a = -3
            v0 = v
            v = v0 + a * t
            s = (v0 + v) / 2 * t
            current += s
            tracks.append(round(s))
    return tracks


def defend_with_tb(browser):
    pass
    # chrome_options = browser.ChromeOptions()
    # chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument('--profile-directory=Default')
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-plugins-discovery");
    # chrome_options.add_argument("--start-maximized")
    # browser = browser.Chrome(chrome_options=chrome_options)
    # browser.delete_all_cookies()
    # browser.set_window_size(800,800)
    # browser.set_window_position(0,0)


def defend_with_tb2(browser):
    js1 = "Object.defineProperties(navigator,{ webdriver:{ get: () => false } });"
    js2 = "window.navigator.chrome = { runtime: {},  };"
    js3 = "Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });"
    js4 = "Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], });"
    browser.execute_script(js1)
    browser.execute_script(js2)
    browser.execute_script(js3)
    browser.execute_script(js4)

# 启动钉钉通知消息
def ding_text(token, content, numbers, is_all):
    """
    token：Token令牌
    content：通知内容
    numbers：通知列表
    is_all：是否全员通知
    """
    # https://oapi.dingtalk.com/robot/send?access_token=75dc4036476a829d8d4bcfefcc674310c7c1cd3ee373c9851ad64e0f184b2494

    # print("ding_text")
    conn = http.client.HTTPSConnection("oapi.dingtalk.com")
    # print(conn)

    tempHead = dict(HEADERS)
    #print("tempHead = ",tempHead);

    params_at = {"atMobiles": numbers, "isAtAll": is_all}
    # print(params_at)

    # params_content = {"content": content}
    # print(params_content)
    # dictParams = {'msgtype': 'text', "text": params_content, "at": params_at}
    whoToAt = ""
    for i in range(len(numbers)):
        whoToAt += "@"+str(numbers[i])

    params_content = {"title": "通知消息", "text": content+"\n"+whoToAt}
    print(params_content)
    dictParams = {'msgtype': 'markdown',
                  "markdown": params_content, "at": params_at}
    # print(dictParams)

    json_params = json.dumps(dictParams)
    # print(json_params)

    # params =  urllib.parse.urlencode(dictParams)
    # print(params)

    try:
        conn.request("POST", "/robot/send?access_token=" +
                     token, json_params, tempHead)

        response = conn.getresponse()
        data = response.read()

        # print(type(data))
        print("ding_text", response.status, response.reason,
              data.decode(), sep=' ; ')  # 指定分隔符
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass

def ding_text_ex(result,title):
    content = "# "+title+"\n"
    for i in range(len(result)):
        content = content+"## "+result[i]["color"]+"\n"
        sizes = result[i]["sizes"]
        for j in range(len(sizes)):
            if not sizes[j]["stock"]:
                continue
            stock = "有货" if sizes[j]["stock"] else "无货"
            content = content+"### "+ sizes[j]["size"]+"-("+stock+")\n"

    # https://oapi.dingtalk.com/robot/send?access_token=828b77c2b4eccc95e3d0e30335824cad2d58bd761d82d3023b0fad4cfbdab4f0
    ding_text("828b77c2b4eccc95e3d0e30335824cad2d58bd761d82d3023b0fad4cfbdab4f0", content, [], True)


"""
淘宝乔丹鞋子数据结构
{
    color = "",
    sizes = [
        {
            size = 40,
            stock = False 表示无库存
        },
    ]
}
"""
def random_sleep(base=0.5,x=1,can=False):
    time.sleep(random.random()*x+base)
    print("模拟人等待。。。")

    try:
        times = int(random.random()*20)
        if can and times > 17:
            try:
                element_tmsy = Browser.find_element_by_xpath('//*[@id="sn-bd"]/div/p[1]/a')
                element_tmsy.click()
                time.sleep(random.random()*5+3)
                print("模拟人等待。。。")
                Browser.back()
            except Exception as e:
                print("模拟点击首页失败，尝试点击店铺,e=",e)

                # //*[@id="shop16722994182"]/div/div[2]/div/div/div/div[2]
                try:
                    element_sp = Browser.find_element_by_xpath("//a[@class=shopLink]")
                    element_sp.click()
                    time.sleep(random.random()*5+3)
                    print("模拟人等待。。。")
                    Browser.back()
                except Exception as e:
                    print("模拟点击商铺失败,e=",e)
                    time.sleep(random.random()*5+3)
        elif times > 14:
            # //*[@id="shop16722994182"]/div/div[2]/div/div/div/div[2]
            try:
                element_gwc = Browser.find_element_by_xpath('//*[@id="J_MUIMallbar"]/div/div[2]/div[10]/div[3]')
                element_gwc.click()
            except Exception as e:
                print("模拟点击购物车失败... e=",e)

            # driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.random()*10+5)
            print("模拟人等待。。。")
            # driver.close()
        else:
            element_body = Browser.find_element_by_xpath("//body")
            for i in range(times):
                element_body.click()
                time.sleep(random.random()*1)
                print("模拟人等待。。。")
    except Exception as e:
        print("随机等待异常,e=",e)


def get_stock(elements_ys_status, elements_cm_status, elements_cm, elements_kc):
    ret = []
    for i in range(len(elements_ys_status)):
        shoes = {
            "color": elements_ys_status[i].get_attribute("title"),
            "sizes": []
        }
        random_sleep(1)

        if elements_ys_status[i].is_displayed():
            if elements_ys_status[i].get_attribute("class") != "tb-selected":
                elements_ys_status[i].click()  # 选中颜色
            for j in range(len(elements_cm_status)):
                stockFlag  = False
                if elements_cm_status[j].get_attribute("class") != "tb-out-of-stock":
                    # stock = elements_kc.text
                    # stockInt = int(stock[2:-1])
                    # print(stock, stockInt)  # 过滤 库存 件
                    random_sleep(1)
                    stockFlag = True

                shoes["sizes"].append({
                    "size": elements_cm[j].text,
                    "stock": stockFlag
                })
        else:
            for j in range(len(elements_cm_status)):
                shoes["sizes"].append({
                    "size": elements_cm[j].text,
                    "stock": False
                })

        ret.append(shoes)
    return ret


def get_stocks(browser, clsId, title):
    """
    tb-sku
    """
    # element_tb_sku = browser.find_element_by_class_name(clsId)
    # print(element_tb_sku)

    # "tb-out-of-stock"

    # 获取到颜色
    # //*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[2]/dd/ul/li[1]
    elements_ys_status = browser.find_elements_by_xpath(
        '//div[@class="'+clsId+'"]/dl[2]/dd/ul/li')
    # //*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[2]/dd/ul/li[1]/a/span
    # elements_ys = browser.find_elements_by_xpath(
    #     '//div[@class="'+clsId+'"]/dl[2]/dd/ul//span')

    print(elements_ys_status[0].is_selected())
    print(elements_ys_status[0].get_attribute("class"))
    print(elements_ys_status[0].get_attribute("title"))

    # elements_ys_status[1].click()
    # 获取到尺码
    # 利用chrome的 右击结点,Copy->Copy XPath
    # //*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[1]
    elements_cm_status = browser.find_elements_by_xpath(
        '//div[@class="'+clsId+'"]/dl[1]/dd/ul/li')
    # //*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[1]/a/span
    elements_cm = browser.find_elements_by_xpath(
        '//div[@class="'+clsId+'"]/dl[1]/dd/ul//span')
    print(elements_cm_status[1].get_attribute("class"))
    print(elements_cm[1].text)

    # //*[@id="J_EmStock"]
    elements_kc = browser.find_element_by_xpath('//*[@id="J_EmStock"]')
    stock = elements_kc.text
    print(stock, stock[2:-1])  # 过滤 库存 件
    # print(elements_kc.text,elements_kc.text[2:-1])
    result = get_stock(elements_ys_status, elements_cm_status,
                       elements_cm, elements_kc)
    print(result)  # 通知服务器

    ding_text_ex(result,title)


def main_nike2(browser, url, targetUrl, title):
    defend_with_tb(browser)
    browser.get(url)
    defend_with_tb2(browser)
    # print(browser.current_url)
    # print(browser.page_source)
    # 跳转到指定的iframe

    browser.switch_to.frame(browser.find_element_by_id("J_loginIframe"))
    # time.sleep(1) #1秒钟等待。
    # print("*"*100 + "GLP\n\n\n")
    # print(browser.page_source)
    # browser.close()

    # try:
    # 	#10秒
    # 	element_mmdl = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "J_Quick2Static")))
    # 	print(element_mmdl)
    # finally:
    # 	browser.quit()

    # element_mmdl = browser.find_element_by_css_selector("p.content")
    # element_mmdl = browser.find_element_by_class_name("iconfont")
    # element_mmdl = browser.find_element_by_partial_link_text("密码登录")
    # element_mmdl = browser.find_element_by_id("J_Quick2Static")
    # element_mmdl = browser.find_element_by_xpath('//*[@id="J_Quick2Static"]')
    # //*表示匹配任意标签,我们这里只匹配i标签
    try:
        element_mmdl = browser.find_element_by_xpath(
            '//i[@id="J_Quick2Static"]')
        element_mmdl.click()  # 点击密码登录
    except Exception as e:
        print("打开登录页面失败，e=", e)
    # print(element_mmdl)

    element_zh = browser.find_element_by_xpath(
        '//input[@id="TPL_username_1"]')  # 账号
    # element_zh.click() #输入框点击会报错
    element_zh.send_keys('cnmbyzm')
    random_sleep(1)

    fail_try = 0
    while not browser.current_url.startswith(targetUrl):
        try:
            element_mm = browser.find_element_by_xpath(
                '//input[@id="TPL_password_1"]')  # 密码
            # element_mm.click()
            element_mm.send_keys('cnmbyzm')
            time.sleep(1)

            try:
                element_hk = browser.find_element_by_xpath(
                    '//span[@id="nc_1_n1z"]')  # 滑块
                # 下面进行一个序列化操作。。
                actions = ActionChains(browser)
                actions.click_and_hold(on_element=element_hk)  # 首先鼠标按下并保持

                tracks = get_tracks(320)
                for track in tracks:
                    actions.move_by_offset(
                        xoffset=track, yoffset=0).perform()  # 鼠标位移
            except Exception as e:
                pass

            # actions.move_by_offset(xoffset=300, yoffset=0)
            # actions.release(on_element=element_hk).perform()# 鼠标抬起

            time.sleep(3)
            element_btn_dl = browser.find_element_by_xpath(
                '//button[@id="J_SubmitStatic"]')  # 登录按钮
            element_btn_dl.click()

            time.sleep(1)
            element_msg = browser.find_element_by_xpath(
                '//div[@id="J_Message"]')  # 登录按钮
            if not element_msg.is_displayed():
                print("登录成功")
                break
            else:
                fail_try = fail_try + 1
                print("登录失败", fail_try)
        except Exception as e:
            time.sleep(3)
            print(e)

    print(browser.current_url)
    # print(browser.page_source)

    while True:
        try:
            get_stocks(browser, "tb-sku", title)
        except Exception as e:
            print("获取商品信息失败,e=", e)
        random_sleep(90,1,True) # 10秒后刷新页面，重新获取商品库存。
        Browser.refresh()



if __name__ == '__main__':
    url = r"https://login.tmall.com/?spm=a220o.1000855.a2226mz.2.1f627ecbpROZxN&redirectURL=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm%3Da1z10.4-b-s.w5003-21076098180.3.31c9174a5Yi3QI%26id%3D576640717890%26scene%3Dtaobao_shop%26sku_properties%3D1627207%3A2471828828"
    main_nike2(Browser, url, "https://detail.tmall.com/item.htm","Jordan官方AIR JORDAN XXXIII PF AJ33男子篮球鞋BV5072")

    Browser.quit()
