# FastDownward

This folder contains the results of the FastDownward (https://www.fast-downward.org) case study.

## Measurement

### General Information
We have used the workload data-network-opt-strips problem 05 from https://github.com/aibasel/downward-benchmarks.
Further, we executed our measurements on an Intel Xeon E5-2630 v4 at 2.20~GHz with 256 GiB RAM (Debian 11).
We contacted Daniel Gnad as an experienced user of Fast Downward and chose with Daniel Gnad the releases, workloads, and configuration options.

### Repetitions

We have repeated the measurement of each configuration 5 times.
The measurement of the configuration was restarted when the relative standard deviation of the performance exceeded 10%.

## Releases

The chosen commits/releases for our performance measurements are:
* 2016_07: e4eb64c613ae34b97ab9409deac5331ec2ce5e43
* 2017_01: 91f44fa59ea57014a7769062a92aa752f503128e
* 2017_07: 363e2fc9a8b7adb48b4c30e929097798928c7370
* 2018_01: 0e8acd2f2613e032040dc6b6d4bf1926848aa4cb
* 2018_07: dd7ddfeea72a699d381dce35657d683259be77c0
* 2019_01: 2cc2a66e8073a73571e0a37cd806380f13751a7c
* 2019_06: release-19.06.0 (das ist ein Release Tag)
* 2019_12: release-19.12.0 (Release Tag)
* 2020_06: release-20.06.0 (Release Tag)
