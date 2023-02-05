from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:

    @staticmethod
    def read_txt_file(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            queries = []
            for line in lines:
                queries.append(line.strip('\n').rstrip())
            return queries

    @staticmethod
    def search(query, searching_url, sleep=True):
        if sleep:
            time.sleep(randint(1,5))
        #n = 30
        # temp_url = '+'.join(query.split()) + "&n=" + str(n)
        temp_url = '+'.join(query.split())
        url = searching_url + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results
    

    @staticmethod
    def scrape_search_result(soup):
        # raw_results = soup.find_all("a", attrs = {"class" : "d-ib fz-20 lh-26 td-hu tc va-bot mxw-100p"})
        raw_results = soup.find_all("a", attrs = {"class" : "result__a"})
        results = []
        for result in raw_results:
            link = result.get('href')
            if link not in results:
                results.append(link)
            if len(results) == 10:
                break
        return results

    @staticmethod
    def write_to_file(filename, query_results):
        with open(filename, 'w') as f:
            json.dump(query_results, f)


if __name__ == "__main__":
    search_engine = SearchEngine()

    filename = "../data/queries_ddg.txt"
    url = "https://www.duckduckgo.com/html/?q="
    write_filename = "../results/hw1.json"

    query_results = dict()
    queries = search_engine.read_txt_file(filename)

    for query in queries:
        new_results = search_engine.search(query, url)
        query_results[query] = new_results
        print(query_results)
    
    search_engine.write_to_file(write_filename, query_results)
    



