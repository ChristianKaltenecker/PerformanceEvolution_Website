# Performance Evolution

We focus on configuration options that were enabled/disabled in our measurements.

## PostgreSQL

Is the case study that is abnormal in comparison to the other case studies since it has only three configuration options with an influence on the performance, namely $\textsf{root}$, $\textsf{fsync}$, and $\textsf{trackActivities}$.
From 5 performance changes, 4 are from $\textsf{root}$ (8.3.5 -> 8.4.0; 9.0.4 -> 9.1.0; 9.1.3 -> 9.2.0; 9.2.4 -> 9.3.0) and 1 is from the configuration option $\textsf{fsync}$ (9.0.0 -> 9.0.4).

### Interesting Insights in the Paper
* outlier case study because of only 3 terms that have an influence (Figure 4)

### Configuration Options with a Change
* root
    * 8.3.5 -> 8.4.0 (speed up)
    * 9.0.4 -> 9.1.0 (slow down)
    * 9.1.3 -> 9.2.0 (speed up)
    * 9.2.4 -> 9.3.0 (slow down)
* fsync
    * Forces synchronization of updates to disk. Having fsync disabled could lead to an unrecoverable data corruption in case of a power failure or system crash. 
    * 9.0.0 -> 9.0.4 (massive slow down)
    In version 9.0.2, the wal_sync_method was forced to fdatasync since kernel changes lead PostgreSQL to choose open_datasync instead. In our case, our kernel version lead to choose to open_datasync, which is considered unsafe (i.e., data may not be necessarily written on disk) in Linux. Beginning from version 9.0.2, PostgreSQL forces fdatasync. This turns out to be much slower since it doesn't use a write buffer but blocks until the data is written on the disk. 

### Commit messages

9.0.0 -> 9.0.4 [REL9_0_0 -> REL9_0_4]:
* 87eadd7e3d6f: Force default wal_sync_method to be fdatasync on Linux
* 1435a8554: Flush the WAL received before exiting

## z3

This case study is also interesting, because from version 4.5.0 to 4.6.0, all configurations change. A reason for this performance change could be that the behavior of optimization commands for the SMT2 command-line interface has changed in version 4.6.0. In the same version, a new linear real arithmetic solver was introduced. Interestingly, not only the overall performance changes, but also the performance of the configuration option $\textsf{proof}$ is degraded by roughly 200%. 
$\textsf{proof}$ generates an object that provides more information about why a certain formula is valid or not (https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/nbjorner-iwil08.pdf).

In version 4.8.1, a single configuration was executed in 20 seconds on zeus (Passau); unfortunately, I can not reproduce that although I use the same configuration and workload. Software version, kernel version, hardware?
QF_FP, proof, model_validate, unsat_core, smtlib2_compliant, partial, euclidean_solver

The error rate is also very high in the first release, because of a few configurations which couldn't be predicted well (estimate: 0.6 seconds; actual: 56 seconds). This anomaly appears only in this release.

### Configuration Options with a Change
* root
    * 4.5.0 -> 4.6.0 (slow down by 50%)
* proof 
    * 4.5.0 -> 4.6.0 (massive slow down) 
    * proof utilities code was moved between these versions
    * some regressions were fixed regarding proof dependencies
* (model_validate/euclidean_solver/"") * proof * smtlib2_compliant * unsat_core * well_sorted check
    * Appear in different versions -- usually each term has an influence of ~ 1%
    * 4.3.2 -> 4.4.0
    * 4.5.0 -> 4.6.0
    * 4.6.0 -> 4.7.1
    * 4.7.1 -> 4.8.1
    * 4.8.1 -> 4.8.3
    * 4.8.3 -> 4.8.4

### Commit messages and changelog

Changelog: https://github.com/Z3Prover/z3/blob/master/RELEASE_NOTES

4.3.2 - 4.4.0:
* Configuration options/Interactions: QF_LRA (Unquantified linear real arithmetic -- speedup), QF_LRA * proof (speedup)
* Changelog: Reports changes on QF_FP; No speedup mentioned
* Commits: 
  * 1e30fd2c65d
  * 89c43676d5719
  * 44e647e72b
  * 2aa91eee705
* Configuration options not mentioned


4.4.0 - 4.4.1:
* Configuration options/Interactions: QF_FP * proof (speedup)
* Changelog: No speedup mentioned
* Commits:
  * eeef4d29d8285
  * 759d80dfe371
  * 73a8f9960f2641
  * a44044fb156cd2c13
  * e180cfe256ecd
  * 478b3160ace
  * 54c959783d0e83
  * e1e27f2c26474
  * b9287343487f
  * 5fdc104f8247d60e
* Configuration option proof mentioned multiple times

4.4.1 - 4.5.0:
* Configuration options/Interactions: QF_FP * proof (slowdown), QF_FP (slowdown)
* Changelog: Reports changes on LRA (new solver); no speedup reported
* Commits:
  * cc6769c8664
  * c1aa33339d2e95c
  * c693c990df9e2babb
  * 43202572ee73b
  * ac902dad1a1022
* Configuration option proof mentioned multiple times

