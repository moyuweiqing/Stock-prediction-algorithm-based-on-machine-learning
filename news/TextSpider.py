#爬虫须知：
#  1、运行前请配置包 requests、bs4、lxml、xlutils、my_fake_useragent

import requests
from bs4 import BeautifulSoup as bs
from my_fake_useragent import UserAgent
#这库用来随机生成user_agent 在这个爬虫中好像没必要

def pagenext():
    base_url = 'http://finance.people.com.cn/index'
    all_content = [];
    for i in range(1,5):
        next_url = base_url + str(i)+'.html#fy01'
        print("获取 ",i," 页")
        page_text = spider(next_url)      #跑第*页的爬虫 获取那一页的数据
        all_content+=page_text
        # time.sleep(10)        #休息一会 防被网站 ban

    for index1 in range(len(all_content)):
        txt_name = "data"+str(index1) +".txt"
        with open(txt_name, "w") as f:
            # f.write('\r')
            for index2 in range(len(all_content[index1])):
                f.write(all_content[index1][index2])
                f.write('\r')
            f.write('\r\n')
        print("写入 ", txt_name)

#进入了文章的具体ulr
def datespider(date_url):
    #设置一下 UserAgent 突破反扒
    response_try = requests.get(date_url, UserAgent().random())
    res = response_try.content
    html = str(res, 'gbk')
    # 用BeautifulSoup框架转化
    response_tree = bs(html, 'lxml')
    if(response_tree==None):
        return []
    else:
        html_el= response_tree.find("div", class_="clearfix w1000_320 text_title")
        author_text = html_el.find("p", class_="author").get_text()
        # author_data =  re.sub(r'\xa0', '', author_text)
        author_data = author_text.replace("\xa0", " ")
        time_el = html_el.find("div", class_="fl")
        time_text = time_el.get_text();
        # 去除杂质
        # time_data =  re.sub(r'\xa0|来源', '', time_text)
        time_data = time_text[0:16]
        time_data = "".join(time_data)
        form_text = time_el.find("a").get_text()
        content_el = response_tree.select('#rwb_zw')[0]
        p_el = content_el.find_all("p")
        content_text = ''
        for text in p_el:
            text_before = text.get_text()
            text_after = text_before.replace("\xa0", " ")
            content_text += text_after
        response_All = []
        response_All.append(author_data)
        response_All.append(time_data)
        response_All.append(form_text)
        response_All.append(content_text)
        return response_All

def spider(url):
    response = requests.get(url, {'User-Agent':UserAgent().random()})
    res = response.content
    html = str(res, 'gbk')
    html_tree = bs(html, 'lxml')
    # 找class =headingNews qiehuan1_c标签下的内容
    html_text = html_tree.find_all("div", class_="headingNews qiehuan1_c")
    h5_text = html_text[2].find_all("h5")

    All_text = []
    for text in h5_text:
        one_text = []
        a_href = text.find('a')['href'];
        # one_text.append(a_href)
        text_title = text.get_text()
        one_text.append(text_title)
        # 调用函数 进去各个文章的具体网站 找其他信息
        text_all = datespider(a_href)
        one_text+=text_all
        All_text.append(one_text)
    return All_text

if __name__ == '__main__':
    pagenext()