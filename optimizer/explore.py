#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

base_path = "optimizer/dataset_1/go_optimization_new/"


go_data_path = "dataset_1/go_optimization_new"
java_nowarmup_data_path = "dataset_2/laaber_optimization_nowarmup_fse20"
java_warmup_data_path = "dataset_2/laaber_optimization_warmup_fse20"


### GO PROJECTS ###
go_projects = ["prometheus-v0.39.0","toml-v2.0.5","zap-v1.23.0"]
go_projects.sort()

# read in go data
go_optimization_quality = []
go_reduction_map = {}
for project in go_projects:
    data_path = go_data_path+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    go_reduction_map[project] = {}
    print("Begin reading "+project)
    for folder in folders:
        df = pd.read_csv(data_path+"/"+folder+"/min_config_res.csv")
        dft = df[df["Config"] == "(3, 5, 5)"]
        go_reduction_map[project][folder] = len(dft["Benchmark"])
        print(folder+": "+str(go_reduction_map[project][folder])+" not reduced")
    
    if len(go_optimization_quality) == 0:
        go_optimization_quality = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        go_optimization_quality = pd.concat([go_optimization_quality, new_df])

list_of_go_projects = list(np.array(go_optimization_quality["Project"].drop_duplicates()))
L_go = len(list_of_go_projects)


### JAVA PROJECTS NO WARMUP ###
# get sorted list of all folders
java_nowarmup_projects = list(os.walk(java_nowarmup_data_path))[0][1]
java_nowarmup_projects.sort()

# read in java data
java_nowarmup_optimization_quality = []
java_nowarmup_reduction_map = {}
for project in java_nowarmup_projects:
    data_path = java_nowarmup_data_path+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    java_nowarmup_reduction_map[project] = {}
    print("Begin reading "+project)
    for folder in folders:
        df = pd.read_csv(data_path+"/"+folder+"/min_config_res.csv")
        dft = df[df["Config"] == "(5, 100)"]
        java_nowarmup_reduction_map[project][folder] = len(dft["Benchmark"])
        print(folder+": "+str(java_nowarmup_reduction_map[project][folder])+" not reduced")
    
    if len(java_nowarmup_optimization_quality) == 0:
        java_nowarmup_optimization_quality = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        java_nowarmup_optimization_quality = pd.concat([java_nowarmup_optimization_quality, new_df])

list_of_java_projects = list(np.array(java_nowarmup_optimization_quality["Project"].drop_duplicates()))
L_java = len(list_of_java_projects)


### JAVA PROJECTS WARMUP ###
# get sorted list of all folders
java_warmup_projects = list(os.walk(java_warmup_data_path))[0][1]
java_warmup_projects.sort()

# read in java data
java_warmup_optimization_quality = []
java_warmup_reduction_map = {}
for project in java_warmup_projects:
    data_path = java_warmup_data_path+"/"+project
    
    java_warmup_reduction_map[project] = {}
    print("Begin reading "+project)
    for folder in folders:
        df = pd.read_csv(data_path+"/"+folder+"/min_config_res.csv")
        dft = df[df["Config"] == "(5, 50)"]
        java_warmup_reduction_map[project][folder] = len(dft["Benchmark"])
        print(folder+": "+str(java_warmup_reduction_map[project][folder])+" not reduced")
    
    if len(java_warmup_optimization_quality) == 0:
        java_warmup_optimization_quality = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        java_warmup_optimization_quality = pd.concat([java_warmup_optimization_quality, new_df])

#%%
java_projs = java_warmup_optimization_quality[java_warmup_optimization_quality["Method"] == "rciw_median_p__median__ci_bootstrap_median_p"]

max_m = np.array(java_projs["Max Time in s"])
max_w = np.array(java_projs["Max Warmup in s"])

min_m = np.array(java_projs["Min Time in s"])
min_w = np.array(java_projs["Min Warmup in s"])

saved_overall = (max_m + max_w) - (min_m + min_w)
saved_overall_p = saved_overall / (max_m + max_w)
saved_overall_h = saved_overall / 60 / 60