4.5.0 - 4.6.0:
* Configuration options/Interactions: QF_FP (speedup), QF_FP * proof (speedup), QF_LRA * proof (slowdown), QF_UFLRA (slowdown), QF_UFLRA * proof (slowdown)
* Changelog: Mentions changes of a new linear arithmetic solver; no speedups reported
* Commits:
  * fbaee08: fix performance regression introduced with theory_str; theory_str slows down things
  * 72c9134424c973: fixing regressions introduced when reducing astm proof dependencies
  * d67f3c14668b8f
* Configuration option proof mentioned regarding speedup

4.6.0 - 4.7.1:
* Configuration options/Interactions: QF_UFLRA * proof (speedup), QF_LRA (speedup), QF_UFLRA (speedup)
* Changelog: Reports breaking changes but no speedups
* Commits: Nothing directly related to runtime performance
  * 9e8192e44811bcfad99866932480619d8e8512af (Speed-up)
  * B5d531f079d6b678dc8accf6fd165185361c18d6 (Speed-up)
  * a1d870f19f6638432eb5f15f0f1a59319a9927ab (Workload mentioned)
  * fc835ba01e5285ceb4c15ec8fa6eb1eb90d6e5ba (Configuration option mentioned)
* Configuration options mentioned


4.7.1 - 4.8.1:
* Configuration options/Interactions: QF_LRA * proof (speedup), QF_LRA (slowdown)
* Changelog: No speedup reported
* Commits:
  * 49e94809282eee4d
  * 16d4e2f5d1b2de3
  * e0d69a0033bcc
  * 4695ca16c84aa0
* Configuration option proof mentioned regarding speedup

4.8.3 - 4.8.4:
* Configuration options/Interactions: QF_UFLRA * proof (slowdown)
* Changelog: Speedups reported but not in relation to configuration option
* Commits: 
  * 9e5aaf074e248084
  * bfcea7a8198ef
* Configuration options not mentioned

4.8.4 - 4.8.5:
* Configuration options/Interactions: QF_FP * proof (speedup), QF_LRA (speedup)
* Changelog: Nothing relevant mentioned
* Commits:
  * 73f6806371e494c (speed-up mentioned)
  * 893e60459369e1b781c3d99015c03d2089dd8c5e (found configuration option proof)
* Configuration option mentioned

4.8.5 - 4.8.6:
* Configuration options/Interactions: QF_UFLRA (slowdown), QF_UFLRA * proof (slowdown)
* Changelog: Nothing relevant mentioned
* Commits: 
  * 43a19cadf6c
* Configuration option mentioned

4.8.6 - 4.8.7:
* Configuration options/Interactions: Nothing
* Changelog: Nothing relevant mentioned
* Commits:
  * 18fe28c0f0db547e
* Configuration option not mentioned

4.8.7 - 4.8.8:
* Configuration options/Interactions: QF_LRA * proof (speedup), QF_UFLRA * proof (speedup), QF_UFLRA * model_validate (slowdown), QF_UFLRA (slowdown)
* Changelog: (PROBABLE REGRESSION REPORTED!) Only regression reported; no speedup
* Commits:
  * 0f2c8c21ff955713a4 (speed-up reported)
  * 140926e7c0ea0e52 (perf regression reported)
  * 20d72e5d9771e4d2efca568ccba767d982af6cbc (Configuration option proof mentioned)
* Configuration options not mentioned directly in relation to performance, but mentioned


4.8.8 - 4.8.9:
* Configuration options/Interactions: QF_UFLRA * model_validate * proof (speedup), QF_LRA * proof (speedup), QF_UFLRA * proof (slowdown), QF_UFLRA * model_validate (slowdown), QF_LRA (slowdown), QF_UFLRA (speedup)
* Changelog: Another potential regression reported through a new arithmetic theory
* Commits:
  * 1fd567d1e9a8bfeea2f7a72de7011b6e8d06edfa (Speed-up reported)
  * 07a1aea689f9c2dff0f74a1b61940d04155cba39 (Configuration option proof mentioned)
* Configuration options mentioned

4.8.9 - 4.8.10:
* Configuration options/Interactions: QF_LRA * proof (slowdown), QF_UFLRA (slowdown)
* Changelog: default solver replaced, but nothing regarding performance reported
* Commits:
  * a95c35dadbfdcc86
* Configuration option mentioned


4.8.10 - 4.8.11:
* Configuration options/Interactions: QF_LRA * proof (slowdown), QF_UFLRA * proof (speedup), QF_UFLRA * model_validate (speedup), QF_UFLRA (slowdown)
* Changelog: Nothing directly related to performance is mentioned
* Commits:
  * 52e67b0d3edb3f
  * 4a8ba8b1609044
  * cc001ad6825074743
  * 998cf4c726258fa (regression mentioned!)
  * 7869cdbbc88a70d018218729654
  * 6aa766a5448db9
  * 8c66691e6d411d9aa0e092843339d7f80983d39a (Configuration option proof mentioned)
* Configuration options not mentioned in relation to performance, but mentioned


4.8.11 - 4.8.12:
* Configuration options/Interactions: QF_LRA (speedup)
* Changelog: Nothing directly related to performance is mentioned
* Commits: 
 * Nothing
* Configuration options not mentioned

