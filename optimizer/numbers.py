#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:07:53 2024

@author: njapke
"""

import os
import numpy as np
import pandas as pd

base_path = "optimizer/dataset_1/go_optimization_new/"


# optimization
go_data_path = "dataset_1/go_optimization_new"
java_data_path_set2 = "dataset_2/laaber_optimization_nowarmup_fse20"
java_data_path_set3 = "dataset_3/optimizer_results_ese21/optimizer_results_only_latest"

# min baseline
# go_data_path = "dataset_1/go_min_baseline"
# java_data_path_set2 = "dataset_2/laaber_min_baseline_nowarmup_fse20"
# java_data_path_set3 = "dataset_3/laaber_min_baseline_ese21/laaber_min_baseline_only_latest_ese21"

# random baseline
# go_data_path = "dataset_1/go_random_baseline"
# java_data_path_set2 = "dataset_2/laaber_random_baseline_nowarmup_fse20"
# java_data_path_set3 = "dataset_3/laaber_random_baseline_ese21/laaber_random_baseline_only_latest_ese21"


### GO PROJECTS ###
go_projects = ["prometheus-v0.39.0","toml-v2.0.5","zap-v1.23.0"]
go_projects.sort()

# read in go data
go_optimization_quality = []
for project in go_projects:
    data_path = go_data_path+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    print("Begin reading "+project)
    if len(go_optimization_quality) == 0:
        go_optimization_quality = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        go_optimization_quality = pd.concat([go_optimization_quality, new_df])

list_of_go_projects = list(np.array(go_optimization_quality["Project"].drop_duplicates()))
L_go = len(list_of_go_projects)


### JAVA PROJECTS ###
# get sorted list of all folders
java_projects_set2 = list(os.walk(java_data_path_set2))[0][1]
java_projects_set2.sort()

# read in java data from set 2
java_optimization_quality_set2 = []
for project in java_projects_set2:
    data_path = java_data_path_set2+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    print("Begin reading "+project)
    if len(java_optimization_quality_set2) == 0:
        java_optimization_quality_set2 = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        java_optimization_quality_set2 = pd.concat([java_optimization_quality_set2, new_df])

list_of_java_projects_set2 = list(np.array(java_optimization_quality_set2["Project"].drop_duplicates()))
L_java_set2 = len(list_of_java_projects_set2)

# read in java data from set 3
java_projects_set3 = list(os.walk(java_data_path_set3))[0][1]
java_projects_set3.sort()

java_optimization_quality_set3 = []
for project in java_projects_set3:
    data_path = java_data_path_set3+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    print("Begin reading "+project)
    if len(java_optimization_quality_set3) == 0:
        java_optimization_quality_set3 = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        java_optimization_quality_set3 = pd.concat([java_optimization_quality_set3, new_df])

list_of_java_projects_set3 = list(np.array(java_optimization_quality_set3["Project"].drop_duplicates()))
L_java_set3 = len(list_of_java_projects_set3)


## calculate results
# filter data
# go_optimization_quality = go_optimization_quality[(go_optimization_quality["Fraction of leq 0.03 change"] >= 0.8)]
# java_optimization_quality_set2 = java_optimization_quality_set2[(java_optimization_quality_set2["Fraction of leq 0.03 change"] >= 0.8)]
# java_optimization_quality_set3 = java_optimization_quality_set3[(java_optimization_quality_set3["Fraction of leq 0.03 change"] >= 0.8)]

# java_optimization_quality_set3 = java_optimization_quality_set3[(java_optimization_quality_set3["Method"] == "cv__mean__ci_bootstrap_mean_p") | (java_optimization_quality_set3["Method"] == "rmad__median__ci_bootstrap_median_p")]

