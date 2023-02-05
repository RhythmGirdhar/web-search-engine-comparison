import json
from os import stat
from typing import overload
import numpy as np
from scipy.stats import spearmanr
import re
import pandas as pd

class Calculate:
    
    @staticmethod
    def read_txt_file(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            queries = []
            for line in lines:
                queries.append(line.strip('\n').rstrip())
            return queries

    @staticmethod
    def read_file(file1, file2):
        with open(file1, 'r') as f:
            data1 = json.load(f)
        with open(file2, 'r') as f:
            data2 = json.load(f)
        return data1, data2

    @staticmethod
    def preprocess_urls(data):
        for key, values in data.items():
            for i, url in enumerate(values):            
                url = re.sub(r'^https?://', '', url)
                url = re.sub(r'^www\.', '', url)
                url = re.sub(r'/$', '', url)
                values[i] = url  
        return data

    @staticmethod
    def percent_overlap(data1, data2):  
        overlap_all = []
        for key1, values1 in data1.items():
            for key2, values2 in data2.items():
             if key1 == key2: 
                overlap = set(values1) & set(values2)
                percent_overlap = len(overlap) / len(set(values1 + values2)) * 100
                overlap_all.append(percent_overlap)     

        return sum(overlap_all) / len(overlap_all)

    @staticmethod
    def spearman_coefficient(data1, data2):
        common_keys = set(data1.keys()).intersection(data2.keys())
        values1 = [data1[key] for key in common_keys]
        values2 = [data2[key] for key in common_keys]
        return spearmanr(values1, values2)[0]

    @staticmethod
    def get_results(data1, data2, queries):
        result = []

        for i, query in enumerate(queries):
            google = data1[query]
            ddg = data2[query]
    
            overlap = []

            for j,res_g in enumerate(google):
                for k,res_d in enumerate(ddg):
                    if res_g == res_d:
                        overlap.append((j+1,k+1))
            
            QUERY_NAME = 'Query ' + str(i+1)
            OVERLAPS = len(overlap)
            PERCENT_OVERLAP = round(len(overlap)/10*100, 1)
            RHO = None
        
            #if no overlap
            if len(overlap) == 0:
                RHO = 0
    
            #if same rank, rho is 1 else 0
            elif len(overlap) == 1:
                if overlap[0][0] == overlap[0][1]:
                    RHO = 1
                else:
                    RHO = 0

            else:
                sum_di_sq = 0
                for pair in overlap:
                    di = pair[0] - pair[1]
                    di_sq = di*di
                    sum_di_sq += di_sq
                RHO = round(1 - ((6 * sum_di_sq) / (OVERLAPS * (OVERLAPS ** 2 -1))), 2)
                
            
            result.append([QUERY_NAME, int(OVERLAPS), PERCENT_OVERLAP, RHO])


            columns = ['Queries', 'Number of Overlapping Results', 'Percent Overlap', 'Spearman Coefficient']
            df = pd.DataFrame(data = result, columns = columns)

            df.mean(axis=0)
            averages = df.mean(axis=0)   
            averages_df = pd.DataFrame({
            'Queries':['Averages'], 
            'Number of Overlapping Results':[round(averages[0],2)], 
            'Percent Overlap':[round(averages[1],2)], 
            'Spearman Coefficient':[round(averages[2],2)]}, index=["100"])

            df = df.append(averages_df)  
        return df   

    @staticmethod
    def write_csv_file(csv_file, df):
        df.to_csv(csv_file, index=False)
        return


if __name__ == "__main__":

    file1 = '../data/Google_Result4.json'
    file2 = '../results/hw1_duckduckgo.json'
    query_txt_file = '../data/queries_ddg.txt'
    csv_file =  '../results/hw1.csv'

    # file1 = '../data/google-results.json'
    # file2 = '../results/hw1_yahoo.json'
    # query_txt_file = '../data/queries_yahoo.txt'
    # csv_file = '../results/hw1_yahoo.csv'

    # file1 = '../veer/Google_Result4.json'
    # file2 = '../veer/hw1.json'
    # query_txt_file = '../veer/100QueriesSet4.txt'
    # csv_file =  '../veer/hw1.csv'  

    calculate = Calculate()
    queries = calculate.read_txt_file(query_txt_file)
    data1, data2 = calculate.read_file(file1, file2)
    data1 = calculate.preprocess_urls(data1)
    data2 = calculate.preprocess_urls(data2)
    result_df = calculate.get_results(data1, data2, queries)
    calculate.write_csv_file(csv_file, result_df)

    # percent_overlap = calculate.percent_overlap(data1, data2)
    # print("Percent Overlap: ", percent_overlap)
    # spearman_coefficient = calculate.spearman_coefficient(data1, data2)
    # print(spearman_coefficient)

    
