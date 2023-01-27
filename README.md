[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

# Performance Evolution of Configurable Software Systems: An Empirical Study

This repository is the supplementary Web site for the paper "Performance Evolution of Configurable Software Systems: An Empirical Study" submitted to the EMSE. In this repository, we list further information to the paper. 

## Data

The data to all subject systems are included in the directory [PerformanceEvolution_Data](./PerformanceEvolution_Data). In each of the case study directories, you will find the following files:
* *README.md*: This file includes information about the performed measurements and the benchmark we used.
* *FeatureModel.xml*: The feature model containing the description of the configuration options that we measured.
* *measurements.csv*: A csv file containing all configurations and the measured performance values. Note that we also measured other non-functional properties that were not investigated in the paper. 
* *models/models.csv*: This file contains the performance models that we learned for each release. Note that we identified the relevant terms of all releases in a first step and afterwards, learned a consistent performance model containing all relevant terms for all releases. Only this way, we could ensure the comparability of performance models in between releases. 
* *WorkloadDescriptions.txt*: This [file](./PerformanceEvolution_Data/WorkloadDescriptions.txt) contains the description of the used workloads.

We used the given data to generate all our plots and results.

## RQ1.1: What is the fraction of configurations affected by performance changes between consecutive releases?

Case Studies | AbsolutePerformance| Difference| 
--- | --- | --- | 
brotli| [1](./RQ1/brotli/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/brotli/Difference/configurationsDifference.pdf) | 
Fast Downward| [1](./RQ1/FastDownward/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/FastDownward/Difference/configurationsDifference.pdf) | 
HSQLDB| [1](./RQ1/HSQLDB/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/HSQLDB/Difference/configurationsDifference.pdf) | 
lrzip| [1](./RQ1/lrzip/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/lrzip/Difference/configurationsDifference.pdf) | 
MariaDB | [1](./RQ1/MariaDB/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/MariaDB/Difference/configurationsDifference.pdf) | 
MySQL |[1](./RQ1/MySQL/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/MySQL/Difference/configurationsDifference.pdf) | 
OpenVPN| [1](./RQ1/OpenVPN/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/OpenVPN/Difference/configurationsDifference.pdf) | 
Opus| [1](./RQ1/Opus/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/Opus/Difference/configurationsDifference.pdf) | 
PostgreSQL| [1](./RQ1/PostgreSQL/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/PostgreSQL/Difference/configurationsDifference.pdf) | 
VP8| [1](./RQ1/VP8/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/VP8/Difference/configurationsDifference.pdf) | 
VP9| [1](./RQ1/VP9/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/VP9/Difference/configurationsDifference.pdf)  | 
z3| [1](./RQ1/z3/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/z3/Difference/configurationsDifference.pdf) | 

The following table contains the number of releases where a certain (rounded) percent of configurations have changed. 
Note that there are only 2 releases with exactly 0 configurations indicating a performance change; the other 9 displayed in the table below are near to 0 (e.g., 0.4%). The same applies to 100%.

| %Changes | Frequency |
| :---: | :---: |
| 0 | 26 |
| 1 | 30 |
| 2 | 14 |
| 3 | 10 |
| 4 | 5 |
| 5 | 4 |
| 6 | 1 |
| 7 | 2 |
| 8 | 1 |
| 9 | 1 |
| 10 | 0 |
| 11 | 2 |
| 12 | 0 |
| 13 | 1 |
| 14 | 1 |
| 15 | 2 |
| 16 | 1 |
| 17 | 2 |
| 18 | 0 |
| 19 | 2 |
| 20 | 1 |
| 21 | 1 |
| 22 | 0 |
| 23 | 1 |
| 24 | 1 |
| 25 | 0 |
| 26 | 2 |
| 27 | 0 |
| 28 | 2 |
| 29 | 0 |
| 30 | 1 |
| 31 | 1 |
| 32 | 0 |
| 33 | 0 |
| 34 | 0 |
| 35 | 1 |
| 36 | 0 |
| 37 | 2 |
| 38 | 2 |
| 39 | 1 |
| 40 | 2 |
| 41 | 0 |
| 42 | 2 |
| 43 | 2 |
| 44 | 1 |
| 45 | 1 |
| 46 | 1 |
| 47 | 2 |
| 48 | 0 |
| 49 | 1 |
| 50 | 1 |
| 51 | 2 |
| 52 | 0 |
| 53 | 0 |
| 54 | 1 |
| 55 | 1 |
| 56 | 0 |
| 57 | 0 |
| 58 | 0 |
| 59 | 1 |
| 60 | 1 |
| 61 | 0 |
| 62 | 0 |
| 63 | 0 |
| 64 | 1 |
| 65 | 0 |
| 66 | 1 |
| 67 | 0 |
| 68 | 0 |
| 69 | 0 |
| 70 | 2 |
| 71 | 0 |
| 72 | 3 |
| 73 | 0 |
| 74 | 1 |
| 75 | 1 |
| 76 | 0 |
| 77 | 2 |
| 78 | 0 |
| 79 | 0 |
| 80 | 1 |
| 81 | 0 |
| 82 | 2 |
| 83 | 0 |
| 84 | 1 |
| 85 | 1 |
| 86 | 0 |
| 87 | 2 |
| 88 | 0 |
| 89 | 1 |
| 90 | 0 |
| 91 | 1 |
| 92 | 1 |
| 93 | 1 |
| 94 | 1 |
| 95 | 0 |
| 96 | 1 |
| 97 | 2 |
| 98 | 6 |
| 99 | 4 |
| 100 | 2 |


## RQ1.2: How stable is the relative performance of configurations in the presence of performance changes between consecutive releases?

The following table displays the number of releases with a certain Kendall Tau value. 

Configuration Tau values:
| Tau | Frequency |
| :---: | :---: |
|-1.0 -- -0.9 | 1 |
|-0.9 -- -0.8 | 0 |
|-0.8 -- -0.7 | 0 |
|-0.7 -- -0.6 | 0 |
|-0.6 -- -0.5 | 0 |
|-0.5 -- -0.4 | 0 |
|-0.4 -- -0.3 | 0 |
|-0.3 -- -0.2 | 2 |
|-0.2 -- -0.1 | 0 |
|-0.1 -- -0.0 | 2 |
|-0.0 -- 0.1 | 3 |
|0.1 -- 0.2 | 4 |
|0.2 -- 0.3 | 4 |
|0.3 -- 0.4 | 8 |
|0.4 -- 0.5 | 6 |
|0.5 -- 0.6 | 9 |
|0.6 -- 0.7 | 18 |
|0.7 -- 0.8 | 16 |
|0.8 -- 0.9 | 41 |
|0.9 -- 1.0 | 49 |
|1.0 -- 1.1 | 8 |

## RQ2.1: How frequent and how strong are changes of performance influences of individual configuration options and interactions between consecutive releases?

The error rates when learning the performance-influence models were as follows:
| Case Study | Release | Error Rate | 
| :---: | :---: | :---: |
| brotli | 0.3.0 | 0.23% |
| | 0.4.0 | 3.02% |
| | 0.5.2 | 2.89% |
| | 0.6.0 | 2.95% |
| | 1.0.0 | 2.96% |
| | 1.0.1 | 3.01% |
| | 1.0.2 | 3.01% |
| | 1.0.3 | 3.67% |
| | 1.0.4 | 3.75% |
| | 1.0.5 | 3.72% |
| | 1.0.6 | 3.67% |
| | 1.0.7 | 3.73% |
| FastDownward | 2016.07 | 3.51% |
| | 2017.01 | 3.62% |
| | 2017.07 | 3.48% |
| | 2018.01 | 3.53% |
| | 2018.07 | 3.66% |
| | 2019.01 | 4.04% |
| | 2019.06 | 4.19% |
| | 2019.12 | 4.17% |
| | 2020.06 | 4.28% |
| HSQLDB | 2.1.0 | 2.40% |
| | 2.2.0 | 3.02% |
| | 2.2.1 | 3.00% |
| | 2.2.2 | 2.87% |
| | 2.2.3 | 2.89% |
| | 2.2.4 | 2.88% |
| | 2.2.5 | 2.71% |
| | 2.2.6 | 2.99% |
| | 2.2.7 | 3.07% |
| | 2.2.8 | 3.02% |
| | 2.2.9 | 3.21% |
| | 2.3.0 | 3.28% |
| | 2.3.1 | 3.28% |
| | 2.3.2 | 3.28% |
| | 2.3.3 | 3.64% |
| | 2.3.4 | 3.43% |
| | 2.3.5 | 3.54% |
| | 2.4.0 | 3.43% |
| | 2.4.1 | 3.44% |
| lrzip | 530 | 5.27% |
| | 543 | 5.58% |
| | 544 | 3.48% |
| | 550 | 7.35% |
| | 551 | 7.37% |
| | 552 | 7.34% |
| | 560 | 6.41% |
| | 571 | 5.98% |
| | 601 | 7.23% |
| | 602 | 7.48% |
| | 604 | 7.21% |
| | 606 | 7.46% |
| | 607 | 5.59% |
| | 608 | 7.29% |
| | 611 | 6.73% |
| | 612 | 6.68% |
| | 614 | 6.82% |
| | 615 | 6.74% |
| | 616 | 6.71% |
| | 620 | 6.73% |
| | 621 | 6.87% |
| | 631 | 6.92% |
| MariaDB | 5.5.23 | 10.14% |
| | 5.5.27 | 9.35% |
| | 5.5.29 | 9.16% |
| | 5.5.31 | 8.72% |
| | 5.5.33a | 8.77% |
| | 5.5.35 | 9.54% |
| | 5.5.38 | 10.36% |
| | 5.5.40 | 9.40% |
| | 10.0.17 | 4.74% |
| | 10.0.19 | 4.73% |
| | 10.1.8 | 4.99% |
| | 10.1.12 | 5.02% |
| | 10.1.14 | 5.17% |
| | 10.1.16 | 5.14% |
| | 10.2.6 | 11.13% |
| | 10.2.7 | 11.06% |
| | 10.2.11 | 4.55% |
| | 10.2.14 | 5.10% |
| | 10.3.8 | 4.93% |
| | 10.3.11 | 4.85% |
| | 10.3.14 | 5.03% |
| | 10.4.7 | 5.16% |
| MySQL | 5.6.10 | 2.70% |
| | 5.6.13 | 3.15% |
| | 5.6.15 | 3.29% |
| | 5.6.17 | 3.38% |
| | 5.6.20 | 3.49% |
| | 5.6.22 | 3.55% |
| | 5.6.24 | 3.72% |
| | 5.6.26 | 3.42% |
| | 5.7.9 | 3.55% |
| | 5.7.11 | 3.36% |
| | 5.7.14 | 3.45% |
| | 5.7.17 | 3.00% |
| | 5.7.18 | 3.41% |
| | 5.7.20 | 3.11% |
| | 5.7.21 | 3.56% |
| | 5.7.22 | 3.97% |
| | 8.0.12 | 3.06% |
| | 8.0.13 | 3.02% |
| | 8.0.15 | 3.38% |
| | 8.0.17 | 3.18% |
| OpenVPN | 2.1.0 | 1.54% |
| | 2.1.2 | 1.55% |
| | 2.1.4 | 1.49% |
| | 2.2.0 | 1.50% |
| | 2.2.1 | 1.55% |
| | 2.2.2 | 1.50% |
| | 2.3.0 | 2.04% |
| | 2.3.18 | 1.85% |
| | 2.3.9 | 2.13% |
| | 2.4.0 | 2.08% |
| | 2.4.3 | 2.02% |
| | 2.4.6 | 2.13% |
| Opus | 1.0.0 | 11.26% |
| | 1.0.1 | 11.27% |
| | 1.0.2 | 11.26% |
| | 1.0.3 | 11.26% |
| | 1.1 | 11.26% |
| | 1.1.1 | 11.26% |
| | 1.1.2 | 11.27% |
| | 1.1.5 | 11.27% |
| | 1.2 | 11.27% |
| | 1.2.1 | 11.27% |
| | 1.3 | 11.26% |
| | 1.3.1 | 11.26% |
| PostgreSQL | 8.3.0 | 1.07% |
| | 8.3.5 | 1.72% |
| | 8.4.0 | 1.30% |
| | 8.4.2 | 1.42% |
| | 9.0.0 | 1.34% |
| | 9.0.4 | 0.67% |
| | 9.1.0 | 1.20% |
| | 9.1.3 | 1.37% |
| | 9.2.0 | 1.13% |
| | 9.2.4 | 1.10% |
| | 9.3.0 | 1.21% |
| | 9.3.4 | 1.22% |
| | 9.4.0 | 1.29% |
| | 9.4.4 | 1.56% |
| | 9.5.0 | 1.25% |
| | 9.5.3 | 1.90% |
| | 9.6.0 | 1.89% |
| | 9.6.3 | 2.54% |
| | 10.0 | 2.13% |
| | 10.4 | 1.86% |
| | 11.0 | 1.43% |
| | 11.2 | 2.02% |
| VP8 | v0.9.1 | 1.88% |
| | v0.9.2 | 1.57% |
| | v0.9.5 | 1.67% |
| | v0.9.6 | 1.06% |
| | v0.9.7 | 1.36% |
| | v0.9.7-p1 | 1.00% |
| | v1.0.0 | 0.74% |
| | v1.1.0 | 0.66% |
| | v1.2.0 | 0.69% |
| | v1.3.0 | 0.70% |
| | v1.4.0 | 1.14% |
| | v1.5.0 | 1.19% |
| | v1.6.1 | 1.98% |
| | v1.7.0 | 2.06% |
| | v1.8.0 | 1.95% |
| VP9 | v1.3.0 | 0.66% |
| | v1.4.0 | 2.22% |
| | v1.5.0 | 8.06% |
| | v1.6.0 | 1.65% |
| | v1.6.1 | 1.57% |
| | v1.7.0 | 1.27% |
| | v1.8.0 | 2.48% |
| z3 | 4.3.2 | 1.20% |
| | 4.4.0 | 1.27% |
| | 4.4.1 | 1.97% |
| | 4.5.0 | 1.59% |
| | 4.6.0 | 1.58% |
| | 4.7.1 | 1.56% |
| | 4.8.1 | 1.59% |
| | 4.8.3 | 1.44% |
| | 4.8.4 | 1.55% |
| | 4.8.5 | 1.52% |
| | 4.8.6 | 1.58% |
| | 4.8.7 | 1.49% |
| | 4.8.8 | 1.46% |
| | 4.8.9 | 1.64% |
| | 4.8.10 | 1.51% |
| | 4.8.11 | 1.47% |
| | 4.8.12 | 1.45% |
| | 4.8.13 | 1.62% |

Case Studies | AbsoluteInfluence| InfluenceDifference| 
--- | --- | --- | 
brotli| [1](./RQ2/brotli/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/brotli/InfluenceDifference/influenceDifference.pdf) | 
Fast Downward| [1](./RQ2/FastDownward/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/FastDownward/InfluenceDifference/influenceDifference.pdf) | 
HSQLDB| [1](./RQ2/HSQLDB/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/HSQLDB/InfluenceDifference/influenceDifference.pdf) | 
lrzip| [1](./RQ2/lrzip/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/lrzip/InfluenceDifference/influenceDifference.pdf) | 
MariaDB| [1](./RQ2/MariaDB/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/MariaDB/InfluenceDifference/influenceDifference.pdf) | 
MySQL| [1](./RQ2/MySQL/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/MySQL/InfluenceDifference/influenceDifference.pdf) | 
OpenVPN| [1](./RQ2/OpenVPN/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/OpenVPN/InfluenceDifference/influenceDifference.pdf) | 
Opus| [1](./RQ2/Opus/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/Opus/InfluenceDifference/influenceDifference.pdf) | 
PostgreSQL| [1](./RQ2/PostgreSQL/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/PostgreSQL/InfluenceDifference/influenceDifference.pdf) | 
VP8| [1](./RQ2/VP8/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/VP8/InfluenceDifference/influenceDifference.pdf) | 
VP9| [1](./RQ2/VP9/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/VP9/InfluenceDifference/influenceDifference.pdf) | 
z3| [1](./RQ2/z3/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/z3/InfluenceDifference/influenceDifference.pdf) | 

When counting the relative influence of each term on the performance of a system, we obtained the following values:
|influence|frequency|
|  :----: |  :----: |
|0|69.90749563284666|
|5|13.192111605619827|
|10|4.774771061319695|
|15|2.88331090037385|
|20|3.2196969696969693|
|25|1.5752765752765754|
|30|1.0285338360629983|
|35|0.6410256410256411|
|40|0.0|
|45|0.0|
|50|0.0|
|55|0.0|
|60|0.0|
|65|0.0|
|70|0.0|
|75|0.0|
|80|2.7777777777777772|
|85|0.0|
|90|0.0|
|95|0.0|
|100|0.0|

## RQ2.2: How stable is the relative influence of configuration options and interactions in the presence of performance changes between consecutive releases?

Case Studies | Ranking| 
--- | --- | 
brotli| [1](./RQ2/brotli/Ranking/influenceRanking.pdf) | 
Fast Downward| [1](./RQ2/FastDownward/Ranking/influenceRanking.pdf) | 
HSQLDB| [1](./RQ2/HSQLDB/Ranking/influenceRanking.pdf) | 
lrzip| [1](./RQ2/lrzip/Ranking/influenceRanking.pdf) | 
OpenVPN| [1](./RQ2/OpenVPN/Ranking/influenceRanking.pdf) | 
Opus| [1](./RQ2/Opus/Ranking/influenceRanking.pdf) | 
PostgreSQL| [1](./RQ2/PostgreSQL/Ranking/influenceRanking.pdf) | 
VP8| [1](./RQ2/VP8/Ranking/influenceRanking.pdf) | 
VP9| [1](./RQ2/VP9/Ranking/influenceRanking.pdf) | 
z3| [1](./RQ2/z3/Ranking/influenceRanking.pdf) | 

We have obtained the following Kendall Tau values:

| Tau | Frequency |
| :---: | :---: |
|-1.0 -- -0.9 | 0 |
|-0.9 -- -0.8 | 0 |
|-0.8 -- -0.7 | 0 |
|-0.7 -- -0.6 | 0 |
|-0.6 -- -0.5 | 0 |
|-0.5 -- -0.4 | 0 |
|-0.4 -- -0.3 | 0 |
|-0.3 -- -0.2 | 0 |
|-0.2 -- -0.1 | 0 |
|-0.1 -- -0.0 | 0 |
|-0.0 -- 0.1 | 3 |
|0.1 -- 0.2 | 1 |
|0.2 -- 0.3 | 3 |
|0.3 -- 0.4 | 3 |
|0.4 -- 0.5 | 2 |
|0.5 -- 0.6 | 1 |
|0.6 -- 0.7 | 6 |
|0.7 -- 0.8 | 6 |
|0.8 -- 0.9 | 11 |
|0.9 -- 1.0 | 15 |
|1.0 -- 1.1 | 127 |
