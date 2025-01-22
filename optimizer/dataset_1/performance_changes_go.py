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

full_path = "go_optimization_new/"
min_path = "go_optimization_forward"
# full_path = "go_min_baseline/"
# min_path = "go_min_baseline_forward"
# full_path = "go_random_baseline/"
# min_path = "go_random_baseline_forward"

# versions = ["prometheus-v0.35.0","prometheus-v0.36.0","prometheus-v0.37.0","prometheus-v0.38.0","prometheus-v0.39.0"]
# versions = ["toml-v2.0.1","toml-v2.0.2","toml-v2.0.3","toml-v2.0.4","toml-v2.0.5"]
versions = ["zap-v1.19.1","zap-v1.20.0","zap-v1.21.0","zap-v1.22.0","zap-v1.23.0"]

method_name = "rmad__median__ci_bootstrap_median_p"

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