4.8.12 - 4.8.13:
* Configuration options/Interactions: QF_LRA * proof (slowdown), QF_UFLRA (speedup)
* Changelog: Nothing directly related to performance is mentioned
* Commits:
  * ed27ce5526bb4b42
  * 3e6ff768a58f072
  * 4dad41416136ab
  * 63ac2ee0d1377
* Configuration options not reported

## brotli

This case study has multiple configuration options with numeric values. In one release and one single numeric value of a certain configuration option, there is a performance bug which is confirmed by the changelog.
The base code (i.e., all other code that is not related to window size or the compression level) shows no significant changes over time; only some configuration options and interactions.
The most changes are between releases 0.3.0-0.4.0 and 0.4.0-0.5.2 with these three releases being the only significant in this case study.

###  Intersting 

The release 0.4.0 reduced the execution time for the compression levels 0,1,2,3,10, and 11 compared to release 0.3.0.
However, in compression levels 0 and 1, the window sizes of 10 and 11 resulted in a slow down.
Between release 0.4.0 and 0.5.2, the execution time of the compression levels 1 and 5 to 10 was even further reduced.
This behavior is also visible in the performance-influence models.

Some performance bugs (according to the changelog) also happen when uncompressing a file. We, however, have measured only the time for compression.

## Commit messages
0.3.0 - 0.4.0 (low quality compression also mentioned in the changelog):
* Changelog: made low quality compression faster; added quality level 0; 
* Commits:
  * 1f01d61bcf: Add two more fast modes (quality 0, 1); quality 1,2 were renamed to quality 2 and 3 and the old quality 3 is removed.
  * f453b1bf36 [only memory]: Reduce memory usage
  * 27688e605c: Faster entropy coding phase for quality 1
  * 4dd9114c97: Partial Hasher initialization for small input data (does not apply; our data is bigger than only 1KB)
* Configuration option mentioned regarding performance change

0.4.0 - 0.5.2:
* Changelog: Nothing
* Commits:
  * 2048189048: new hasher; improved speed and reduced memory usage for q:5-9 w 10-16
* Configuration option mentioned

0.5.2 - 0.6.0 (better compression on 1MB+ files, faster compression on mid-low quality levels; fix encoder q10-11 slowdown):
* Changelog: Nothing
* Commits:
  * 5db62dcc: Fix slow-down after a long copy (q10-11)
  * 0a63f99db: Limit for window size for q0-1 and use fix shifts for the hashes
  * 8a06e0293: Improve the compression
* Configuration option mentioned

0.6.0 - 1.0.0:
* Changelog: Nothing
* Commits:
  * a629289e: speedup compression for RLEish (Run Length Encoding) data
* Configuration option not mentioned

1.0.0 - 1.0.1 (only one day in between): 
* Changelog: Nothing
* Commits:
  * Nothing
* Configuration option not mentioned

1.0.1 - 1.0.2 (changes of the terms are higher than 5% and therefore, this release was chosen):
* Changelog: Nothing
* Commits:
  * 39ef4bbdc: add new (fast) dictionary generator "Sieve"
* Configuration option not mentioned

1.0.2 - 1.0.3:
* Changelog: Improved compression ratio; Nothing related to performance
* Commits:
  * 35e69fc7c: New dictionary generator with the speed of "Sieve" and the quality of "DM" -> does not necessarily imply that the speed of the new dictionary generator is better than before.
  * da254cffdb: Fix q=10 1-byte input compression
* Configuration option mentioned

1.0.3 - 1.0.4 (1 month 1 week in between):
* Changelog: better compression; Nothing related to performance
* Commits:
  * 0f3c84e7e: better compression (similar to changelog)
* Configuration option not mentioned

1.0.4 - 1.0.5:
* Changelog: q=1 compression on small files improved
* Commits:
  * 68db5c027: improve q=1 compression on small files
* Configuration option mentioned

1.0.6 - 1.0.7:
* Changelog: focuses on ARM architecture; Nothing regarding x86 architecture
* Some speedup detected in configuration options: CompressionLevel_9 * WindowSize_24; CompressionLevel 9 * WindowSize_23; CompressionLEvel_9 * WindowSize_22; CompressionLEvel_10 * WindowSize_19
* Commits:
 * Nothing
* Configuration option not mentioned

## OpenVPN

This case study (along with PostgreSQL) has a release (2.2.1 -- 2.2.2) where no configurations have changed. Generally, the performance of OpenVPN is very stable with 2 exceptions:
* 2.2.2 - 2.3.0
* 2.3.9 - 2.4.0

### Commit messages
2.2.2 - 2.3.0
* Configuration Options/Interaction: lzo (speed up); sha512 (speed up)
* Changelog:
  * Fix reconnection issues when push and UDP (we use tcp in our setup).
  * They also fixed some regressions happening in configuration options we do not use (e.g., --http-proxy).
  * Modified create_socket_tcp.

* Commits:
  * 74bbc7: build: proper lzo detection and usage (?)
* Configuration option mentioned

2.3.9 - 2.4.0:
* Configuration Options/Interaction: base (slow down); lzo and sha512 (speed up); SHA1 (slow down); SHA512 * LZO (slow down)
* Changelog: 
  * In 2.3.10: Fix regression in setups without a client certificate
