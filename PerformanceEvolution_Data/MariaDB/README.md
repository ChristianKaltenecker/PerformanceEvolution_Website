# MySQL & MariaDB (pervolution)

Discretized results available in [MySQL_MariaDB_pervolution_bin](../MySQL_MariaDB_pervolution_bin).

## Case Study Information

- software: MySQL and MariaDB
- cluster: zeus
- benchmark/workload: oltp_read_write scenario of sysbench 1.0.17 with 10000 events
- configurations: 972
- revisions:
    - mariadb: 22
    - mysql: 20
- properties:
  - performance (run time)
  - cpu load
- notes:
  - 5 repetitions
  - < 10% relative standard deviation for property performance
  - same configuration space for both MySQL and MariaDB
  - there is a gap in the selected revision space of MariaDB due to the following versions crashing at runtime:
    - 10.0.10 - 10.0.17
    - 10.1.18 - 10.1.23

## Measurements Information

- average relative standard deviations:
  - performance: 6.38 %
- relative standard deviations available in separate files
- discretized results available

