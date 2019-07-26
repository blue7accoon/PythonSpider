#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool
import requests,time,os
from scrapy import Selector
# from multiprocessing import freeze_support


# 获取html内容
def getHtml(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        return response.text
    except:
        pass


# 解析html内容
def htmlParser(htmlText):
    quotesList = []
    try:
        selector = Selector(text=htmlText)
        authors = selector.css('small[class="author"]::text').getall()
        quotes = selector.css('span[class="text"]::text').getall()
        for i in range(len(quotes)):
            quotesList.append((quotes[i], authors[i]))
        return quotesList
    except:
        pass


# 将解析后的内容打印在标准输出
def printQuotes(quotesInfo):
    for n in range(len(quotesInfo)):
        print(time.strftime("[%Y-%m-%d %H-%M-%S]"),
              "{0} -- {1}".format(quotesInfo[n][0],
              quotesInfo[n][1]), end="\n\n")


# 将爬取的内容生成txt文件
def genTxtFile(quotesText):
    try:
        with open("quotes.txt", "a") as f:
            for n in range(len(quotesText)):
                print(time.strftime("[%Y-%m-%d %H-%M-%S]"),
                      "{0} -- {1}".format(quotesText[n][0],
                      quotesText[n][1]), file=f, end="\n\n")
    except:
        pass


# 单个页面的完整爬取过程
def quotesSpider(page):
    print("[Process id of page <{0}>: {1}]".format(page, os.getpid()))
    start = time.time()
    url = "http://quotes.toscrape.com/page/{}/".format(page)
    htmlText = getHtml(url)
    quotesInfo = htmlParser(htmlText)
    printQuotes(quotesInfo)
    genTxtFile(quotesInfo)
    end = time.time()
    print("-" * 36)
    print("[Page {0}] handled for {1:.4f} seconds!".format(page, end-start))
    print("-" * 36)


# 入口函数
def main():
    begin = time.time()
    print("Start scraping, main process id: {}".format(os.getpid()))
    print("-" * 45)

    p = Pool(10)
    for i in range(1, 11):
        p.apply_async(quotesSpider, args=(i,))
    p.close()
    p.join()

    finish = time.time()
    print("-*" * 22 + "-")
    print("Scraping complete,total "
          "consuming time: {:.4f}!".format(finish - begin))


# Windows平台下运行multiprocessing模块必须添加
# if __name__ == "__main__"语句，如若仍然报错
# 可添加freeze_support()尝试解决
if __name__ == "__main__":
    main()

