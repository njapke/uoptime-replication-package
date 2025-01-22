#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast import literal_eval as make_tuple
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as sta
import scikit_posthocs as sp
from cliffs_delta import cliffs_delta

# prevent showing of figures
plt.ioff()
sns.set(rc={'figure.figsize':(12,8)})

method_map = {"cv__mean__ci_bootstrap_mean_p":"Mean (CV)",
              "cv__median__ci_bootstrap_median_p":"Median (CV)",
              "rciw_mean_p__mean__ci_bootstrap_mean_p": "Mean (RCIW_1)",
              "rciw_mean_t__mean__ci_bootstrap_mean_t":"Mean (RCIW_2)",
              "rciw_median_p__median__ci_bootstrap_median_p":"Median (RCIW_3)",
              "rmad__mean__ci_bootstrap_mean_p":"Mean (RMAD)",
              "rmad__median__ci_bootstrap_median_p":"Median (RMAD)"}

# input data
# path_of_projects = "dataset_1/go_optimization_new"
# full_config_time = 3*5*5 # go
# full_config_string = "(3, 5, 5)"
# path_of_projects = "dataset_2/laaber_optimization_warmup_fse20"
# full_config_time = 5*50 # java warmup
# full_config_string = "(5, 50)"
# path_of_projects = "dataset_2/laaber_optimization_nowarmup_fse20"
# full_config_time = 5*100 # java no warmup
# full_config_string = "(5, 100)"
path_of_projects = "dataset_3/optimizer_results_ese21/optimizer_results_only_latest"
full_config_time = 3*20 # java warmup
full_config_string = "(3, 20)"

# get sorted list of all files
projects = list(os.walk(path_of_projects))[0][1]
projects.sort()


