#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import numpy as np
import pandas as pd

data_path = "/path/to/this/folder/"
in_folder = "laaber_preprocessed_ese21"
out_folder = "laaber_preprocessed_ese21_filtered"
Path(data_path+out_folder).mkdir(parents=True, exist_ok=True)

# get sorted list of all files
files = list(os.walk(data_path+in_folder))[0][2]
files.sort()

for file in files:
    # skip non-csv files
    if file[-4:] != ".csv":
        continue
    
    print("Processing "+file)
    # read data
    df = pd.read_csv(data_path+in_folder+"/"+file, index_col="m_id")
    
    # get all benchmarks
    benchmarks = np.array(df["b_name"].drop_duplicates())
    
    # get setup variables
    it_setup = df["it_setup"][1]
    fork_setup = df["fork_setup"][1]
    df.drop(columns=["it_setup", "fork_setup"], inplace=True)
    
    borked_list = []
    for b in range(len(benchmarks)):
        bench = benchmarks[b]
        dft = df[(df["b_name"] == bench)]
        data = np.array(dft["ns_per_op"])
        if len(data) != 60:
            print("Warning for {}".format(bench))
            borked_list.append(bench)
    if len(borked_list) > 0:
        borked_filter = df["b_name"].isin(borked_list)
        cleaned_df = df[~borked_filter]
        cleaned_df.to_csv(data_path+out_folder+"/"+file)
        