* Commits:
  * b59fc7f: Fix missing return value checks; should become faster
  * fc91d4b: Increase control channel packet size for faster handshakes
  * 160504a29: Refactor CRL (certificate revocation list) handling
  * 985156e: Fix --cipher=none regression
  * 65eedc35: Make sure float won't happen if hmac check failed (regression)
  * af1e4d26: switch to SHA256 instead of SHA1
  * dd2fbc26: sha1 returns correct SHA1 fingerprint
  * 5d523377: Disable SSL compression
* Configuration option mentioned


## Opus

Just stable... no performance changes here.

## lrzip
With 220 different configuration options and interactions thereof, it is hard to tell which configuration option or interaction caused the influence and whether it was positive/negative.
This turns out to be a drawback since it makes tracking difficult.

* Changelog: https://github.com/ckolivas/lrzip/blob/master/ChangeLog

### Releases
530 - 543 (configurations stay the same or have a massive slow down):
* Configuration Options/Interactions: compression(Lzo,Gzip,Lzma) * processorCount(2,4,8), level 3-9; processorCount_4 slow down
* Changelog: 540-543: fixes and speedup;
* Commits:
  * 692949287: Sliding mmap was causing a slowdown of death
  * 2b08c6e280: Fix the output of zpaq compress and decompress
* Configuration option is mentioned


543 - 544 (some configurations have a speed up, some a slow down -- major change):
* Configuration Options/Interaction: same as 530. processorCount_4 slowed down when using different compressions; reverts some changes from 543; some are even worse (compressionLZMA * processorCount_8); hard to tell
* Changelog: speed ups are mentioned
* Commits:
  * 688aa55c7930: Spawn threads in regular intervals; speeds up compression
* Configuration option is mentioned regarding speed-up


544 - 550 (configurations stay the same or are speeded up -- major change):
* Changelog: speed up mentioned
* Commits:
  * 8dd9b00: Reverted 688aa55c7 because it was not only resuling in a speed up but also in a slow down
  * 50437a84: Improves threading by bringing it higher up in the code.
  * e0265b33: Rescales the lzma levels and brings a speed up to lzma
* Configuration option lzma and threading mentioned regarding speed-up

551 - 552:
* Changelog: no performance changes are reported.
Focus on decompression.
* Commits:
  * 8d110e3366d: Check that thread really exited before moving on
* Configuration option mentioned

552 - 560 (major change):
* Changelog: speed ups reported
* Commits:
  * 7287ab8a6: md5 process bytes saving time
  * 4036125f947: Make the buffer sized, speedup
* Configuration option not mentioned

560 - 571 (speed up -- major change):
* Changelog: 0.570: Multithreading speedup; 
* Commits:
  * f9f880908c: Small slow down by removing fragile exponential growth buffer size
  * bb33f7571cc: Speeding up multi-threading
* Configuration option mentioned regarding speed-up

571 - 601 (slow down -- major change):
* Changelog: no speed up/slow down reported
* Commits:
  * 643054ae: Fix threading error (?)
* Configuration option mentioned

601 - 602:
* Changelog: nothing relevant reported
* Commits:
  * Nothing
* Configuration option not mentioned

602 - 604:
* Changelog: Nothing relevant reported
* Commits:
  * 7ed977b1c1: Detach threads from the compression side
* Configuration option mentioned

604 - 606:
* Changelog: Nothing relevant supported
* Commits:
  * d033743e6f: Reverts 
* Configuration option not mentioned

606 - 607 (speed up):
* Changelog: Nothing relevant reported (except for the update to lzma 920)
* Commits:
  * 71bb72f5da: Update to lzma 920 library
* Configuration option mentioned

607 - 608 (speed up):
* Changelog: Speed up reported 2x
* Commits:
  * f496e0705: Speed up
* Configuration option not mentioned

608 - 611 (slow down and some speed up):
* Changelog: Speed up reported
* Commits:
  * f4165ec26
  * 2fada9fb
  * c136424
  * 0e593f768
  * 92c09a758
  * 5edf8471d1
  * dbc71eceb (slow down)
* Configuration option mentioned

612 - 614:
* Changelog: Nothing relevant reported
* Commits:
  * 081265f: No back end compression for blocks smaller than 64 bytes
* Configuration option mentioned

614 - 615:
* Changelog: Multiple micro-optimizations and several fixes but no clear relation to performance
* Commits:
  * 6f0410d28f
  * 87fe625829
* Configuration option not mentioned

620 - 621:
* Changelog: Microoptiomisation is reported; but no clear speed up /slow down
* Commits:
  * 9a17a54c: make high buffer only one page size faster
  * aa753fee: microoptimisation
  * f378595dc

## HSQLDB

Changelog: http://hsqldb.org/doc/2.0/changelist_2_0.txt

### Commit messages and changelog
2.1.0 - 2.2.0 (slow down):
* Configuration Options/Interactions: logSize (slow-down)
* Changelog: Only speed up reported (fixed regression)
* Commits:
  * Nothing
* Configuration option not mentioned


2.2.1 - 2.2.2 (speed up of some configurations):
* Configuration Options/Interactions: blowfish, logSize * blowFish * defragLimit
* Changelog: improved query speed
* Commits:
  * 796fa0ccedc: improved query speed
