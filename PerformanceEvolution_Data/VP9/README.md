# VP9 (pervolution)

## Case Study Information

- software: libvpx/vpxenc (codec VP9)
- cluster: zeus
- benchmark/workload:
  - input: first 200 frames of lossless version of the 'Sintel' trailer (y4m, 480p)
  - output: webm (VP9)
- configurations: 3008
- revisions: 7
- properties:
  - performance (run time)
  - output file size
  - cpu load
- notes:
  - 5 repetitions
  - < 10% relative standard deviation for property performance
  - configuration space constraints:
    - `not rtQuality or not twoPass`
      - reason: setting rtQuality automatically disables twoPass

## Measurements Information

- average relative standard deviations:
  - performance: 0.44 %
- relative standard deviations available in separate files
- discretized results available

