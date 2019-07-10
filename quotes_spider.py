#!/usr/bin/env python
# coding: utf-8

import time,requests
from scrapy import Selector



# 获取html内容
def get_html(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        return response.text
    except:
        pass


# 对获取的内容进行解析
def html_parser(htmlText):
    try:
        selector = Selector(text=htmlText)
        author = selector.css('small[class="author"]::text').getall()
        quote = selector.css('span[class="text"]::text').getall()
        quotesList = list(zip(quote, author))
        return quotesList
    except:
        pass


# 将解析后的内容打印在标准输出
def quotes_printer(quotesInfo):
    for quote in quotesInfo:
        print(time.strftime("[%Y-%m-%d %H-%M-%S]"),
              "{0}--{1}".format(quote[0],quote[1]),
              end="\n\n")


# 入口函数
def main():
    start = time.time()
    url = "http://quotes.toscrape.com/page/{}/"

    for i in range(1, 11):
        begin = time.time()
        htmlText = get_html(url.format(i))
        quotesInfo = html_parser(htmlText)
        quotes_printer(quotesInfo)
        finish = time.time()
        print("-" * 36)
        print("page  <{0}>  complete! time consuming:{1:.4f}".format(i, finish-begin))
        print("-" * 36)

    end = time.time()
    print("*" * 36)
    print("Total consuming time: {:.4f}!".format(end-start))
    print("*" * 36)


if __name__ == "__main__":
    main()