* Configuration option not mentioned

2.2.5 - 2.2.6 (slow down):
* Configuration Options/Interactions: mvcc
* Changelog: Fix of MVCC is mentioned (but no slow down)
* Commits:
  * 04db897bbc6: optimization (only speed up?)
* Configuration option mentioned

2.2.6 - 2.2.7:
* Configuration options: None
* Changelog: Nothing
* Commits:
  * 22f6fd2d8
* Configuration option not mentioned

2.2.9 - 2.3.0 (slow down and a few configurations sped up):
* Configuration Options/Interactions: blowFish * logSize_5 * defragLimit_50 (speed up); blowfish * defragLimit_100 * logSize 5 (slowdown) blowfish * cacheSize_10000 (slow down); blowfish * logSize_5 (speed up); blowfish (speed up)
* Changelog: Speed up reported; few regressions fixed; no slow down reported
* Commits:
  * Nothing
* Configuration option not mentioned


2.3.0 - 2.3.1 (some slow down, some speed up -- no changes in performance-influence model visible):
* Configuration Options/Interactions: None
* Changelog: Nothing mentioned
* Commits:
  * Nothing
* Configuration option not mentioned

2.3.1 - 2.3.2 (same configurations -- seems as changes are reverted -- no changes in performance-influence model visible):
* Configuration Options/Interactions: None
* Changelog: Nothing mentioned
* Commits:
  * Nothing
* Configuration option not mentioned

2.3.2 - 2.3.3 (slow down of specific configurations):
* Configuration Options/Interactions: defragLimit_50 * logSize_5 * blowfish
* Changelog: only regressions reported
* Commits:
  * Nothing
* Configuration option not mentioned

## MariaDB

Changelogs:
5.5-series: https://mariadb.com/kb/en/mariadb-galera-55-changelogs/
10.0-series: https://mariadb.com/kb/en/changelogs-mariadb-100-series/
10.2-series: https://mariadb.com/kb/en/changelogs-mariadb-102-series/


### Commit messages and changelog
5.5.23 - 5.5.27:
Configuration Options: delayedInnodbFlush (slowdown), dsyncFlush (slowdown), delayedInnodbFlush * dsyncFlush (speedup)
Changelog: They mention 2 fixes regarding flush in 5.5.24; Mentions a problem on ext3/ext4 on Linux so that fdatasync does not correctly sync all data in 5.5.27
Commits:
63f6c4e8fcd: change from fsync to fdatasync on Linux
598bb174677207475e34eb3c0632cab91f6dea9a: speed-up mentioned
ce7a3b43c80f8e6452713b799d5cae98af95bb7f: speed-up mentioned
Configuratiopn option mentioned+

5.5.35 - 5.5.38:
Configuration Options: dsyncFlush (slowdown), directFlush (speedup), delayedInnodbLogWrite * dsyncFlush (slowdown)
Changelog: Nothing relevant mentioned
Commits:
f01f49916b7a0: speed up mentioned; innodb storage mentioned
6db663d614: speed up mentioned
e1a30696034b70e3bf78036aa75a6e8389ebb2c4: mentions speed up
Configuration option is mentioned

5.5.40 (9.10.2014) - 10.0.17 (27.02.2015):
Configuration Options: delayedInnodbLogWrite * dsyncFlush (speed up), delayedInnodbLogFlush * dsyncFlush (slow down), delayedInnodbLogFlush (speed up), dsyncFlush (speed up)
Changelog: Hard to compare two major versions when they are developed in parallel; it seems that the changes from 5.5.23 - 5.5.27 are reversed (maybe the patch is missing?)
Commits: 11MB logs...
476a8660e: New version of InnoDB
87f5261039: Remove the innodb_flush_method fdatasync
cdf6d3ec047d30: flush mentioned
d8986fd6c3b69d2970e66684e1d00dd603fc9ab7: Speed up mentioned
53d44ad18b83dd59481ddaa71dcf8dc9e3446b83: Speed up mentioned
84fbabace0ad32c71c9317ff07b944adece92121: Speed up mentioned
Configuration option mentioned

10.1.16 (18.07.2016) - 10.2.6 (23.05.2017):
Configuration Options: delayedInnodbLogFlush (speed up)
Changelog: 10.2.4 mentions innodb and logging; for page compressed and encrypted tables log sequence number is not stored; this lead to a missmatch and some output in syslog
Commits: 
2d656793: Fix an issue where the json writer produced extra members in output; Configuration option mentioned; no speed up mentioned
fec844aca88: Newer version of InnoDB
850ed6e4cc9c4608844e5188b4be226fa63e2736: speed up mentioned
Configuration option mentioned

10.2.7 (12.07.2017) - 10.2.11 (28.11.2017):
Configuration Options: delayedInnodbLogFlush (slow down)
Changelog: 10.2.8: Revert an InnoDB Memcached from MySQL 5.6.37; Flushes redo log too often; there are many changes to Innodb, but it is unclear which one leads to a regression
Commits:
cb9648a6b5: Revert an InnoDB Memcached plugin fix; innodb mentioned; no speed up mentioned
3f24cf2dbdc3885f47a3ea84fc6383d3007cc996: speed up mentioned
A6c801438717b815288acb72513f5e42fe736b7b: speed up mentioned
Configuration option mentioned

