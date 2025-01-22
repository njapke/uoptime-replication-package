#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from matplotlib import rcParams

#plt.style.use("seaborn-v0_8")

# reset kernel, when editing other figures
rcParams["lines.markersize"] = 6.0 # default is 6.0
rcParams["font.size"] = 13.0 # default is 10.0

method_map = {"cv__mean__ci_bootstrap_mean_p":"Mean (CV)",
              "cv__median__ci_bootstrap_median_p":"Median (CV)",
              "rciw_mean_p__mean__ci_bootstrap_mean_p": "Mean (RCIW_1)",
              "rciw_mean_t__mean__ci_bootstrap_mean_t":"Mean (RCIW_2)",
              "rciw_median_p__median__ci_bootstrap_median_p":"Median (RCIW_3)",
              "rmad__mean__ci_bootstrap_mean_p":"Mean (RMAD)",
              "rmad__median__ci_bootstrap_median_p":"Median (RMAD)"}

go_project_map = {"prometheus-v0.39.0" : "G$_1$",
                  "toml-v2.0.5" : "G$_2$",
                  "zap-v1.23.0" : "G$_3$"}

java_project_map = {"laaber_byte-buddy" : "J$_1$",
                    "laaber_jctools" : "J$_2$",
                    "laaber_jenetics" : "J$_3$",
                    "laaber_jmh-core-benchmarks" : "J$_4$",
                    "laaber_jmh-jdk-microbenchmarks" : "J$_5$",
                    "laaber_log4j2" : "J$_6$",
                    "laaber_protostuff" : "J$_7$",
                    "laaber_rxjava" : "J$_8$",
                    "laaber_squidlib" : "J$_9$",
                    "laaber_zipkin" : "J$_{10}$",
                    "laaber_bytebuddy-01_10_07-jmh121" : "J$_{11}$",
                    "laaber_jenetics-05_02_00-jmh121" : "J$_{12}$",
                    "laaber_xodus-01_03_23-jmh121" : "J$_{13}$",
                    "laaber_zipkin-02_21_00-jmh121" : "J$_{14}$"}

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

L_all = L_go + L_java_set2 + L_java_set3


# plot variables
max_time_color = "#cccccc"
min_time_color = "#969696"
leq001_color = "#525252"
leq003_color = "#525252"
leq005_color = "#525252"



