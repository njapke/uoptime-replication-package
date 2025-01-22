#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import numpy as np
import pandas as pd
import stat_functions as st
import time
import tqdm
import multiprocessing as mp
import functools

class ConfigCounter:
    def __init__(self, fork, it):
        self.fork = fork
        self.it = it
        self.max = fork*it
        self.current = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.max:
            it = self.current % self.it
            r = self.current // self.it
            fork = r % self.fork
            return (fork+1,it+1)
        raise StopIteration

data_path = "laaber_preprocessed_ese21"

# get sorted list of all files
files = list(os.walk(data_path))[0][2]
files.sort()

list_of_instability_funcs = [(st.cv, np.mean, st.ci_bootstrap_mean_p),
                              (st.cv, np.median, st.ci_bootstrap_median_p),
                              (st.rmad, np.mean, st.ci_bootstrap_mean_p),
                              (st.rmad, np.median, st.ci_bootstrap_median_p),
                              (st.rciw_mean_p, np.mean, st.ci_bootstrap_mean_p),
                              (st.rciw_mean_t, np.mean, st.ci_bootstrap_mean_t),
                              (st.rciw_median_p, np.median, st.ci_bootstrap_median_p),]

exec_times = []
for file in files:
    print("Processing "+file)
    # read data
    df = pd.read_csv(data_path+"/"+file, index_col="m_id")
    
    # get all benchmarks
    benchmarks = np.array(df["b_name"].drop_duplicates())
    
    # get setup variables
    it_setup = df["it_setup"][1]
    fork_setup = df["fork_setup"][1]
    df.drop(columns=["it_setup", "fork_setup"], inplace=True)
    
    for bench in benchmarks:
        dat = df[df["b_name"] == bench]
        if len(np.array(dat["ns_per_op"])) == 0:
            print(file + ": " + bench + " is empty")
    
    for inst_funcs in list_of_instability_funcs:
        print("Using instability function setup "+str(inst_funcs))
        # Select instability measure and CI method
        calc_inst = inst_funcs[0]
        calc_avg = inst_funcs[1]
        calc_ci = inst_funcs[2]
        
        # Select threshold to mark benchmarks as unstable
        ts = 0.01
        
        # Time execution for min setup
        start = time.time()
        
        # res = []
        # for bench in benchmarks:
        def great_func(bench, df):
            _res = []
            dft = df[(df["b_name"] == bench)
                      & (df["fork_pos"] <= fork_setup)
                      & (df["it_pos"] <= it_setup)]
            data = np.array(dft["ns_per_op"])
            
            inst = calc_inst(data, it=10000) # instability
            
            time_bound = fork_setup*it_setup # time per instance in seconds
            
            avg = calc_avg(data)
            
            ci = calc_ci(data, it=10000)
            
            _res.append([bench, (fork_setup,it_setup), inst, time_bound, avg, min(ci), max(ci)])
                
            return _res
        
        # res = [great_func(x) for x in bench]
        with mp.Pool() as pool:
            res = list(tqdm.tqdm(pool.imap_unordered(functools.partial(great_func, df=df), benchmarks, chunksize=10), total=len(benchmarks)))
    
            pool.close()
            pool.join()
        
        # flatten
        res = [item for sublist in res for item in sublist]
        result_df = pd.DataFrame(res, columns=["Benchmark","Config","Instability","Time","Average","CI Lower","CI Upper"])
        
        reduced_res = result_df[result_df["Instability"] < ts]
        
        full_config_res = result_df[result_df["Config"] == (fork_setup,it_setup)]
        
        # Print execution time
        end = time.time()
        curr_exec_time = end - start
        print("Finished after "+str(curr_exec_time)+" seconds")
        exec_times.append([file, inst_funcs, curr_exec_time])
        
        # create result folder
        proj_name = file[:-4]
        method_name = calc_inst.__name__+"__"+calc_avg.__name__+"__"+calc_ci.__name__
        full_result_path = "optimizer_results/"+proj_name+"/"+method_name
        # full_result_path = "tmp/opt/"+proj_name+"/"+method_name
        Path(full_result_path).mkdir(parents=True, exist_ok=True)
        
        # write results
        full_config_res.to_csv(full_result_path+"/full_config_res.csv",index=False)

# exec_times_df = pd.DataFrame(exec_times, columns=["File","Instability Functions","Execution Time"])
# exec_times_df.to_csv("optimizer_results/exec_times_df.csv",index=False)
print("Finished")