## MySQL

### Commit messages and changelog

Changelog for 5.6: https://dev.mysql.com/doc/relnotes/mysql/5.6/en/
Changelog for 5.7: https://dev.mysql.com/doc/relnotes/mysql/5.7/en/
Changelog for 8.0: https://dev.mysql.com/doc/relnotes/mysql/8.0/en/

5.6.26 (24.07.2015) - 5.7.9 (21.10.2015):
Configuration options: binaryLog (slow down), binaryLog * delayedInnodbLogFlush (slow down)   -- they have a data dependency
Changelog:Multiple changes and fixes are mentioned regarding the binary log; also work on delayedInnodbLogFlush is mentioned but not related to binarylog
Commits:
5ece4a68df: Logging code was refactored in logging and binlogging
33ef855d4aaee: mentions flush and binary log together;
f00337956cd21: same
87c69291df1d422f9041645d9d27d2bccf6ff8a2: speed up mentioned
0b56f8cb6084e443421488902bc57b102683cd5b: speed up mentioned
Configuration option is mentioned


5.7.22 (19.04.2018) - 8.0.12 (27.07.2018):
Configuration options: delayedInnodbFlush (speed up), delayedInnodbFlush * dsyncFlush (slow down), Flush * Write * dsyncFlush (speed up), dsyncFlush (slow down), directFlush (slow down), binaryLog (speed up), innodbBufferPoolSize (speed up), directFlush * innodbBufferPoolSize (speed up)
Changelog: Mentions buffer size optimizations and speed ups in larger sorts
215f4439e1da855: InnoDB startup refactoring; includes buffer_size
2bd59f6e54cb152d539c46aa52a3b6507fb10bca: Speed-up mentioned
c5768818b32fdc65aec9118b1fe7e63205eefd45: Speed-up mentioned
71b0c585173257ff7a27f0cebe562f69ada2720a: Speed-up mentioned
200bf464776319dd2619cd7dc398d53c5e2e958b: Speed-up mentioned
79f49360dca75e6495cd104fc651a7db4212e6be: Speed-up mentioned
Configuration option is mentioned

8.0.13 - 8.0.15:
Configuration options: delayedInnodbLogFlush (speedup), delayedInnodbLogFlush * dsyncFlush (slowdown), delayedInnodbLogFlush * directFlush (speedup)
Changelog: Mentiones speedup
Commits: 
2809dd8df525: Speed-up mentioned
b0955c74d4d027f2838ae6c48cd3dfbed639cbaf: Speed-up mentioned
Configuration option is mentioned

## VP8
Shares the same repository with VP9.

### Commit messages and changelogs
0.9.1 - 0.9.2:
Configuration options: twoPass (speed up), bestQuality (speed up), goodQuality(speed up), constantBitrate * twoPass (speed up), bestQuality * noAltRef (speed up), constantBitrage * threads * twoPass (slow down)...
Changelog: Mentions a fix of two-pass for y4m input, mentions speed improvements
Commits:
e105e245e: Fix framrate for Y4M input; configuration option mentioned
Configuration option mentioned


0.9.2 - 0.9.5:
Configuration options: constantBitrate * twoPass (speed up), twoPass (minor slow down)
Changelog: only minor speed improvements for encoder mentioned, but more in relation to bestQuality; mentions changes for two pass.
Commits:
ff3068d6d: Change on two pass.
788c0eb5: Tune effect of motion in two pass
Configuration option mentioned

0.9.5 - 0.9.6:
Configuration options: bestQuality (speed up), goodQuality (speed up), twoPass (speed up), constantBitrate * goodQuality (speed up), bestQuality * constantBitrage (slow down)
Changelog: Mentions the speed improvement on bestQuality and goodQuality on x86 architecture
Commits:
b095d9df3c: Adjustment to boost calculation in two pass
3c18a2bb2e: Performance improvement in first pass
ff4a71f4c: boost for good quality mode
cec6a596b: A change should also help in speeding up the quality modes
13db80c2823: Improved performance of good quality
19054ab6da: Redefined good quality settings
431dac08d: Disabled some features for first pass
Configuration option mentioned

0.9.6 - 0.9.7:
Configuration options: goodQuality (speed up), twoPass (speed up), bestQuality (speed up), constantBitrate * goodQuality (slow down), bestQuality * constantBitrage (slow down), quality * threads (speed up), constantBitrate * threads * twoPass (speed up)
Changelog: Mentions speed up for bestQuality, goodQuality and for one-pass.
Commits:
b5ea2fbc2: Improved 1-pass CBR rate control
6c565fada0820
61f0c090dff65135c1828a7c407f51fe21405926: speed-up mentioned
0e9a6ed72a06dd367049d33ec656f7e3bf2211a2: Speed-up mentioned
Configuration option mentioned

0.9.7 - 0.9.7-p1:
Configuration options: constantBitrate * goodQuality (speed up), bestQuality * constantBitrate (speed up)
Changelog: Doesn't mention speedups, only a few fixes.
Commits:
e96131705: Revers b5ea2fb because of loss of quality
Configuration option mentioned

