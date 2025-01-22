# Replication Package of "µOpTime: Statically Reducing the Execution Time of Microbenchmark Suites Using Stability Metrics"

This repository contains the replication package for μOpTime.
It contains a Go project called _cloud benchmark tool_, which can run microbenchmarking experiments in GCloud instances using open-source projects that use Go's testing toolchain.
Next, there is the implementation of μOpTime, an approach to reduce the levels of repetition in an RMIT-based microbenchmarking experiment.
The folder _optimizer_ contains several Python scripts, which implement the optimization algorithm of μOpTime, as well as scripts for analysis of the results.
Finally, there is the data set of microbenchmarking results of 3 open-source Go projects, which we collected for evaluating μOpTime, which is contained in the folders _optimizer/dataset_1/final\_data\_with\_config_ (in SQLite format) and _optimizer/dataset_1/go\_data\_path_ (in CSV format).

