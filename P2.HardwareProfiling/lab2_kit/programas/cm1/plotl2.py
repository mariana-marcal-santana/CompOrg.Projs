import matplotlib.pyplot as plt
import re

# Input data as a string
data = """
cache_size=65536        stride=1        avg_misses=0.000899     avg_time=0.002890
cache_size=65536        stride=2        avg_misses=0.000641     avg_time=0.001955
cache_size=65536        stride=4        avg_misses=0.000760     avg_time=0.002226
cache_size=65536        stride=8        avg_misses=0.000820     avg_time=0.002237
cache_size=65536        stride=16       avg_misses=0.000658     avg_time=0.002268
cache_size=65536        stride=32       avg_misses=0.000591     avg_time=0.002060
cache_size=65536        stride=64       avg_misses=0.000529     avg_time=0.001935
cache_size=65536        stride=128      avg_misses=0.000577     avg_time=0.001877
cache_size=65536        stride=256      avg_misses=0.000809     avg_time=0.001899
cache_size=65536        stride=512      avg_misses=0.000846     avg_time=0.001928
cache_size=65536        stride=1024     avg_misses=0.000656     avg_time=0.001867
cache_size=65536        stride=2048     avg_misses=0.053699     avg_time=0.002181
cache_size=65536        stride=4096     avg_misses=0.000267     avg_time=0.005023
cache_size=65536        stride=8192     avg_misses=0.000030     avg_time=0.002160
cache_size=65536        stride=16384    avg_misses=0.000011     avg_time=0.002136
cache_size=65536        stride=32768    avg_misses=0.000010     avg_time=0.002036
cache_size=131072       stride=1        avg_misses=0.001754     avg_time=0.001955
cache_size=131072       stride=2        avg_misses=0.001505     avg_time=0.001860
cache_size=131072       stride=4        avg_misses=0.001666     avg_time=0.002198
cache_size=131072       stride=8        avg_misses=0.001495     avg_time=0.002196
cache_size=131072       stride=16       avg_misses=0.001676     avg_time=0.002246
cache_size=131072       stride=32       avg_misses=0.001495     avg_time=0.002051
cache_size=131072       stride=64       avg_misses=0.001474     avg_time=0.001980
cache_size=131072       stride=128      avg_misses=0.001455     avg_time=0.001863
cache_size=131072       stride=256      avg_misses=0.001586     avg_time=0.001879
cache_size=131072       stride=512      avg_misses=0.001361     avg_time=0.001898
cache_size=131072       stride=1024     avg_misses=0.001217     avg_time=0.001894
cache_size=131072       stride=2048     avg_misses=0.084483     avg_time=0.002298
cache_size=131072       stride=4096     avg_misses=0.001208     avg_time=0.008237
cache_size=131072       stride=8192     avg_misses=0.000198     avg_time=0.005075
cache_size=131072       stride=16384    avg_misses=0.000008     avg_time=0.002189
cache_size=131072       stride=32768    avg_misses=0.000011     avg_time=0.002173
cache_size=131072       stride=65536    avg_misses=0.000008     avg_time=0.002080
cache_size=262144       stride=1        avg_misses=0.021303     avg_time=0.001987
cache_size=262144       stride=2        avg_misses=0.039550     avg_time=0.001901
cache_size=262144       stride=4        avg_misses=0.079012     avg_time=0.002211
cache_size=262144       stride=8        avg_misses=0.154182     avg_time=0.002225
cache_size=262144       stride=16       avg_misses=0.301461     avg_time=0.002241
cache_size=262144       stride=32       avg_misses=0.566626     avg_time=0.002089
cache_size=262144       stride=64       avg_misses=1.083864     avg_time=0.002048
cache_size=262144       stride=128      avg_misses=1.261313     avg_time=0.002207
cache_size=262144       stride=256      avg_misses=1.871821     avg_time=0.002456
cache_size=262144       stride=512      avg_misses=1.976102     avg_time=0.002526
cache_size=262144       stride=1024     avg_misses=1.834599     avg_time=0.002642
cache_size=262144       stride=2048     avg_misses=1.247887     avg_time=0.005606
cache_size=262144       stride=4096     avg_misses=2.814956     avg_time=0.009268
cache_size=262144       stride=8192     avg_misses=2.016558     avg_time=0.010436
cache_size=262144       stride=16384    avg_misses=0.000084     avg_time=0.005060
cache_size=262144       stride=32768    avg_misses=0.000007     avg_time=0.002188
cache_size=262144       stride=65536    avg_misses=0.000003     avg_time=0.002169
cache_size=262144       stride=131072   avg_misses=0.000004     avg_time=0.002079
cache_size=524288       stride=1        avg_misses=0.032046     avg_time=0.001989
cache_size=524288       stride=2        avg_misses=0.062997     avg_time=0.001899
cache_size=524288       stride=4        avg_misses=0.126676     avg_time=0.002205
cache_size=524288       stride=8        avg_misses=0.250912     avg_time=0.002219
cache_size=524288       stride=16       avg_misses=0.490933     avg_time=0.002222
cache_size=524288       stride=32       avg_misses=0.937751     avg_time=0.002094
cache_size=524288       stride=64       avg_misses=1.824605     avg_time=0.002102
cache_size=524288       stride=128      avg_misses=2.549870     avg_time=0.002535
cache_size=524288       stride=256      avg_misses=3.873273     avg_time=0.003051
cache_size=524288       stride=512      avg_misses=4.150428     avg_time=0.003200
cache_size=524288       stride=1024     avg_misses=4.453178     avg_time=0.003309
cache_size=524288       stride=2048     avg_misses=4.650250     avg_time=0.004356
cache_size=524288       stride=4096     avg_misses=3.392999     avg_time=0.009616
cache_size=524288       stride=8192     avg_misses=4.403172     avg_time=0.010825
cache_size=524288       stride=16384    avg_misses=2.831391     avg_time=0.009807
cache_size=524288       stride=32768    avg_misses=0.268747     avg_time=0.007665
cache_size=524288       stride=65536    avg_misses=0.000006     avg_time=0.002339
cache_size=524288       stride=131072   avg_misses=0.000003     avg_time=0.002170
cache_size=524288       stride=262144   avg_misses=0.000002     avg_time=0.002079
cache_size=1048576      stride=1        avg_misses=0.034449     avg_time=0.001989
cache_size=1048576      stride=2        avg_misses=0.069089     avg_time=0.001899
cache_size=1048576      stride=4        avg_misses=0.139848     avg_time=0.002205
cache_size=1048576      stride=8        avg_misses=0.278761     avg_time=0.002221
cache_size=1048576      stride=16       avg_misses=0.548033     avg_time=0.002222
cache_size=1048576      stride=32       avg_misses=1.047853     avg_time=0.002096
cache_size=1048576      stride=64       avg_misses=2.040279     avg_time=0.002131
cache_size=1048576      stride=128      avg_misses=2.915715     avg_time=0.002624
cache_size=1048576      stride=256      avg_misses=4.562963     avg_time=0.003238
cache_size=1048576      stride=512      avg_misses=4.938294     avg_time=0.003405
cache_size=1048576      stride=1024     avg_misses=5.197932     avg_time=0.003485
cache_size=1048576      stride=2048     avg_misses=2.997739     avg_time=0.003148
cache_size=1048576      stride=4096     avg_misses=3.523741     avg_time=0.009275
cache_size=1048576      stride=8192     avg_misses=3.387404     avg_time=0.009721
cache_size=1048576      stride=16384    avg_misses=2.370089     avg_time=0.009223
cache_size=1048576      stride=32768    avg_misses=1.572261     avg_time=0.009348
cache_size=1048576      stride=65536    avg_misses=0.000075     avg_time=0.005555
cache_size=1048576      stride=131072   avg_misses=0.000004     avg_time=0.002289
cache_size=1048576      stride=262144   avg_misses=0.000002     avg_time=0.002130
cache_size=1048576      stride=524288   avg_misses=0.000002     avg_time=0.002075
cache_size=2097152      stride=1        avg_misses=0.034446     avg_time=0.001990
cache_size=2097152      stride=2        avg_misses=0.069107     avg_time=0.001865
cache_size=2097152      stride=4        avg_misses=0.139929     avg_time=0.002171
cache_size=2097152      stride=8        avg_misses=0.279049     avg_time=0.002211
cache_size=2097152      stride=16       avg_misses=0.548624     avg_time=0.002220
cache_size=2097152      stride=32       avg_misses=1.050365     avg_time=0.002097
cache_size=2097152      stride=64       avg_misses=2.046033     avg_time=0.002121
cache_size=2097152      stride=128      avg_misses=2.938747     avg_time=0.002652
cache_size=2097152      stride=256      avg_misses=4.627567     avg_time=0.003256
cache_size=2097152      stride=512      avg_misses=5.078749     avg_time=0.003449
cache_size=2097152      stride=1024     avg_misses=5.460556     avg_time=0.003538
cache_size=2097152      stride=2048     avg_misses=3.075742     avg_time=0.003136
cache_size=2097152      stride=4096     avg_misses=3.698092     avg_time=0.009315
cache_size=2097152      stride=8192     avg_misses=3.955446     avg_time=0.009576
cache_size=2097152      stride=16384    avg_misses=3.465614     avg_time=0.009547
cache_size=2097152      stride=32768    avg_misses=2.775228     avg_time=0.009878
cache_size=2097152      stride=65536    avg_misses=0.786894     avg_time=0.009714
cache_size=2097152      stride=131072   avg_misses=0.000304     avg_time=0.005658
cache_size=2097152      stride=262144   avg_misses=0.000011     avg_time=0.002310
cache_size=2097152      stride=524288   avg_misses=0.000002     avg_time=0.002165
cache_size=2097152      stride=1048576  avg_misses=0.000001     avg_time=0.002073
"""

# Parse the data
pattern = re.compile(r'cache_size=(\d+)\s+stride=(\d+)\s+avg_misses=([\d.]+)')
matches = pattern.findall(data)

# Organize the data
data_dict = {}
for cache_size, stride, avg_misses in matches:
    cache_size = int(cache_size)
    stride = int(stride)
    avg_misses = float(avg_misses)
    if cache_size not in data_dict:
        data_dict[cache_size] = {'stride': [], 'avg_misses': []}
    data_dict[cache_size]['stride'].append(stride)
    data_dict[cache_size]['avg_misses'].append(avg_misses)

# Plot the data
plt.figure(figsize=(12, 8))
for cache_size, values in data_dict.items():
    plt.plot(values['stride'], values['avg_misses'], marker='o', label=f'Cache Size = {cache_size}')

# Configure the plot
plt.xlabel('Stride')
plt.ylabel('Average Misses')
plt.title('Average Misses VS Stride for Array Sizes')
plt.xscale('log', base=2)
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('avg_misses_vs_stride.png')
