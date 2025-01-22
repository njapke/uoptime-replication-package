#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:21:46 2023

@author: njapke
"""

import numpy as np
import pandas as pd

# Intersection for intervals
def intersect(i1, i2):
    min1 = min(i1)
    max1 = max(i1)
    min2 = min(i2)
    max2 = max(i2)
    
    higher_min = max(min1, min2)
    lower_max = min(max1, max2)
    
    length_inner = abs(lower_max - higher_min) if higher_min < lower_max else 0
    
    return length_inner

full_path = "optimizer_results_ese21/results_only_full/"
min_path = "optimizer_results_forward_ese21/"

bytebuddy = ["laaber_bytebuddy-01_00_00-jmh121",
    "laaber_bytebuddy-01_00_03-jmh121",
    "laaber_bytebuddy-01_01_00-jmh121",
    "laaber_bytebuddy-01_01_01-jmh121",
    "laaber_bytebuddy-01_02_00-jmh121",
    "laaber_bytebuddy-01_02_03-jmh121",
    "laaber_bytebuddy-01_03_00-jmh121",
    "laaber_bytebuddy-01_03_10-jmh121",
    "laaber_bytebuddy-01_03_20-jmh121",
    "laaber_bytebuddy-01_04_00-jmh121",
    "laaber_bytebuddy-01_04_11-jmh121",
    "laaber_bytebuddy-01_04_22-jmh121",
    "laaber_bytebuddy-01_04_33-jmh121",
    "laaber_bytebuddy-01_05_00-jmh121",
    "laaber_bytebuddy-01_05_07-jmh121",
    "laaber_bytebuddy-01_05_13-jmh121",
    "laaber_bytebuddy-01_06_00-jmh121",
    "laaber_bytebuddy-01_06_07-jmh121",
    "laaber_bytebuddy-01_06_14-jmh121",
    "laaber_bytebuddy-01_07_00-jmh121",
    "laaber_bytebuddy-01_07_06-jmh121",
    "laaber_bytebuddy-01_07_11-jmh121",
    "laaber_bytebuddy-01_08_00-jmh121",
    "laaber_bytebuddy-01_08_11-jmh121",
    "laaber_bytebuddy-01_08_22-jmh121",
    "laaber_bytebuddy-01_09_00-jmh121",
    "laaber_bytebuddy-01_09_08-jmh121",
    "laaber_bytebuddy-01_09_16-jmh121",
    "laaber_bytebuddy-01_10_00-jmh121",
    "laaber_bytebuddy-01_10_03-jmh121",
    "laaber_bytebuddy-01_10_07-jmh121"]
jenetics = ["laaber_jenetics-03_00_00-jmh121",
    "laaber_jenetics-03_00_01-jmh121",
    "laaber_jenetics-03_01_00-jmh121",
    "laaber_jenetics-03_02_00-jmh121",
    "laaber_jenetics-03_03_00-jmh121",
    "laaber_jenetics-03_04_00-jmh121",
    "laaber_jenetics-03_05_00-jmh121",
    "laaber_jenetics-03_05_01-jmh121",
    "laaber_jenetics-03_06_00-jmh121",
    "laaber_jenetics-03_07_00-jmh121",
    "laaber_jenetics-03_08_00-jmh121",
    "laaber_jenetics-03_09_00-jmh121",
    "laaber_jenetics-04_01_00-jmh121",
    "laaber_jenetics-04_02_00-jmh121",
    "laaber_jenetics-04_02_01-jmh121",
    "laaber_jenetics-04_03_00-jmh121",
    "laaber_jenetics-04_04_00-jmh121",
    "laaber_jenetics-05_00_00-jmh121",
    "laaber_jenetics-05_00_01-jmh121",
    "laaber_jenetics-05_01_00-jmh121",
    "laaber_jenetics-05_02_00-jmh121"]
xodus = ["laaber_xodus-01_00_05-jmh121",
    "laaber_xodus-01_00_06-jmh121",
    "laaber_xodus-01_01_00-jmh121",
    "laaber_xodus-01_02_00-jmh121",
    "laaber_xodus-01_02_01-jmh121",
    "laaber_xodus-01_02_02-jmh121",
    "laaber_xodus-01_02_03-jmh121",
    "laaber_xodus-01_03_00-jmh121",
    "laaber_xodus-01_03_09-jmh121",
    "laaber_xodus-01_03_23-jmh121"]
zipkin = ["laaber_zipkin-02_00_00-jmh121",
    "laaber_zipkin-02_01_00-jmh121",
    "laaber_zipkin-02_02_00-jmh121",
    "laaber_zipkin-02_03_00-jmh121",
    "laaber_zipkin-02_04_00-jmh121",
    "laaber_zipkin-02_05_00-jmh121",
    "laaber_zipkin-02_06_00-jmh121",
    "laaber_zipkin-02_07_00-jmh121",
    "laaber_zipkin-02_08_00-jmh121",
    "laaber_zipkin-02_09_00-jmh121",
    "laaber_zipkin-02_10_00-jmh121",
    "laaber_zipkin-02_11_00-jmh121",
    "laaber_zipkin-02_12_00-jmh121",
    "laaber_zipkin-02_13_00-jmh121",
    "laaber_zipkin-02_14_00-jmh121",
    "laaber_zipkin-02_15_00-jmh121",
    "laaber_zipkin-02_16_00-jmh121",
    "laaber_zipkin-02_17_00-jmh121",
    "laaber_zipkin-02_19_00-jmh121",
    "laaber_zipkin-02_21_00-jmh121"]

projects = {"bytebuddy" : bytebuddy, "jenetics" : jenetics, "xodus":  xodus, "zipkin" : zipkin}
method_name = "rciw_median_p__median__ci_bootstrap_median_p"

res = []
for p in projects.keys():
    count = []
    for v in projects[p]:
        
        df = pd.read_csv(full_path+"/"+v+"/"+method_name+"/full_config_res.csv")
        count.append(len(df))
    res.append((p, min(count), max(count)))
    
