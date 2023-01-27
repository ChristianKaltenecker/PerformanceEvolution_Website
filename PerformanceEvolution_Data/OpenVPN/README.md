Pontipine cluster
uiq2 workload aa 220.000.000 ~1.400MB
Max send time for iperf3 20s to ensure less stdev(incomplete measurements not with 1s timeframe result in high inaccurate performance spikes)
UDP Mbits max 200
Iperf 3.6
Throughput measured in mbits
Only from client to server measured measured due to too high stdev in other direction, similar to  https://community.openvpn.net/openvpn/wiki/PerformanceTesting#Testcases except only 1 client and tcp.

https://community.openvpn.net/openvpn/wiki/Gigabit_Networks_Linux has a good visualization of our setup.
Optimizations from that link however will be ignore as we want the most general setup and there were also no improvements from applying them since they only make sense for udp.

Lib Versions: 
pkcs11-helper-1.11 
ENSSL_VERSION:-1.0.2i
LZO 2.09
