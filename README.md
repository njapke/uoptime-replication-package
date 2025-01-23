# Replication Package of "µOpTime: Statically Reducing the Execution Time of Microbenchmark Suites Using Stability Metrics"

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14725868.svg)](https://doi.org/10.5281/zenodo.14725868)

This repository contains the replication package for μOpTime.

## Research

If you use this software in a publication, please cite it as:

```bibtex
@software{japke_2025_14725868,
  author       = {Japke, Nils and
                  Grambow, Martin and
                  Laaber, Christoph and
                  Bermbach, David},
  title        = {Replication Package: µOpTime: Statically Reducing
                   the Execution Time of Microbenchmark Suites Using
                   Stability Metrics},
  month        = jan,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.14725868},
  url          = {https://doi.org/10.5281/zenodo.14725868},
}
```

Please also cite the corresponding paper as:

```bibtex
@misc{japke2025muoptimestaticallyreducingexecution,
      title={$\mu$OpTime: Statically Reducing the Execution Time of Microbenchmark Suites Using Stability Metrics}, 
      author={Nils Japke and Martin Grambow and Christoph Laaber and David Bermbach},
      year={2025},
      eprint={2501.12878},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2501.12878}, 
}
```

## Content

This repository contains a Go project called _cloud benchmark tool_, which can run microbenchmarking experiments in GCloud instances using open-source projects that use Go's testing toolchain.
Next, there is the implementation of μOpTime, an approach to reduce the levels of repetition in an RMIT-based microbenchmarking experiment.
The folder _optimizer_ contains several Python scripts, which implement the optimization algorithm of μOpTime, as well as scripts for analysis of the results.
Finally, there is the data set of microbenchmarking results of 3 open-source Go projects, which we collected for evaluating μOpTime, which is contained in the folders _optimizer/dataset_1/final\_data\_with\_config_ (in SQLite format) and _optimizer/dataset_1/go\_data\_path_ (in CSV format).

