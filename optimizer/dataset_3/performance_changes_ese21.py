#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
# full_path = "laaber_min_baseline_ese21/laaber_min_baseline_all_ese21/"
# min_path = "laaber_min_baseline_forward_ese21/"
# full_path = "laaber_random_baseline_ese21/laaber_random_baseline_all_ese21/"
# min_path = "laaber_random_baseline_forward_ese21/"

# versions = ["laaber_bytebuddy-01_00_00-jmh121",
#     "laaber_bytebuddy-01_00_03-jmh121",
#     "laaber_bytebuddy-01_01_00-jmh121",
#     "laaber_bytebuddy-01_01_01-jmh121",
#     "laaber_bytebuddy-01_02_00-jmh121",
#     "laaber_bytebuddy-01_02_03-jmh121",
#     "laaber_bytebuddy-01_03_00-jmh121",
#     "laaber_bytebuddy-01_03_10-jmh121",
#     "laaber_bytebuddy-01_03_20-jmh121",
#     "laaber_bytebuddy-01_04_00-jmh121",
#     "laaber_bytebuddy-01_04_11-jmh121",
#     "laaber_bytebuddy-01_04_22-jmh121",
#     "laaber_bytebuddy-01_04_33-jmh121",
#     "laaber_bytebuddy-01_05_00-jmh121",
#     "laaber_bytebuddy-01_05_07-jmh121",
#     "laaber_bytebuddy-01_05_13-jmh121",
#     "laaber_bytebuddy-01_06_00-jmh121",
#     "laaber_bytebuddy-01_06_07-jmh121",
#     "laaber_bytebuddy-01_06_14-jmh121",
#     "laaber_bytebuddy-01_07_00-jmh121",
#     "laaber_bytebuddy-01_07_06-jmh121",
#     "laaber_bytebuddy-01_07_11-jmh121",
#     "laaber_bytebuddy-01_08_00-jmh121",
#     "laaber_bytebuddy-01_08_11-jmh121",
#     "laaber_bytebuddy-01_08_22-jmh121",
#     "laaber_bytebuddy-01_09_00-jmh121",
#     "laaber_bytebuddy-01_09_08-jmh121",
#     "laaber_bytebuddy-01_09_16-jmh121",
#     "laaber_bytebuddy-01_10_00-jmh121",
#     "laaber_bytebuddy-01_10_03-jmh121",
#     "laaber_bytebuddy-01_10_07-jmh121"]
# versions = ["laaber_jenetics-03_00_00-jmh121",
#     "laaber_jenetics-03_00_01-jmh121",
#     "laaber_jenetics-03_01_00-jmh121",
#     "laaber_jenetics-03_02_00-jmh121",
#     "laaber_jenetics-03_03_00-jmh121",
#     "laaber_jenetics-03_04_00-jmh121",
#     "laaber_jenetics-03_05_00-jmh121",
#     "laaber_jenetics-03_05_01-jmh121",
#     "laaber_jenetics-03_06_00-jmh121",
#     "laaber_jenetics-03_07_00-jmh121",
#     "laaber_jenetics-03_08_00-jmh121",
#     "laaber_jenetics-03_09_00-jmh121",
#     "laaber_jenetics-04_01_00-jmh121",
#     "laaber_jenetics-04_02_00-jmh121",
#     "laaber_jenetics-04_02_01-jmh121",
#     "laaber_jenetics-04_03_00-jmh121",
#     "laaber_jenetics-04_04_00-jmh121",
#     "laaber_jenetics-05_00_00-jmh121",
#     "laaber_jenetics-05_00_01-jmh121",
#     "laaber_jenetics-05_01_00-jmh121",
#     "laaber_jenetics-05_02_00-jmh121"]
# versions = ["laaber_xodus-01_00_05-jmh121",
#     "laaber_xodus-01_00_06-jmh121",
#     "laaber_xodus-01_01_00-jmh121",
#     "laaber_xodus-01_02_00-jmh121",
#     "laaber_xodus-01_02_01-jmh121",
#     "laaber_xodus-01_02_02-jmh121",
#     "laaber_xodus-01_02_03-jmh121",
#     "laaber_xodus-01_03_00-jmh121",
#     "laaber_xodus-01_03_09-jmh121",
#     "laaber_xodus-01_03_23-jmh121"]
versions = ["laaber_zipkin-02_00_00-jmh121",
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

method_name = "rciw_median_p__median__ci_bootstrap_median_p"

res = []
for i in range(len(versions) - 1):
    v1 = versions[i]
    v2 = versions[i+1]
    
    full_v1 = pd.read_csv(full_path+"/"+v1+"/"+method_name+"/full_config_res.csv")
    full_v2 = pd.read_csv(full_path+"/"+v2+"/"+method_name+"/full_config_res.csv")
    
    min_v1 = pd.read_csv(min_path+"/"+v1+"/"+method_name+"/forward_res.csv")
    min_v2 = pd.read_csv(min_path+"/"+v2+"/"+method_name+"/forward_res.csv")
    
    b_full_v1 = np.array(full_v1["Benchmark"].drop_duplicates())
    b_full_v2 = np.array(full_v2["Benchmark"].drop_duplicates())
    b_full_int = np.intersect1d(b_full_v1,b_full_v2)
    
    b_min_v1 = np.array(min_v1["Benchmark"].drop_duplicates())
    b_min_v2 = np.array(min_v2["Benchmark"].drop_duplicates())
    b_min_int = np.intersect1d(b_min_v1,b_min_v2)
    
    benchmarks = np.intersect1d(b_full_int,b_min_int)
    
    full_perf_changes = 0
    min_perf_changes = 0
    false_pos = 0
    false_neg = 0
    true_pos = 0
    true_neg = 0
    for b in benchmarks:
        bench_full_v1 = full_v1[full_v1["Benchmark"] == b]
        bench_full_v2 = full_v2[full_v2["Benchmark"] == b]
        
        bench_min_v1 = min_v1[min_v1["Benchmark"] == b]
        bench_min_v2 = min_v2[min_v2["Benchmark"] == b]
        
        # more than 3% performance change (relevant perf change)
        cr_full = (bench_full_v2["Average"].iloc[0] - bench_full_v1["Average"].iloc[0]) / bench_full_v1["Average"].iloc[0]
        cr_min = (bench_min_v2["Average"].iloc[0] - bench_min_v1["Average"].iloc[0]) / bench_min_v1["Average"].iloc[0]
        
        # overlapping confidence intervals
        int_full = intersect([bench_full_v1["CI Lower"].iloc[0], bench_full_v1["CI Upper"].iloc[0]], [bench_full_v2["CI Lower"].iloc[0], bench_full_v2["CI Upper"].iloc[0]])
        int_min = intersect([bench_min_v1["CI Lower"].iloc[0], bench_min_v1["CI Upper"].iloc[0]], [bench_min_v2["CI Lower"].iloc[0], bench_min_v2["CI Upper"].iloc[0]])
        
        full_perf_change_detected = cr_full > 0.03 and int_full <= 0
        min_perf_change_detected = cr_min > 0.03 and int_min <= 0
        
        if full_perf_change_detected:
            full_perf_changes = full_perf_changes + 1
        if min_perf_change_detected:
            min_perf_changes = min_perf_changes + 1
        if full_perf_change_detected and not min_perf_change_detected:
            false_neg = false_neg + 1
        if not full_perf_change_detected and min_perf_change_detected:
            false_pos = false_pos + 1
        if full_perf_change_detected and min_perf_change_detected:
            true_pos = true_pos + 1
        if not full_perf_change_detected and not min_perf_change_detected:
            true_neg = true_neg + 1
    
    N_FPR = false_pos + true_neg
    if N_FPR > 0:
        FPR = false_pos / N_FPR
    else:
        FPR = 0
    
    N_FNR = false_neg + true_pos
    if N_FNR > 0:
        FNR = false_neg / N_FNR
    else:
        FNR = 0
    
    res.append([v1, v2, len(benchmarks), full_perf_changes, min_perf_changes, false_pos, false_neg, true_pos, true_neg, FPR, FNR])

result_df = pd.DataFrame(res, columns=["v1","v2","No of Benchmark","Full Perf Changes","Min Perf Changes","False Positives","False Negatives","True Positives","True Negatives","FPR","FNR"])

print(np.sum(result_df["Full Perf Changes"]))
print(np.sum(result_df["Min Perf Changes"]))
print(result_df["FPR"].quantile([0,0.5,1]))
print(result_df["FNR"].quantile([0,0.5,1]))