h_test = []
for project in projects:

    data_path = path_of_projects+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    print("Begin analyzing "+project)
    res = []
    avg_dev_col = []
    method_col = []
    # loop over all subfolders
    for folder in folders:
        print("Processing "+folder)
        
        # quality data
        min_setup = pd.read_csv(data_path+"/"+folder+"/min_config_res.csv")
        quality = pd.read_csv(data_path+"/"+folder+"/quality_df.csv")
        N = len(min_setup)
        
        # time saving
        max_time_s = full_config_time*N
        max_time_h = max_time_s / 60 / 60
        time_saved = np.sum(np.array(quality["Time Saved"]))
        time_saved_p = time_saved / max_time_s
        min_time_s = max_time_s - time_saved
        min_time_h = min_time_s / 60 / 60
        
        # only for Java warmup: calculate warmup times
        if path_of_projects == "laaber_optimization_warmup_fse20":
            max_warmup_s = 5*50*N # warmup phase is 50 iterations on each fork
            max_warmup_h = max_warmup_s / 60 / 60
            min_config_forks = np.array([make_tuple(x)[0] for x in min_setup["Config"]])
            min_warmup_s = np.sum(min_config_forks*50)
            min_warmup_h = min_warmup_s / 60 / 60
            warmup_saved = np.sum(min_config_forks*(-50) + 5*50)
            warmup_saved_p = time_saved / max_warmup_s
        elif path_of_projects == "optimizer_results_ese21/optimizer_results_only_latest":
            max_warmup_s = 3*20*N # warmup phase is 20 iterations on each fork
            max_warmup_h = max_warmup_s / 60 / 60
            min_config_forks = np.array([make_tuple(x)[0] for x in min_setup["Config"]])
            min_warmup_s = np.sum(min_config_forks*20)
            min_warmup_h = min_warmup_s / 60 / 60
            warmup_saved = np.sum(min_config_forks*(-50) + 3*20)
            warmup_saved_p = time_saved / max_warmup_s
        
        # avg diff
        abs_avg_diff = np.abs(np.array(quality["Average Difference"]))
        leq001 = len(abs_avg_diff[abs_avg_diff <= 0.01]) / len(abs_avg_diff)
        leq003 = len(abs_avg_diff[abs_avg_diff <= 0.03]) / len(abs_avg_diff)
        leq005 = len(abs_avg_diff[abs_avg_diff <= 0.05]) / len(abs_avg_diff)
        leq010 = len(abs_avg_diff[abs_avg_diff <= 0.1]) / len(abs_avg_diff)
        
        # ci diff
        ci_up_diff = np.abs(np.array(quality["CI Upper Difference"]))
        worst_ci_u = max(ci_up_diff)
        ci_lo_diff = np.abs(np.array(quality["CI Lower Difference"]))
        worst_ci_lo = max(ci_lo_diff)
        
        avg_diff = np.array(quality["Average Difference"])
        N = len(avg_diff)
        if len(avg_dev_col) == 0:
            avg_dev_col = avg_diff
            method_col = np.repeat([method_map[folder]],N)
        else:
            avg_dev_col = np.concatenate((avg_dev_col, avg_diff))
            method_col = np.concatenate((method_col, np.repeat([method_map[folder]],N)))
        
        
        if path_of_projects == "laaber_optimization_warmup_fse20" or path_of_projects == "optimizer_results_ese21/optimizer_results_only_latest":
            res.append([project, folder, max_time_s, max_time_h, min_time_s, min_time_h, time_saved, time_saved_p, max_warmup_s, max_warmup_h, min_warmup_s, min_warmup_h, warmup_saved, warmup_saved_p, leq001, leq003, leq005, leq010, worst_ci_u, worst_ci_lo])
        else:
            res.append([project, folder, max_time_s, max_time_h, min_time_s, min_time_h, time_saved, time_saved_p, leq001, leq003, leq005, leq010, worst_ci_u, worst_ci_lo])
    
    if path_of_projects == "laaber_optimization_warmup_fse20" or path_of_projects == "optimizer_results_ese21/optimizer_results_only_latest":
        result_df = pd.DataFrame(res, columns=["Project","Method","Max Time in s","Max Time in h","Min Time in s","Min Time in h","Time Saved","Time Saved %","Max Warmup in s","Max Warmup in h","Min Warmup in s","Min Warmup in h","Warmup Saved","Warmup Saved %","Fraction of leq 0.01 change","Fraction of leq 0.03 change","Fraction of leq 0.05 change","Fraction of leq 0.1 change","CI Lower Dev","CI Upper Dev"])
    else:
        result_df = pd.DataFrame(res, columns=["Project","Method","Max Time in s","Max Time in h","Min Time in s","Min Time in h","Time Saved","Time Saved %","Fraction of leq 0.01 change","Fraction of leq 0.03 change","Fraction of leq 0.05 change","Fraction of leq 0.1 change","CI Lower Dev","CI Upper Dev"])
    avg_dev_df = pd.DataFrame({"Average Difference":avg_dev_col, "Method":method_col})
    result_df.to_csv(data_path+"/quality_analysis.csv",index=False)
    
    # kruskal-wallis h test
    methods = avg_dev_df["Method"].drop_duplicates()
    samp = [avg_dev_df[avg_dev_df["Method"] == x]["Average Difference"] for x in methods]
    h_test_res = sta.kruskal(*samp)
    h_test.append([project, h_test_res.statistic, h_test_res.pvalue])
    
    # dunn's post-hoc test
    dunns_test_df = sp.posthoc_dunn(samp)
    dunns_test_df.index = list(methods)
    dunns_test_df.columns = list(methods)
    dunns_test_df.to_csv(data_path+"/dunns_test.csv")
    
    # cliff's delta
    n_samp = len(samp)
    delta_res = np.zeros((n_samp,n_samp))
    for i in range(n_samp):
        for j in range(n_samp):
            delta_res[i,j] = cliffs_delta(samp[i], samp[j])[0]
    delta_df = pd.DataFrame(delta_res, index=list(methods), columns=list(methods))
    delta_df.to_csv(data_path+"/cliffs_delta.csv")
    
    ax = sns.boxplot(data=avg_dev_df, x="Average Difference", y="Method")
    fig = ax.get_figure()
    fig.savefig(path_of_projects+"/"+project+"_boxplot.png",bbox_inches="tight")
    plt.close(fig)

h_test_df = pd.DataFrame(h_test, columns=["Project","Statistic","p-Value"])
h_test_df.to_csv(path_of_projects+"/kruskal.csv",index=False)
