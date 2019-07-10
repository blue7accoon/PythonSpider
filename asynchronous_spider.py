#!/usr/bin/env python
# coding: utf-8



# 异步爬虫
import asyncio,time
import requests,concurrent.futures
from scrapy import Selector


# 获取html内容
def getHtml(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
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
    try:
        for page in quotesInfo:
            for quote in page:
                print(time.strftime("[%Y-%m-%d %H-%M-%S]"),
                      "{0} -- {1}".format(quote[0],
                      quote[1]), end="\n\n")
    except:
        pass


#  将爬取的内容生成txt文件
def genTextFile(quotesText):
    try:
        with open("quotes.txt", "a") as f:
            for page in quotesText:
                for quote in page:
                    print(time.strftime("[%Y-%m-%d %H-%M-%S]"),
                          "{0} -- {1}".format(quote[0],
                          quote[1]), file=f, end="\n\n")
    except:
        pass


# 爬取单个网页完整流程
def spider(page):
    print("Scrape page <{}> from toscrape.com!".format(page))
    start = time.time()
    url = "http://quotes.toscrape.com/page/{}/".format(page)
    htmlText = getHtml(url)
    quotesInfo = htmlParser(htmlText)

    end = time.time()
    print("[Page {0}] handled for {1:.4f} seconds!".format(page, end-start))
    return quotesInfo

# 转换为协程
async def main(all_quotes):
    loop = asyncio.get_event_loop()
    # asyncio外部函数即使转换为协程也无法异步执行
    # 需要调用run_in_executor方法生成额外的进程
    # 或线程来达到异步执行的效果
    with concurrent.futures.ThreadPoolExecutor(10) as pool:
        results = (
            loop.run_in_executor(pool, spider, i) for i in range(1, 11)
        )

        # 不可删除
        for result in await asyncio.gather(*results):
            all_quotes.append(result)



if __name__=="__main__":
    op = time.time()
    all_quotes = []
    print("Asynchronous spider start scraping!", end="\n\n")
    print("-" * 45)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(all_quotes))
    printQuotes(all_quotes)
    genTextFile(all_quotes)

    ed = time.time()
    print("-*" * 22 + "-")
    print("Scraping complete,total consuming time: {:.4f}!".format(ed-op))

