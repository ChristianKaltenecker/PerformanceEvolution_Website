[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

# Performance Evolution of Configurable Software Systems: An Empirical Study

This repository is the supplementary Web site for the paper "Performance Evolution of Configurable Software Systems: An Empirical Study" submitted to the TOSEM. In this repository, we list further information to the paper. 

## Data

The data to all subject systems are included in the directory [PerformanceEvolution_Data](./PerformanceEvolution_Data). In each of the case study directories, you will find the following files:
* *README.md*: This file includes information about the performed measurements and the benchmark we used.
* *FeatureModel.xml*: The feature model containing the description of the configuration options that we measured.
* *measurements.csv*: A csv file containing all configurations and the measured performance values. Note that we also measured other non-functional properties that were not investigated in the paper. 
* *models/models.csv*: This file contains the performance models that we learned for each release. Note that we identified the relevant terms of all releases in a first step and afterwards, learned a consistent performance model containing all relevant terms for all releases. Only this way, we could ensure the comparability of performance models in between releases. 

We used the given data to generate all our plots and results.

## RQ1.1: What is the fraction of configurations affected by performance changes between consecutive releases?

Case Studies | AbsolutePerformance| Difference| 
--- | --- | --- | 
Apache| [1](./RQ1/Apache/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/Apache/Difference/configurationsDifference.pdf) | 
brotli| [1](./RQ1/brotli/AbsolutePerformance/configurationsPerformance.pdf) | [1](./RQ1/brotli/Difference/configurationsDifference.pdf) | 
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

%Changes | Frequency | 
 :----: |  :----: | 
0 | 14 | 
1 | 31 | 
2 | 29 | 
3 | 16 | 
4 | 11 | 
5 | 7 | 
6 | 3 | 
7 | 3 | 
8 | 3 | 
9 | 1 | 
10 | 0 | 
11 | 1 | 
12 | 1 | 
13 | 1 | 
14 | 1 | 
15 | 1 | 
16 | 2 | 
17 | 1 | 
18 | 1 | 
19 | 1 | 
20 | 1 | 
21 | 1 | 
22 | 0 | 
23 | 1 | 
24 | 1 | 
25 | 0 | 
26 | 1 | 
27 | 1 | 
28 | 0 | 
29 | 0 | 
30 | 1 | 
31 | 0 | 
32 | 1 | 
33 | 0 | 
34 | 0 | 
35 | 0 | 
36 | 0 | 
37 | 1 | 
38 | 1 | 
39 | 1 | 
40 | 3 | 
41 | 0 | 
42 | 1 | 
43 | 0 | 
44 | 2 | 
45 | 1 | 
46 | 0 | 
47 | 1 | 
48 | 1 | 
49 | 0 | 
50 | 1 | 
51 | 2 | 
52 | 0 | 
53 | 0 | 
54 | 0 | 
55 | 1 | 
56 | 0 | 
57 | 0 | 
58 | 0 | 
59 | 0 | 
60 | 0 | 
61 | 0 | 
62 | 0 | 
63 | 0 | 
64 | 1 | 
65 | 0 | 
66 | 1 | 
67 | 0 | 
68 | 0 | 
69 | 0 | 
70 | 1 | 
71 | 1 | 
72 | 0 | 
73 | 1 | 
74 | 1 | 
75 | 0 | 
76 | 1 | 
77 | 1 | 
78 | 0 | 
79 | 0 | 
80 | 0 | 
81 | 0 | 
82 | 0 | 
83 | 2 | 
84 | 0 | 
85 | 1 | 
86 | 1 | 
87 | 1 | 
88 | 0 | 
89 | 0 | 
90 | 1 | 
91 | 0 | 
92 | 1 | 
93 | 0 | 
94 | 2 | 
95 | 0 | 
96 | 0 | 
97 | 1 | 
98 | 3 | 
99 | 7 | 
100 | 3 | 


## RQ1.2: How stable is the relative performance of configurations in the presence of performance changes between consecutive releases?

The following table displays the number of releases with a certain Kendall Tau value. 

Configuration Tau values:
Kendall Tau value | Frequency | 
 :----: |  :----: | 
-1.00 | 1 | 
-0.99 | 0 | 
-0.98 | 0 | 
-0.97 | 0 | 
-0.96 | 0 | 
-0.95 | 0 | 
-0.94 | 0 | 
-0.93 | 0 | 
-0.92 | 0 | 
-0.91 | 0 | 
-0.90 | 0 | 
-0.89 | 0 | 
-0.88 | 0 | 
-0.87 | 0 | 
-0.86 | 0 | 
-0.85 | 0 | 
-0.84 | 0 | 
-0.83 | 0 | 
-0.82 | 0 | 
-0.81 | 0 | 
-0.80 | 0 | 
-0.79 | 0 | 
-0.78 | 0 | 
-0.77 | 0 | 
-0.76 | 0 | 
-0.75 | 0 | 
-0.74 | 0 | 
-0.73 | 0 | 
-0.72 | 0 | 
-0.71 | 0 | 
-0.70 | 0 | 
-0.69 | 0 | 
-0.68 | 0 | 
-0.67 | 0 | 
-0.66 | 0 | 
-0.65 | 0 | 
-0.64 | 0 | 
-0.63 | 0 | 
-0.62 | 0 | 
-0.61 | 0 | 
-0.60 | 0 | 
-0.59 | 0 | 
-0.58 | 0 | 
-0.57 | 0 | 
-0.56 | 0 | 
-0.55 | 0 | 
-0.54 | 0 | 
-0.53 | 0 | 
-0.52 | 0 | 
-0.51 | 0 | 
-0.50 | 0 | 
-0.49 | 0 | 
-0.48 | 0 | 
-0.47 | 0 | 
-0.46 | 0 | 
-0.45 | 0 | 
-0.44 | 0 | 
-0.43 | 0 | 
-0.42 | 0 | 
-0.41 | 0 | 
-0.40 | 0 | 
-0.39 | 0 | 
-0.38 | 0 | 
-0.37 | 0 | 
-0.36 | 0 | 
-0.35 | 0 | 
-0.34 | 0 | 
-0.33 | 0 | 
-0.32 | 0 | 
-0.31 | 0 | 
-0.30 | 0 | 
-0.29 | 0 | 
-0.28 | 0 | 
-0.27 | 0 | 
-0.26 | 0 | 
-0.25 | 0 | 
-0.24 | 1 | 
-0.23 | 0 | 
-0.22 | 0 | 
-0.21 | 0 | 
-0.20 | 0 | 
-0.19 | 0 | 
-0.18 | 0 | 
-0.17 | 0 | 
-0.16 | 0 | 
-0.15 | 0 | 
-0.14 | 0 | 
-0.13 | 0 | 
-0.12 | 0 | 
-0.11 | 0 | 
-0.10 | 0 | 
-0.09 | 0 | 
-0.08 | 0 | 
-0.07 | 0 | 
-0.06 | 0 | 
-0.05 | 0 | 
-0.04 | 0 | 
-0.03 | 1 | 
-0.02 | 1 | 
-0.01 | 0 | 
0.00 | 1 | 
0.01 | 0 | 
0.02 | 0 | 
0.03 | 0 | 
0.04 | 0 | 
0.05 | 0 | 
0.06 | 1 | 
0.07 | 1 | 
0.08 | 0 | 
0.09 | 0 | 
0.10 | 0 | 
0.11 | 0 | 
0.12 | 0 | 
0.13 | 0 | 
0.14 | 1 | 
0.15 | 1 | 
0.16 | 0 | 
0.17 | 0 | 
0.18 | 1 | 
0.19 | 0 | 
0.20 | 0 | 
0.21 | 0 | 
0.22 | 0 | 
0.23 | 0 | 
0.24 | 2 | 
0.25 | 0 | 
0.26 | 0 | 
0.27 | 0 | 
0.28 | 1 | 
0.29 | 1 | 
0.30 | 5 | 
0.31 | 1 | 
0.32 | 0 | 
0.33 | 1 | 
0.34 | 0 | 
0.35 | 3 | 
0.36 | 1 | 
0.37 | 0 | 
0.38 | 2 | 
0.39 | 0 | 
0.40 | 1 | 
0.41 | 0 | 
0.42 | 0 | 
0.43 | 0 | 
0.44 | 0 | 
0.45 | 3 | 
0.46 | 3 | 
0.47 | 2 | 
0.48 | 1 | 
0.49 | 3 | 
0.50 | 6 | 
0.51 | 2 | 
0.52 | 1 | 
0.53 | 0 | 
0.54 | 1 | 
0.55 | 0 | 
0.56 | 1 | 
0.57 | 1 | 
0.58 | 1 | 
0.59 | 0 | 
0.60 | 3 | 
0.61 | 1 | 
0.62 | 1 | 
0.63 | 0 | 
0.64 | 3 | 
0.65 | 3 | 
0.66 | 4 | 
0.67 | 5 | 
0.68 | 0 | 
0.69 | 1 | 
0.70 | 2 | 
0.71 | 0 | 
0.72 | 1 | 
0.73 | 4 | 
0.74 | 1 | 
0.75 | 2 | 
0.76 | 0 | 
0.77 | 2 | 
0.78 | 1 | 
0.79 | 2 | 
0.80 | 3 | 
0.81 | 1 | 
0.82 | 1 | 
0.83 | 2 | 
0.84 | 4 | 
0.85 | 7 | 
0.86 | 4 | 
0.87 | 2 | 
0.88 | 5 | 
0.89 | 5 | 
0.90 | 3 | 
0.91 | 0 | 
0.92 | 6 | 
0.93 | 4 | 
0.94 | 1 | 
0.95 | 3 | 
0.96 | 2 | 
0.97 | 5 | 
0.98 | 12 | 
0.99 | 8 | 
1.00 | 28 | 
1.01 | 0 | 

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
| Apache | 2.2.0 | 0.81% |
| | 2.2.3 | 0.82% |
| | 2.2.6 | 0.81% |
| | 2.2.9 | 0.63% |
| | 2.2.11 | 0.63% |
| | 2.2.13 | 0.58% |
| | 2.2.15 | 0.38% |
| | 2.2.17 | 0.35% |
| | 2.2.20 | 0.36% |
| | 2.2.22 | 0.62% |
| | 2.4.2 | 0.81% |
| | 2.4.4 | 0.84% |
| | 2.4.7 | 0.70% |
| | 2.4.10 | 0.57% |
| | 2.4.16 | 0.54% |
| | 2.4.18 | 0.44% |
| | 2.4.23 | 0.39% |
| | 2.4.27 | 0.38% |
| | 2.4.33 | 0.34% |
| | 2.4.35 | 0.34% |
| | 2.4.38 | 0.35% |
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
| VP8 | v0.9.1 | 6.33% |
| | v0.9.2 | 4.16% |
| | v0.9.5 | 4.15% |
| | v0.9.6 | 1.29% |
| | v0.9.7 | 2.50% |
| | v0.9.7-p1 | 0.99% |
| | v1.0.0 | 0.65% |
| | v1.1.0 | 0.56% |
| | v1.2.0 | 0.79% |
| | v1.3.0 | 0.78% |
| | v1.4.0 | 1.13% |
| | v1.5.0 | 1.19% |
| | v1.6.1 | 2.26% |
| | v1.7.0 | 2.31% |
| | v1.8.0 | 2.59% |
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
| VP9 | v1.3.0 | 0.64% |
| | v1.4.0 | 2.36% |
| | v1.5.0 | 8.46% |
| | v1.6.0 | 1.82% |
| | v1.6.1 | 1.69% |
| | v1.7.0 | 1.45% |
| | v1.8.0 | 2.45% |
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
| z3 | 4.3.2 | 1927.29% |
| | 4.4.0 | 1.34% |
| | last-pure-pure | 1.52% |
| | last-pure-unstable | 1.59% |
| | 4.4.1 | 1.34% |
| | 4.5.0 | 1.41% |
| | 4.6.0 | 1.81% |
| | 4.7.1 | 1.86% |
| | 4.8.1 | 3.45% |
| | 4.8.3 | 2.12% |
| | 4.8.4 | 2.54% |
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

Note that the error rate of predicting release 4.3.2 of z3 is abnormally high. This is because a few configurations couldn't be predicted well (estimate: 0,6 seconds; actual: 56 seconds) by using our setting. In the paper, we have not considered this error rate. However, including this error rate would result in 13% error rate on average, which is still small. Also note that we only use the performance-influence models to investigate which configuration options are causing performance changes.

Case Studies | AbsoluteInfluence| InfluenceDifference| 
--- | --- | --- | 
Apache| [1](./RQ2/Apache/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/Apache/InfluenceDifference/influenceDifference.pdf) | 
brotli| [1](./RQ2/brotli/AbsoluteInfluence/configurationsInfluence.pdf) | [1](./RQ2/brotli/InfluenceDifference/influenceDifference.pdf) | 
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
%Changes | Frequency | 
 :----: |  :----: | 
0 | 8507 | 
1 | 827 | 
2 | 406 | 
3 | 259 | 
4 | 144 | 
5 | 128 | 
6 | 162 | 
7 | 102 | 
8 | 98 | 
9 | 41 | 
10 | 50 | 
11 | 44 | 
12 | 53 | 
13 | 24 | 
14 | 26 | 
15 | 13 | 
16 | 7 | 
17 | 21 | 
18 | 10 | 
19 | 2 | 
20 | 5 | 
21 | 1 | 
22 | 4 | 
23 | 5 | 
24 | 4 | 
25 | 7 | 
26 | 10 | 
27 | 11 | 
28 | 5 | 
29 | 8 | 
30 | 1 | 
31 | 1 | 
32 | 6 | 
33 | 2 | 
34 | 10 | 
35 | 2 | 
36 | 3 | 
37 | 6 | 
38 | 1 | 
39 | 4 | 
40 | 3 | 
41 | 0 | 
42 | 1 | 
43 | 0 | 
44 | 21 | 
45 | 3 | 
46 | 0 | 
47 | 0 | 
48 | 2 | 
49 | 0 | 
50 | 1 | 
51 | 1 | 
52 | 0 | 
53 | 2 | 
54 | 1 | 
55 | 21 | 
56 | 0 | 
57 | 0 | 
58 | 0 | 
59 | 0 | 
60 | 0 | 
61 | 0 | 
62 | 0 | 
63 | 0 | 
64 | 0 | 
65 | 0 | 
66 | 0 | 
67 | 0 | 
68 | 0 | 
69 | 0 | 
70 | 0 | 
71 | 0 | 
72 | 0 | 
73 | 0 | 
74 | 0 | 
75 | 0 | 
76 | 0 | 
77 | 0 | 
78 | 0 | 
79 | 0 | 
80 | 0 | 
81 | 0 | 
82 | 0 | 
83 | 0 | 
84 | 0 | 
85 | 0 | 
86 | 0 | 
87 | 0 | 
88 | 0 | 
89 | 0 | 
90 | 0 | 
91 | 0 | 
92 | 0 | 
93 | 2 | 
94 | 2 | 
95 | 4 | 
96 | 5 | 
97 | 2 | 
98 | 1 | 
99 | 1 | 
100 | 0 | 

Similarly to the table in RQ1.1, we obtain the following values for changing terms:
%Changes | Frequency | 
 :----: |  :----: | 
0 | 113 | 
1 | 2 | 
2 | 2 | 
3 | 2 | 
4 | 0 | 
5 | 2 | 
6 | 3 | 
7 | 1 | 
8 | 5 | 
9 | 1 | 
10 | 2 | 
11 | 3 | 
12 | 2 | 
13 | 1 | 
14 | 1 | 
15 | 2 | 
16 | 0 | 
17 | 1 | 
18 | 1 | 
19 | 4 | 
20 | 0 | 
21 | 1 | 
22 | 1 | 
23 | 1 | 
24 | 1 | 
25 | 0 | 
26 | 1 | 
27 | 3 | 
28 | 1 | 
29 | 0 | 
30 | 1 | 
31 | 1 | 
32 | 1 | 
33 | 5 | 
34 | 0 | 
35 | 0 | 
36 | 0 | 
37 | 0 | 
38 | 1 | 
39 | 0 | 
40 | 0 | 
41 | 0 | 
42 | 0 | 
43 | 0 | 
44 | 0 | 
45 | 0 | 
46 | 0 | 
47 | 0 | 
48 | 0 | 
49 | 0 | 
50 | 1 | 
51 | 0 | 
52 | 1 | 
53 | 0 | 
54 | 1 | 
55 | 0 | 
56 | 0 | 
57 | 2 | 
58 | 0 | 
59 | 0 | 
60 | 2 | 
61 | 0 | 
62 | 1 | 
63 | 0 | 
64 | 0 | 
65 | 0 | 
66 | 0 | 
67 | 0 | 
68 | 0 | 
69 | 0 | 
70 | 0 | 
71 | 1 | 
72 | 0 | 
73 | 0 | 
74 | 0 | 
75 | 1 | 
76 | 0 | 
77 | 1 | 
78 | 1 | 
79 | 0 | 
80 | 0 | 
81 | 0 | 
82 | 0 | 
83 | 0 | 
84 | 0 | 
85 | 1 | 
86 | 0 | 
87 | 0 | 
88 | 0 | 
89 | 0 | 
90 | 1 | 
91 | 0 | 
92 | 1 | 
93 | 0 | 
94 | 0 | 
95 | 2 | 
96 | 0 | 
97 | 0 | 
98 | 0 | 
99 | 0 | 
100 | 0 | 

## RQ2.2: How stable is the relative influence of configuration options and interactions in the presence of performance changes between consecutive releases?

Case Studies | Ranking| 
--- | --- | 
Apache| [1](./RQ2/Apache/Ranking/influenceRanking.pdf) | 
brotli| [1](./RQ2/brotli/Ranking/influenceRanking.pdf) | 
HSQLDB| [1](./RQ2/HSQLDB/Ranking/influenceRanking.pdf) | 
lrzip| [1](./RQ2/lrzip/Ranking/influenceRanking.pdf) | 
OpenVPN| [1](./RQ2/OpenVPN/Ranking/influenceRanking.pdf) | 
Opus| [1](./RQ2/Opus/Ranking/influenceRanking.pdf) | 
PostgreSQL| [1](./RQ2/PostgreSQL/Ranking/influenceRanking.pdf) | 
VP8| [1](./RQ2/VP8/Ranking/influenceRanking.pdf) | 
VP9| [1](./RQ2/VP9/Ranking/influenceRanking.pdf) | 
z3| [1](./RQ2/z3/Ranking/influenceRanking.pdf) | 

We have obtained the folliwing Kendall Tau values:

Kendall Tau value | Frequency | 
 :----: |  :----: | 
-1.00 | 0 | 
-0.99 | 0 | 
-0.98 | 0 | 
-0.97 | 0 | 
-0.96 | 0 | 
-0.95 | 0 | 
-0.94 | 0 | 
-0.93 | 0 | 
-0.92 | 0 | 
-0.91 | 0 | 
-0.90 | 0 | 
-0.89 | 0 | 
-0.88 | 0 | 
-0.87 | 0 | 
-0.86 | 0 | 
-0.85 | 0 | 
-0.84 | 0 | 
-0.83 | 0 | 
-0.82 | 0 | 
-0.81 | 0 | 
-0.80 | 0 | 
-0.79 | 0 | 
-0.78 | 0 | 
-0.77 | 0 | 
-0.76 | 0 | 
-0.75 | 0 | 
-0.74 | 0 | 
-0.73 | 0 | 
-0.72 | 0 | 
-0.71 | 0 | 
-0.70 | 0 | 
-0.69 | 0 | 
-0.68 | 0 | 
-0.67 | 0 | 
-0.66 | 0 | 
-0.65 | 0 | 
-0.64 | 0 | 
-0.63 | 0 | 
-0.62 | 0 | 
-0.61 | 0 | 
-0.60 | 0 | 
-0.59 | 0 | 
-0.58 | 0 | 
-0.57 | 0 | 
-0.56 | 0 | 
-0.55 | 0 | 
-0.54 | 0 | 
-0.53 | 0 | 
-0.52 | 0 | 
-0.51 | 0 | 
-0.50 | 0 | 
-0.49 | 0 | 
-0.48 | 0 | 
-0.47 | 0 | 
-0.46 | 0 | 
-0.45 | 0 | 
-0.44 | 0 | 
-0.43 | 0 | 
-0.42 | 1 | 
-0.41 | 0 | 
-0.40 | 0 | 
-0.39 | 0 | 
-0.38 | 0 | 
-0.37 | 0 | 
-0.36 | 0 | 
-0.35 | 0 | 
-0.34 | 0 | 
-0.33 | 1 | 
-0.32 | 0 | 
-0.31 | 0 | 
-0.30 | 0 | 
-0.29 | 0 | 
-0.28 | 0 | 
-0.27 | 0 | 
-0.26 | 0 | 
-0.25 | 0 | 
-0.24 | 1 | 
-0.23 | 0 | 
-0.22 | 0 | 
-0.21 | 0 | 
-0.20 | 0 | 
-0.19 | 0 | 
-0.18 | 0 | 
-0.17 | 0 | 
-0.16 | 0 | 
-0.15 | 0 | 
-0.14 | 0 | 
-0.13 | 0 | 
-0.12 | 0 | 
-0.11 | 1 | 
-0.10 | 0 | 
-0.09 | 0 | 
-0.08 | 0 | 
-0.07 | 0 | 
-0.06 | 0 | 
-0.05 | 0 | 
-0.04 | 0 | 
-0.03 | 0 | 
-0.02 | 1 | 
-0.01 | 0 | 
0.00 | 2 | 
0.01 | 0 | 
0.02 | 0 | 
0.03 | 0 | 
0.04 | 0 | 
0.05 | 0 | 
0.06 | 0 | 
0.07 | 1 | 
0.08 | 0 | 
0.09 | 0 | 
0.10 | 0 | 
0.11 | 0 | 
0.12 | 0 | 
0.13 | 0 | 
0.14 | 0 | 
0.15 | 0 | 
0.16 | 0 | 
0.17 | 0 | 
0.18 | 0 | 
0.19 | 0 | 
0.20 | 0 | 
0.21 | 1 | 
0.22 | 0 | 
0.23 | 0 | 
0.24 | 1 | 
0.25 | 0 | 
0.26 | 0 | 
0.27 | 0 | 
0.28 | 0 | 
0.29 | 0 | 
0.30 | 0 | 
0.31 | 0 | 
0.32 | 0 | 
0.33 | 1 | 
0.34 | 0 | 
0.35 | 1 | 
0.36 | 0 | 
0.37 | 0 | 
0.38 | 1 | 
0.39 | 0 | 
0.40 | 0 | 
0.41 | 1 | 
0.42 | 0 | 
0.43 | 0 | 
0.44 | 0 | 
0.45 | 0 | 
0.46 | 0 | 
0.47 | 0 | 
0.48 | 0 | 
0.49 | 0 | 
0.50 | 0 | 
0.51 | 0 | 
0.52 | 0 | 
0.53 | 0 | 
0.54 | 0 | 
0.55 | 0 | 
0.56 | 0 | 
0.57 | 0 | 
0.58 | 0 | 
0.59 | 0 | 
0.60 | 1 | 
0.61 | 1 | 
0.62 | 2 | 
0.63 | 0 | 
0.64 | 0 | 
0.65 | 0 | 
0.66 | 0 | 
0.67 | 1 | 
0.68 | 0 | 
0.69 | 1 | 
0.70 | 0 | 
0.71 | 0 | 
0.72 | 1 | 
0.73 | 1 | 
0.74 | 0 | 
0.75 | 0 | 
0.76 | 2 | 
0.77 | 0 | 
0.78 | 2 | 
0.79 | 1 | 
0.80 | 2 | 
0.81 | 1 | 
0.82 | 0 | 
0.83 | 2 | 
0.90 | 2 | 
0.91 | 0 | 
0.92 | 0 | 
0.93 | 1 | 
0.94 | 1 | 
0.95 | 1 | 
0.96 | 1 | 
0.97 | 2 | 
0.98 | 2 | 
0.99 | 2 | 
1.00 | 148 | 
1.01 | 0 |  
0.84 | 1 | 
0.85 | 1 | 
0.86 | 0 | 
0.87 | 0 | 
0.88 | 0 | 
0.89 | 1 | 
0.90 | 2 | 
0.91 | 0 | 
0.92 | 0 | 
0.93 | 1 | 
0.94 | 1 | 
0.95 | 1 | 
0.96 | 1 | 
0.97 | 2 | 
0.98 | 2 | 
0.99 | 2 | 
1.00 | 148 |