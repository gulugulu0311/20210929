import json
import time

import requests
import send_mail
from lxml import etree


def get_url_list():
    with open('novel_list.json', 'r', encoding="utf-8") as f:
        return json.load(f)


def get_page(novel_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36 '
    }

    res = requests.get(novel_url, headers=headers)
    res.encoding = 'utf-8'
    return etree.HTML(res.text)


def record_in_json(data):
    with open('record.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


def get_chapter_content(chapter_url):
    chapter_html = get_page(chapter_url)
    return chapter_html.xpath('//div[@class="read-content j_readContent"]/p/text()')


def check(index_id):
    with open('record.json', 'r', encoding='utf-8') as f:
        record_list = json.load(f)
        try:
            return record_list[index_id - 1]['total_record']
        except IndexError:
            return 0


def main():
    data = []  # 字典列表 change to json
    for item_url in get_url_list():
        novel_id = item_url['id']
        html = get_page(item_url['url'])
        # 小说名称
        novel = html.xpath('//div[@class="crumbs-nav center990  top-op"]/span/a/text()')[3]
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
        content = '\n'.join(get_chapter_content(newest_link))
        # json
        data.append({
            "total_record": total_current,
            "title": novel + '\t' + chapters[newest_index],
            "content": content + '...'
        })

        # 发送邮件
        if not check(novel_id) == total_current:  # 章节数目改变，即小说更新
            send_mail.mail(novel + ' ' + chapters[newest_index], content)
    record_in_json(data)

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)
