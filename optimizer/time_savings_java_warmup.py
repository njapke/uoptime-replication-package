#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# reset kernel, when editing other figures
rcParams["lines.markersize"] = 6.0 # default is 6.0
rcParams["font.size"] = 15.0 # default is 10.0

method_map = {"cv__mean__ci_bootstrap_mean_p":"Mean (CV)",
              "cv__median__ci_bootstrap_median_p":"Median (CV)",
              "rciw_mean_p__mean__ci_bootstrap_mean_p": "Mean (RCIW_1)",
              "rciw_mean_t__mean__ci_bootstrap_mean_t":"Mean (RCIW_2)",
              "rciw_median_p__median__ci_bootstrap_median_p":"Median (RCIW_3)",
              "rmad__mean__ci_bootstrap_mean_p":"Mean (RMAD)",
              "rmad__median__ci_bootstrap_median_p":"Median (RMAD)"}

java_project_map = {"laaber_byte-buddy" : "J$_1$",
                    "laaber_jctools" : "J$_2$",
                    "laaber_jenetics" : "J$_3$",
                    "laaber_jmh-core-benchmarks" : "J$_4$",
                    "laaber_jmh-jdk-microbenchmarks" : "J$_5$",
                    "laaber_log4j2" : "J$_6$",
                    "laaber_protostuff" : "J$_7$",
                    "laaber_rxjava" : "J$_8$",
                    "laaber_squidlib" : "J$_9$",
                    "laaber_zipkin" : "J$_{10}$"}

java_data_path = "laaber_optimization_warmup_fse20"

### JAVA PROJECTS ###
# get sorted list of all folders
java_projects = list(os.walk(java_data_path))[0][1]
java_projects.sort()

# read in java data
java_optimization_quality = []
for project in java_projects:
    data_path = java_data_path+"/"+project
    
    # get sorted list of all files
    folders = list(os.walk(data_path))[0][1]
    folders.sort()
    
    print("Begin reading "+project)
    if len(java_optimization_quality) == 0:
        java_optimization_quality = pd.read_csv(data_path+"/quality_analysis.csv")
    else:
        new_df = pd.read_csv(data_path+"/quality_analysis.csv")
        java_optimization_quality = pd.concat([java_optimization_quality, new_df])

list_of_java_projects = list(np.array(java_optimization_quality["Project"].drop_duplicates()))
L_java = len(list_of_java_projects)


# plot variables
max_time_color = "#d9d9d9"
min_time_color = "#969696"
max_warmup_color = "#bdbdbd"
min_warmup_color = "#737373"
leq001_color = "#525252"
leq003_color = "#525252"
leq005_color = "#525252"


# initialize figure
fig_ratio = 3/4
fig = plt.figure(layout="constrained", figsize=(8,5.5))
ax = plt.axes()

java_projs = java_optimization_quality[java_optimization_quality["Method"] == "rciw_median_p__median__ci_bootstrap_median_p"]
ax.set_title("RCIW$_3$")

# calculate long bars to plot
full_config_time = np.array(java_projs["Max Time in h"]) + np.array(java_projs["Max Warmup in h"])
min_config_time = np.array(java_projs["Min Time in h"]) + np.array(java_projs["Min Warmup in h"])

# setup title, ticks, limits, labels
ax.set_title("Execution Times considering Warmup Phases for\nData Set 2 (RCIW$_3$)")
# ax.set_xticks(range(L_java), list_of_java_projects, rotation="vertical")
ax.set_xticks(range(L_java), [java_project_map[x] for x in list_of_java_projects])
ax.set_xlim(-0.5, L_java-0.5)
ax.set_ylim(0, max(full_config_time) * 1.05)
ax.set_ylabel("execution time (h)")

# plot bars, l1,l2 missing
left_pos = np.array(range(L_java)) - 0.2
right_pos = np.array(range(L_java)) + 0.2

l1 = ax.bar(left_pos, full_config_time, width=0.4, color=max_time_color, label="measurement time\n(full config.)")
l2 = ax.bar(left_pos, java_projs["Max Warmup in h"], width=0.4, color=max_warmup_color, label="warmup time\n(full config.)")

l3 = ax.bar(right_pos, min_config_time, width=0.4, color=min_time_color, label="measurement time\n(min. config.)")
l4 = ax.bar(right_pos, java_projs["Min Warmup in h"], width=0.4, color=min_warmup_color, label="warmup time\n(min. config.)")

# twin x and quality marks (only works when plotted on twin after original is added to figure)
axt = ax.twinx()
axt.set_ylim(0,1.05)
# ax2t.set_yticks([])
axt.set_ylabel("fraction of microbenchmarks")

l5 = axt.scatter(np.array(range(L_java)) - 0.25, java_projs["Fraction of leq 0.01 change"], marker="x", color=leq001_color, label="fraction of MBs\nwith 1% change")
l6 = axt.scatter(np.array(range(L_java)), java_projs["Fraction of leq 0.03 change"], marker="o", facecolor="none", edgecolor=leq003_color, label="fraction of MBs\nwith 3% change")
l7 = axt.scatter(np.array(range(L_java)) + 0.25, java_projs["Fraction of leq 0.05 change"], marker="v", facecolor="none", edgecolor=leq005_color, label="fraction of MBs\nwith 5% change")

# fig.legend(handles=[l1,l2,l3,l4,l5,l6,l7], loc='center left', bbox_to_anchor=(0.085,0.45))
fig.legend(handles=[l1,l2,l3,l4,l5,l6,l7], bbox_to_anchor=(0, -0.45), loc="lower left", bbox_transform=fig.transFigure, ncol=2)

fig.savefig("time_savings_warmup.pdf", bbox_inches = "tight")
