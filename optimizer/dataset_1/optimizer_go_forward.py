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

# base_version_folder = "go_optimization_new/"
# base_version_folder = "go_min_baseline/"
base_version_folder = "go_random_baseline/"
data_path = "go_data_path"

# base_version = "prometheus-v0.35.0.csv"
# new_versions = ["prometheus-v0.36.0.csv","prometheus-v0.37.0.csv","prometheus-v0.38.0.csv","prometheus-v0.39.0.csv"]
# base_version = "toml-v2.0.1.csv"
# new_versions = ["toml-v2.0.2.csv","toml-v2.0.3.csv","toml-v2.0.4.csv","toml-v2.0.5.csv"]
base_version = "zap-v1.19.1.csv"
new_versions = ["zap-v1.20.0.csv","zap-v1.21.0.csv","zap-v1.22.0.csv","zap-v1.23.0.csv"]

base_version_path = base_version_folder + base_version[:-4]

list_of_instability_funcs = [(st.cv, np.mean, st.ci_bootstrap_mean_p),
                             (st.rmad, np.median, st.ci_bootstrap_median_p),
                             (st.rciw_mean_p, np.mean, st.ci_bootstrap_mean_p),
                             (st.rciw_mean_t, np.mean, st.ci_bootstrap_mean_t),
                             (st.rciw_median_p, np.median, st.ci_bootstrap_median_p),]

for file in new_versions:
    print("Processing "+file)
    # read data
    df = pd.read_csv(data_path+"/"+file, index_col="m_id")
    
    # get all benchmarks
    benchmarks = np.array(df["b_name"].drop_duplicates())
    
    # get setup variables
    bed_setup = df["bed_setup"][1]
    it_setup = df["it_setup"][1]
    sr_setup = df["sr_setup"][1]
    ir_setup = df["ir_setup"][1]
    df.drop(columns=["bed_setup", "it_setup", "sr_setup", "ir_setup"], inplace=True)
    
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
                     & (df["ir_pos"] <= 1)
                     & (df["sr_pos"] <= c[0])
                     & (df["it_pos"] <= c[1])
                     & (df["bed_pos"] <= c[2])]
            data = np.array(dft["ns_per_op"])
            
            inst = calc_inst(data, it=10000) # instability
            
            time_bound = c[0]*c[1]*c[2] # time per instance in seconds
            
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
