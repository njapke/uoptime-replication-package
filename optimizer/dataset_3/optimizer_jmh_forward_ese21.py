#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# add parent folder to module path
sys.path.append("../")

from ast import literal_eval as make_tuple
from pathlib import Path
import numpy as np
import pandas as pd
import stat_functions as st
import time

class ConfigCounter:
    def __init__(self, sr, it, bed):
        self.sr = sr
        self.it = it
        self.bed = bed
        self.max = sr*it*bed
        self.current = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.max:
            bed = self.current % self.bed
            r = self.current // self.bed
            it = r % self.it
            r = r // self.it
            sr = r % self.sr
            return (sr+1,it+1,bed+1)
        raise StopIteration

# base_version_folder = "optimizer_results_ese21/optimizer_results_only_base/"
# base_version_folder = "laaber_min_baseline_ese21/laaber_min_baseline_only_base_ese21/"
base_version_folder = "laaber_random_baseline_ese21/laaber_random_baseline_only_base_ese21/"
data_path = "optimizer_results_ese21/laaber_preprocessed_ese21/"

# base_version = "laaber_bytebuddy-01_00_00-jmh121.csv"
# new_versions = ["laaber_bytebuddy-01_00_03-jmh121.csv",
#                 "laaber_bytebuddy-01_01_00-jmh121.csv",
#                 "laaber_bytebuddy-01_01_01-jmh121.csv",
#                 "laaber_bytebuddy-01_02_00-jmh121.csv",
#                 "laaber_bytebuddy-01_02_03-jmh121.csv",
#                 "laaber_bytebuddy-01_03_00-jmh121.csv",
#                 "laaber_bytebuddy-01_03_10-jmh121.csv",
#                 "laaber_bytebuddy-01_03_20-jmh121.csv",
#                 "laaber_bytebuddy-01_04_00-jmh121.csv",
#                 "laaber_bytebuddy-01_04_11-jmh121.csv",
#                 "laaber_bytebuddy-01_04_22-jmh121.csv",
#                 "laaber_bytebuddy-01_04_33-jmh121.csv",
#                 "laaber_bytebuddy-01_05_00-jmh121.csv",
#                 "laaber_bytebuddy-01_05_07-jmh121.csv",
#                 "laaber_bytebuddy-01_05_13-jmh121.csv",
#                 "laaber_bytebuddy-01_06_00-jmh121.csv",
#                 "laaber_bytebuddy-01_06_07-jmh121.csv",
#                 "laaber_bytebuddy-01_06_14-jmh121.csv",
#                 "laaber_bytebuddy-01_07_00-jmh121.csv",
#                 "laaber_bytebuddy-01_07_06-jmh121.csv",
#                 "laaber_bytebuddy-01_07_11-jmh121.csv",
#                 "laaber_bytebuddy-01_08_00-jmh121.csv",
#                 "laaber_bytebuddy-01_08_11-jmh121.csv",
#                 "laaber_bytebuddy-01_08_22-jmh121.csv",
#                 "laaber_bytebuddy-01_09_00-jmh121.csv",
#                 "laaber_bytebuddy-01_09_08-jmh121.csv",
#                 "laaber_bytebuddy-01_09_16-jmh121.csv",
#                 "laaber_bytebuddy-01_10_00-jmh121.csv",
#                 "laaber_bytebuddy-01_10_03-jmh121.csv",
#                 "laaber_bytebuddy-01_10_07-jmh121.csv"]
# base_version = "laaber_jenetics-03_00_00-jmh121.csv"
# new_versions = ["laaber_jenetics-03_00_01-jmh121.csv",
#                 "laaber_jenetics-03_01_00-jmh121.csv",
#                 "laaber_jenetics-03_02_00-jmh121.csv",
#                 "laaber_jenetics-03_03_00-jmh121.csv",
#                 "laaber_jenetics-03_04_00-jmh121.csv",
#                 "laaber_jenetics-03_05_00-jmh121.csv",
#                 "laaber_jenetics-03_05_01-jmh121.csv",
#                 "laaber_jenetics-03_06_00-jmh121.csv",
#                 "laaber_jenetics-03_07_00-jmh121.csv",
#                 "laaber_jenetics-03_08_00-jmh121.csv",
#                 "laaber_jenetics-03_09_00-jmh121.csv",
#                 "laaber_jenetics-04_01_00-jmh121.csv",
#                 "laaber_jenetics-04_02_00-jmh121.csv",
#                 "laaber_jenetics-04_02_01-jmh121.csv",
#                 "laaber_jenetics-04_03_00-jmh121.csv",
#                 "laaber_jenetics-04_04_00-jmh121.csv",
#                 "laaber_jenetics-05_00_00-jmh121.csv",
#                 "laaber_jenetics-05_00_01-jmh121.csv",
#                 "laaber_jenetics-05_01_00-jmh121.csv",
#                 "laaber_jenetics-05_02_00-jmh121.csv"]
# base_version = "laaber_xodus-01_00_05-jmh121.csv"
# new_versions = ["laaber_xodus-01_00_06-jmh121.csv",
#                 "laaber_xodus-01_01_00-jmh121.csv",
#                 "laaber_xodus-01_02_00-jmh121.csv",
#                 "laaber_xodus-01_02_01-jmh121.csv",
#                 "laaber_xodus-01_02_02-jmh121.csv",
#                 "laaber_xodus-01_02_03-jmh121.csv",
#                 "laaber_xodus-01_03_00-jmh121.csv",
#                 "laaber_xodus-01_03_09-jmh121.csv",
#                 "laaber_xodus-01_03_23-jmh121.csv"]
base_version = "laaber_zipkin-02_00_00-jmh121.csv"
new_versions = ["laaber_zipkin-02_01_00-jmh121.csv",
                "laaber_zipkin-02_02_00-jmh121.csv",
                "laaber_zipkin-02_03_00-jmh121.csv",
                "laaber_zipkin-02_04_00-jmh121.csv",
                "laaber_zipkin-02_05_00-jmh121.csv",
                "laaber_zipkin-02_06_00-jmh121.csv",
                "laaber_zipkin-02_07_00-jmh121.csv",
                "laaber_zipkin-02_08_00-jmh121.csv",
                "laaber_zipkin-02_09_00-jmh121.csv",
                "laaber_zipkin-02_10_00-jmh121.csv",
                "laaber_zipkin-02_11_00-jmh121.csv",
                "laaber_zipkin-02_12_00-jmh121.csv",
                "laaber_zipkin-02_13_00-jmh121.csv",
                "laaber_zipkin-02_14_00-jmh121.csv",
                "laaber_zipkin-02_15_00-jmh121.csv",
                "laaber_zipkin-02_16_00-jmh121.csv",
                "laaber_zipkin-02_17_00-jmh121.csv",
                "laaber_zipkin-02_19_00-jmh121.csv",
                "laaber_zipkin-02_21_00-jmh121.csv"]