0.9.7-p1 - 1.0.0:
Configuration options: bestQuality (speed up), goodQuality (speed up)
Changelog: Reports performance improvements in different qualities
Commits:
b9f19f8917: speedup on quality
Configuration option mentioned


1.0.0 - 1.1.0:
Configuration options: bestQuality (slow down), goodQuality (slow down), twoPass (speed up)
Changelog: A denoiser is added to the encoder; no slow down reported for "most material". twoPass speed up is reported
Commits:
019384f2d36: two pass optimization
Nothing found regarding goodQuality or bestQuality

1.1.0 - 1.2.0:
Configuration options: very minor changes; constantBitrate * twoPass (slow down)
Changelog: Does not clearly mention speed up or slow down
Commits:
64075c9b0129e: Encoder denoiser performance improvement (nothing to slow down)
7b0b6a2c414a7e8947d37c817d5b312a7ec844f7: Configuration option mentioned
Configuration option mentioned in the commits


1.2.0 - 1.3.0:
Configuration option: bestQuality (slow down), goodQuality (slow down), twoPass (slow down)
Changelog: Introduces VP9. Mentions speed optimizations but no slow downs.
Commits:
ee2051f6500: two pass rate control code changes
e237fd7c: Two pass refactoring
9255ad107f2e1: Impact on quality (higher runtime)
374a17366: Force lossless coding at very high quality
11abab356e: mentions slower encoding on speed 2
Configuration option mentioned

1.3.0 - 1.4.0:
Configuration options: twoPass (massive speed up), threads2/threads3/threads4 * twoPass (slow down), quality * constantBitrate * threads (speed up)
Changelog: Focuses on VP9; Vp8 is not mentioned at all
Commits:
0639b5cff: speed up in quality
096ab11012: Removing pass number check (the output file has been opened twice during two-pass encoding)
c30a9cd97: Speed up in 2 pass
2e05341ab4990: Speed up in 2 pass
Configuration option mentioned

1.4.0 - 1.5.0:
Configuration options: minor changes, bestQuality (speed up), goodQuality (speed up)
Changelog: Mentions VP9; combines some functions with VP9
Commits:
8dd466edc84: impact on quality of animated test sequence
Configuration option mentioned


1.5.0 - 1.6.1:
Configuration options: constantBitrate * goodQuality (speed up), bestQuality * constantBitrate (speed up), quality * twoPass (slow down), quality * threads * twoPass (speed up)
Changelog: Mentions VP9 speed up (but only high-level)
Commits:
1cd987d9222a27f0f2dfb3b71bc2325313865b90: Speed-up mentioned
8ba98516: Improve best quality settings speed
6fbb4c3061e: Speed up VP8 on Linux
configuration option mentioned

1.6.1 - 1.7.0:
Configuration options: None
Changelog: Nothing regarding VP8
Commits:
c8678fb7f38024345462cfab3b34d649548ff445: Speed-up mentioned
Configuration option does not make sense

1.7.0 - 1.8.0:
Configuration options: None
Changelog: Focuses on VP9
Commits:
c176e6490:  ~10% improvement on 64 bit
ad0ed535a: mentions it is faster
Configuration options: Not mentioned

## VP9

### Commit messages and changelogs
1.3.0 - 1.4.0:
Configuration options: columnTiling (massive slow down), bestQuality (massive slow down), goodQuality (slow down), quality * noAltRef (speed up), arnMaxFrames * quality (slow down), columnTiling * constantBitrate (speed up), bestQuality * columnTiling (high slow down)
Changelog:  Mentions only speed ups, no slow downs; 
Commits:
ea8aaf15b55: 20% slower
eba9c762a: tile-based multi-threaded encoder
54eda13f8df587fe0a5a202f232f66863aff445a: Slow down mentioned
Configuration option is mentioned

1.4.0 - 1.5.0:
Configuration options: goodQuality (massive speed up) but slow down when it comes to threading and column tiling
Changelog: Only mentions speed ups, no slow downs
Commits:
9fd8abc54: speed up compression for speed 5-8
9cfba09ac0e5: Optimize vpx_quantize assembler
Configuration option is mentioned


1.5.0 - 1.6.0:
Configuration options: bestQuality (massive speed up -- probably fix of 1.4.0 slow down?), columnTiling * goodquality * threads (slow down)
Changelog: Instructions have been reordered for Intel processors. 
Commits:
af7fb17c09: Time savings on Xeon desktop
74a679de: Port optimizations to vp9
Configuration option not mentioned

1.6.0 - 1.6.1:
Configuration options: bestQuality (slow down), goodQuality (speed up), goodQuality * columnTiling * threads (slow down)
Changelog:  Mentions only speed up
Commits:
5d881770e59: Change default recode rule for good speed and best; mentioned speed-up
Configuration option mentioned


1.6.1 - 1.7.0:
Configuration options: bestQuality (speed up), goodQuality (speed up), constantBitrate (speed up)
Changelog: VP9 high-bit performance reported
Commits:
9c2552a1c149cbc: speed up 
6557baf3363e: speed up
1a5482d4d: Denoiser speed-up
Configuration option mentioned