# create each figure
for i in range(5):
    # GridSpec for facets
    fig = plt.figure()
    
    # prepare iteration
    if i == 0:
        go_projs = go_optimization_quality[go_optimization_quality["Method"] == "cv__mean__ci_bootstrap_mean_p"]
        java_projs_set2 = java_optimization_quality_set2[java_optimization_quality_set2["Method"] == "cv__mean__ci_bootstrap_mean_p"]
        java_projs_set3 = java_optimization_quality_set3[java_optimization_quality_set3["Method"] == "cv__mean__ci_bootstrap_mean_p"]
        fig.suptitle("CV")
    elif i == 1:
        go_projs = go_optimization_quality[go_optimization_quality["Method"] == "rmad__median__ci_bootstrap_median_p"]
        java_projs_set2 = java_optimization_quality_set2[java_optimization_quality_set2["Method"] == "rmad__median__ci_bootstrap_median_p"]
        java_projs_set3 = java_optimization_quality_set3[java_optimization_quality_set3["Method"] == "rmad__median__ci_bootstrap_median_p"]
        fig.suptitle("RMAD")
    elif i == 2:
        go_projs = go_optimization_quality[go_optimization_quality["Method"] == "rciw_mean_p__mean__ci_bootstrap_mean_p"]
        java_projs_set2 = java_optimization_quality_set2[java_optimization_quality_set2["Method"] == "rciw_mean_p__mean__ci_bootstrap_mean_p"]
        java_projs_set3 = java_optimization_quality_set3[java_optimization_quality_set3["Method"] == "rciw_mean_p__mean__ci_bootstrap_mean_p"]
        fig.suptitle("RCIW$_1$")
    elif i == 3:
        go_projs = go_optimization_quality[go_optimization_quality["Method"] == "rciw_mean_t__mean__ci_bootstrap_mean_t"]
        java_projs_set2 = java_optimization_quality_set2[java_optimization_quality_set2["Method"] == "rciw_mean_t__mean__ci_bootstrap_mean_t"]
        java_projs_set3 = java_optimization_quality_set3[java_optimization_quality_set3["Method"] == "rciw_mean_t__mean__ci_bootstrap_mean_t"]
        fig.suptitle("RCIW$_2$")
    elif i == 4:
        go_projs = go_optimization_quality[go_optimization_quality["Method"] == "rciw_median_p__median__ci_bootstrap_median_p"]
        java_projs_set2 = java_optimization_quality_set2[java_optimization_quality_set2["Method"] == "rciw_median_p__median__ci_bootstrap_median_p"]
        java_projs_set3 = java_optimization_quality_set3[java_optimization_quality_set3["Method"] == "rciw_median_p__median__ci_bootstrap_median_p"]
        fig.suptitle("RCIW$_3$")
    
    # GridSpec for facets
    inner = gs.GridSpec(1, 3, wspace=0.4, hspace=0.1, width_ratios=[L_go/L_all,L_java_set2/L_all,L_java_set3/L_all])
    
    # initialize go subplot
    ax1 = plt.Subplot(fig, inner[0])
    
    # setup title, ticks, limits, labels
    ax1.set_title("Data Set 1 (Go)")
    # ax1.set_xticks(range(L_go), list_of_go_projects, rotation="vertical")
    ax1.set_xticks(range(L_go), [go_project_map[x] for x in list_of_go_projects])
    ax1.set_xlim(-0.5, L_go-0.5)
    ax1.set_ylim(0, max(go_projs["Max Time in h"]) * 1.1)
    # ax1.set_yscale("log")
    # ax1.set_ylim(0, max(java_projs["Max Time in h"]) + 0.1)
    ax1.set_ylabel("execution time (h)")
    
    # plot bars
    l1 = ax1.bar(range(L_go), go_projs["Max Time in h"], color=max_time_color, label="execution time (full config.)")
    l2 = ax1.bar(range(L_go), go_projs["Min Time in h"], color=min_time_color, label="execution time (min. config.)")
    fig.add_subplot(ax1)
    
    # twin x and quality marks (only works when plotted on twin after original is added to figure)
    ax1t = ax1.twinx()
    ax1t.set_ylim(0,1.05)
    ax1t.set_yticks([])
    # ax1t.set_ylabel("fraction of microbenchmarks (x marks)")
    
    l3 = ax1t.scatter(np.array(range(L_go)) - 0.25, go_projs["Fraction of leq 0.01 change"], marker="x", color=leq001_color, label="fraction of MBs with 1% change")
    l4 = ax1t.scatter(np.array(range(L_go)), go_projs["Fraction of leq 0.03 change"], marker="o", facecolor="none", edgecolor=leq003_color, label="fraction of MBs with 3% change")
    l5 = ax1t.scatter(np.array(range(L_go)) + 0.25, go_projs["Fraction of leq 0.05 change"], marker="v", facecolor="none", edgecolor=leq005_color, label="fraction of MBs with 5% change")
    
    # initialize java subplot for data set 2
    ax2 = plt.Subplot(fig, inner[1])
    
    # setup title, ticks, limits, labels
    ax2.set_title("Data Set 2 (Java)")
    # ax2.set_xticks(range(L_java_set2), list_of_java_projects_set2, rotation="vertical")
    ax2.set_xticks(range(L_java_set2), [java_project_map[x] for x in list_of_java_projects_set2])
    ax2.set_xlim(-0.5, L_java_set2-0.5)
    # ax2.set_yscale("log")
    ax2.set_ylim(0, max(java_projs_set2["Max Time in h"]) * 1.05)
    # ax2.set_ylabel("execution time (h)")
    
    # plot bars, l1,l2 missing
    ax2.bar(range(L_java_set2), java_projs_set2["Max Time in h"], color=max_time_color, label="execution time (full config.)")
    ax2.bar(range(L_java_set2), java_projs_set2["Min Time in h"], color=min_time_color, label="execution time (min. config.)")
    fig.add_subplot(ax2)
    
    # twin x and quality marks (only works when plotted on twin after original is added to figure)
    ax2t = ax2.twinx()
    ax2t.set_ylim(0,1.05)
    ax2t.set_yticks([])
    # ax2t.set_ylabel("fraction of microbenchmarks")
    
    ax2t.scatter(np.array(range(L_java_set2)) - 0.25, java_projs_set2["Fraction of leq 0.01 change"], marker="x", color=leq001_color, label="fraction of microbenchmarks with 1% change")
    ax2t.scatter(np.array(range(L_java_set2)), java_projs_set2["Fraction of leq 0.03 change"], marker="o", facecolor="none", edgecolor=leq003_color, label="fraction of microbenchmarks with 3% change")
    ax2t.scatter(np.array(range(L_java_set2)) + 0.25, java_projs_set2["Fraction of leq 0.05 change"], marker="v", facecolor="none", edgecolor=leq005_color, label="fraction of microbenchmarks with 5% change")
    # ax2t.scatter(np.array(range(L_java_set2)) + 0.1, java_projs_set2["Fraction of leq 0.1 change"], marker="x", color=leq010_color, label="fraction of 0.1 change")
    
    # initialize java subplot for data set 3
    ax3 = plt.Subplot(fig, inner[2])
    
    # setup title, ticks, limits, labels
    ax3.set_title("Data Set 3 (Java)")
    # ax3.set_xticks(range(L_java_set3), list_of_java_projects_set3, rotation="vertical")
    ax3.set_xticks(range(L_java_set3), [java_project_map[x] for x in list_of_java_projects_set3])
    ax3.set_xlim(-0.5, L_java_set3-0.5)
    # ax3.set_yscale("log")
    ax3.set_ylim(0, max(java_projs_set3["Max Time in h"]) * 1.05)
    # ax3.set_ylabel("execution time (h)")
    
    # plot bars, l1,l2 missing
    ax3.bar(range(L_java_set3), java_projs_set3["Max Time in h"], color=max_time_color, label="execution time (full config.)")
    ax3.bar(range(L_java_set3), java_projs_set3["Min Time in h"], color=min_time_color, label="execution time (min. config.)")
    fig.add_subplot(ax3)
    
    # twin x and quality marks (only works when plotted on twin after original is added to figure)
    ax3t = ax3.twinx()
    ax3t.set_ylim(0,1.05)
    # ax3t.set_yticks([])
    ax3t.set_ylabel("fraction of microbenchmarks")
    
    ax3t.scatter(np.array(range(L_java_set3)) - 0.25, java_projs_set3["Fraction of leq 0.01 change"], marker="x", color=leq001_color, label="fraction of microbenchmarks with 1% change")
    ax3t.scatter(np.array(range(L_java_set3)), java_projs_set3["Fraction of leq 0.03 change"], marker="o", facecolor="none", edgecolor=leq003_color, label="fraction of microbenchmarks with 3% change")
    ax3t.scatter(np.array(range(L_java_set3)) + 0.25, java_projs_set3["Fraction of leq 0.05 change"], marker="v", facecolor="none", edgecolor=leq005_color, label="fraction of microbenchmarks with 5% change")
    # ax3t.scatter(np.array(range(L_java_set3)) + 0.1, java_projs_set3["Fraction of leq 0.1 change"], marker="x", color=leq010_color, label="fraction of 0.1 change")

    # plt.close(fig)
    fig.savefig(f"plots/time_savings_{i}.pdf", bbox_inches = "tight")