base_version_path = base_version_folder + base_version[:-4]

# list_of_instability_funcs = [(st.cv, np.mean, st.ci_bootstrap_mean_p),
#                               (st.rmad, np.median, st.ci_bootstrap_median_p),
#                               (st.rciw_mean_p, np.mean, st.ci_bootstrap_mean_p),
#                               (st.rciw_mean_t, np.mean, st.ci_bootstrap_mean_t),
#                               (st.rciw_median_p, np.median, st.ci_bootstrap_median_p),]

list_of_instability_funcs = [(st.rciw_median_p, np.median, st.ci_bootstrap_median_p)]

for file in new_versions:
    print("Processing "+file)
    # read data
    df = pd.read_csv(data_path+"/"+file, index_col="m_id")
    
    # get all benchmarks
    benchmarks = np.array(df["b_name"].drop_duplicates())
    
    # get setup variables
    it_setup = df["it_setup"][1]
    fork_setup = df["fork_setup"][1]
    df.drop(columns=["it_setup", "fork_setup"], inplace=True)
    
    for inst_funcs in list_of_instability_funcs:
        print("Using instability function setup "+str(inst_funcs))
        # Select instability measure and CI method
        calc_inst = inst_funcs[0]
        calc_avg = inst_funcs[1]
        calc_ci = inst_funcs[2]
        method_name = calc_inst.__name__+"__"+calc_avg.__name__+"__"+calc_ci.__name__
        
        bv_min = pd.read_csv(base_version_path+"/"+method_name+"/min_config_res.csv")
        bv_benchmarks = np.array(bv_min["Benchmark"])
        
        # Select threshold to mark benchmarks as unstable
        ts = 0.01

        # Time execution for min setup
        start = time.time()
        
        res = []
        # ir is always 3
        for b in range(len(benchmarks)):
            bench = benchmarks[b]
            if not np.isin(bench, bv_benchmarks):
                continue
            
            c = make_tuple(bv_min[bv_min["Benchmark"] == bench]["Config"].iloc[0])
            
            # c = ConfigCounter(bv_config[0], bv_config[1], bv_config[2]) # sr, it, bed
            dft = df[(df["b_name"] == bench)
                     & (df["fork_pos"] <= c[0])
                     & (df["it_pos"] <= c[1])]
            data = np.array(dft["ns_per_op"])
            
            inst = calc_inst(data, it=10000) # instability
            
            time_bound = c[0]*c[1] # time per instance in seconds
            
            avg = calc_avg(data)
            
            ci = calc_ci(data, it=10000)
            
            res.append([bench, c, inst, time_bound, avg, min(ci), max(ci)])
        
        result_df = pd.DataFrame(res, columns=["Benchmark","Config","Instability","Time","Average","CI Lower","CI Upper"])
        
        # create result folder
        proj_name = file[:-4]
        full_result_path = "optimizer_results/"+proj_name+"/"+method_name
        Path(full_result_path).mkdir(parents=True, exist_ok=True)
        
        # write results
        result_df.to_csv(full_result_path+"/forward_res.csv",index=False)

print("Finished")