1.7.0 - 1.8.0:
Configuration options: bestQuality (slow down), constantBitrate (speed up), columnTiling * noAltRef (speed up), arnMaxFrames * quality (slow down)
Changelog: Mentions 2pass improvements in combination with auto-alt-ref; aso mentions improvements on real-time encoding.
Commits:
067457339bc: Improvement of bitrate mentioned
25d6542251a: Encoding speed a bit faster for lower quality settings
55db4f033: Increase convergence speed of noise estimation
2eac6df788dbc: speed feature controls tx size search depth
Configuration option mentioned


## FastDownward

### Commit messages and change logs

2016_06 - 2017_01: 
Configuration options: collection_max_size * num_samples (slow-down), PDB (slow-down), shrink_fh (slow-down), lm_rhw (speed-up), landmark (speed-up)
Changelog: There was no changelog for this revision
Commits:
dfdccf815129f6d51d48cd502e5bdf77d4d0df97: fixed performance issue (speed-up)
97944b49607d1e9967554cd8e3718a7326e7e185: configuration option 'landmark' mentioned
de17135aefbe19ea740f5ee251c259d9f14e06b9: configuration option 'landmark' mentioned
da3d61530239f380e259dc10f0f35c9a0792139b: configuration option 'landmark' mentioned
41f14f51ca0e3b71979581eea12150d3f30d966e: configuration option 'landmark' mentioned
46838c2b47126c4b8ad4a8129d76341cf9a27261: configuration option 'landmark' mentioned
7a9203b73c778a3983c115eae49aa153f05aec27: configuration option 'landmark' mentioned
Configuration option mentioned


2017_01 - 2017_07: 
Configuration options: collection_max_size * num_samples (slow-down), PDB (slow-down), shrink_fh (slow-down), lm_rhw (speed-up), blind (speed-up), hmax (slow-down)
Changelog: There was no changelog for this revision
Commits:
f3fec8be30b4d7cebac842995df971550d2e06fc: Configuration option 'landmark' mentioned
Configuration option mentioned

2017_07 - 2018_01:
Configuration options: collection_max_size * num_samples (speed-up), shrink_fh (speed-up), blind (speed-up), hmax (slow-down), cpdbs (speed-up), lmcut (slow-down)
Changelog: There was no changelog for this revision
Commits:
fb322500801caa48ae464b4d869aeac8d6dbace0: Configuration option 'shrink_fh' mentioned
153d579a697230741779dee1ad5bd5646f8e0141: Configuration optoin 'shrink_fh' mentioned
ecdd704bc9f004764ccb08292b135022aa3e21d6: Configuration option 'PDB' mentioned
b731637b1eb6beb52e142e89f4c89a48aaa1fbb8: Configuration option 'Canonical PDB' mentioned
Configuration option mentioned

2018_01 - 2018_07: 
Configuration options: collection_max_size * min_improvement * num_samples (slow-down), collection_max_size * num_samples (speed-up), shrink_fh (speed-up), lm_hm (slow-down), blind (speed-up), hmax (slow-down), iPDB (slow-down), lm_rhw (slow-down)
Changelog: There was no changelog for this revision
Commits:
Nothing
Configuration option not mentioned

2018_07 - 2019_01:
Configuration options: lm_rhw * no_orders (speed-up), shrink_fh (speed-up), lm_hm (speed-up)
Changelog: There was no changelog for this revision
Commits:
e4970b079d6a7fdbc04accf9ad7acd17907e6b87: Mentions performance tuning
951e98f730f84c95771b72efe0b49fbdf05e9d7d: 'landmark' mentioned
4bef566981dd2a8dc5f93d9131fe2243cd6b15da: 'landmark' mentioned
Configuration option mentioned

2019_01 - 2019_06:
Configuration options: collection_max_size * min_improvement * num_samples (slow-down), collection_max_size * num_samples (speed-up), shrink_fh (slow-down), lm_hm (slow-down), lm_rhw (slow-down), iPDB (speed-up), min_improvement (slow-down)
Changelog: There was no changelog for this revision
Commits:
212d1f4e8f3a32cd5a0a0a2dfc5759df203bd661: Slow-down reported (It is possible that the new code now uniquifies certain conditions
    multiple times, but there is no harm in that other than a slight
    performance cost.)
5c59dd0a982bc6ca70735617133aa402d526cfe0: Configuration option 'PDB' mentioned
52f1d51b69de3857b895d8a0e7e90fd7c46bf4dc: Configuration option 'PDB' mentioned
15d29405f5bb9d3c1659d78b6635ce21937ac05e: Configuration option 'PDB' mentioned
e1e3178509cc83fe2c0e0e38e2eed7f50e9f06a3: Configuration option 'landmark' mentioned
a3926cf575510d7d65fdc5e4f21d2d14c50d5829: Configuration option 'landmark' mentioned
1b8685eea3c0bd9898e3901a5c1e707e6d8a0931: Configuration option 'landmark' mentioned
Configuration option mentioned



2019_06 - 2019_12:
Configuration options: None
Changelog: Nothing relevant mentioned
Commits:
No configuration options mentioned

2019_12 - 2020_06: 
Configuration options: shrink_fh (speed-up), lm_hm (slow-down)
Changelog:Nothing relevant reported
Commits:
No configuration option mentioned
