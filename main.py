import json
import time

import requests
import send_mail
from lxml import etree

URL = 'https://book.qidian.com/info/1027669580/#Catalog'  # 目录url


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36 '
    }

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    return etree.HTML(res.text)


def save_to_json(data):
    with open('record.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


def get_chapter_content(chapter_url):
    chapter_html = get_page(chapter_url)
    return chapter_html.xpath('//div[@class="read-content j_readContent"]/p/text()')


def check():
    with open('record.json', 'r', encoding='utf-8') as f:
        dict = json.load(f)
        return dict['total_record']


def main():
    html = get_page(URL)
    # 章节名称
    chapters = html.xpath('//ul[@class="cf"]/li/a/text()')
    # 章节link
    links = html.xpath('//ul[@class="cf"]/li/a/@href')
    # 最新章节url
    newest_link = 'https:' + links[len(links) - 1]
    # 当前更新章节总数
    total_current = len(chapters)
    newest_index = total_current - 1  # 索引
    # 邮件内容
    content = ''.join(get_chapter_content(newest_link))

    # json
    data = {
        "total_record": total_current,
        "title": chapters[newest_index],
        "content": content + '...'
    }

    # 发送邮件
    if not check() == total_current:    # 章节数目改变，即小说更新
        send_mail.mail(chapters[newest_index], content)
        # 记录
        save_to_json(data)
    # print(content)
    # print(chapters[newest_index])
    print('-----------------------------------')


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)
