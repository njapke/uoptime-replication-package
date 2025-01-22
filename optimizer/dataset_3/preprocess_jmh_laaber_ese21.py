#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import pandas as pd

# paths (edit accordingly)
data_laaber = "/path/to/replication_package_testcaseprio/data/executions"

# iterate over all folders by christoph
subdirs = next(os.walk(data_laaber))[1]
for sd in subdirs:
    if sd != "netty" and sd != "RxJava": # TODO: hack until finished
        continue
    print(f"Beginning to process {sd}...")
    json_path = os.path.join(data_laaber, sd, "results/json")
    
    files = list(os.walk(json_path))[0][2]
    files.sort()
    files = list(filter(lambda f: f[-4:] == "json", files))
    
    fork_setup = 3
    
    borked = False
    for kk in range(len(files) // fork_setup):
        k = kk*fork_setup
        proj_name = files[k][:-7] # removes -1.json from filename
        
        print(f"Read {files[k]}, {files[k+1]} and {files[k+2]} into laaber_{proj_name}.csv")
        
        df = pd.DataFrame(columns=["n","ns_per_op","it_setup","fork_setup","it_pos","fork_pos","b_name"])
        
        for fork in range(fork_setup):
            file_path = os.path.join(json_path, files[k+fork])
            print(f"Read {files[k+fork]}")
            fork_no = fork + 1
            
            with open(file_path) as f:
                try:
                    j = json.load(f)
                except json.JSONDecodeError:
                    borked = True
                    break
                # skip empty json
                if len(j) == 0:
                    continue
                # bench_name = file[:-5] # removes .json from filename
                
                for bench in j:
                    bench_name = bench["benchmark"]
                    
                    # process data
                    data_j = bench["primaryMetric"]["rawDataHistogram"]
                    score_unit = bench["primaryMetric"]["scoreUnit"]
                    unit_conv = 1
                    if score_unit == "us/op":
                        unit_conv = 1e3
                    elif score_unit == "ms/op":
                        unit_conv = 1e6
                    elif score_unit == "s/op":
                        unit_conv = 1e9
                    it_setup = bench["measurementIterations"]
                    
                    it_no = 1
                    for it in data_j[0]:
                        it_arr = np.array(it)
                        weighted_sum = (it_arr[:,0]*it_arr[:,1]).sum()
                        N = it_arr[:,1].sum()
                        m = weighted_sum / N
                        df = pd.concat([df, pd.DataFrame([[N,m*unit_conv,it_setup,fork_setup,it_no,fork_no,bench_name]], columns=df.columns)], ignore_index=True)
                        it_no = it_no + 1
        if borked:
            borked = False
            continue

        df.index.name = "m_id"
        # df.to_csv("laaber_preprocessed_ese21/laaber_" + proj_name + ".csv")
        df.to_csv("tmp/laaber_" + proj_name + ".csv")
