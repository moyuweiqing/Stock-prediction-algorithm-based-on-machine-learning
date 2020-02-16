import requests
from lxml import etree
import datetime
import jieba
import jieba.analyse

start = datetime.date(2019, 10, 1)  # 起始日期
end = datetime.date(2019, 11, 30)  # 结束日期
my_word = ['金融', '经济']
my_title = []
f=open('cctv.txt', 'w')

while start <= end:
    url = 'http://tv.cctv.com/lm/xwlb/day/' + start.strftime('%Y%m%d') + '.shtml'
    r = requests.post(url, timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    html = etree.HTML(r.text)
    html_data = html.xpath('/html/body/ul[*]/li[*]/a/div[2]/div[1]')

    f.write(str(start))
    f.write('\n')
    for i in html_data:  # 数据处理
        print(i.text)
        fenci_text = jieba.cut(i.text)
        for j in fenci_text:
            if j in my_word:
                my_title.append(i.text)
                f.write(i.text)
                f.write('\n')
                break;
            else:
                continue;

    start += datetime.timedelta(days=1)

print(my_title)