import matplotlib.pyplot as plt
import re

# Input data as a string
data = """
cache_size=65536        stride=1        avg_misses=0.000507     avg_time=0.002420
cache_size=65536        stride=2        avg_misses=0.000273     avg_time=0.001887
cache_size=65536        stride=4        avg_misses=0.000216     avg_time=0.002115
cache_size=65536        stride=8        avg_misses=0.000180     avg_time=0.002190
cache_size=65536        stride=16       avg_misses=0.000185     avg_time=0.002128
cache_size=65536        stride=32       avg_misses=0.000198     avg_time=0.002116
cache_size=65536        stride=64       avg_misses=0.000187     avg_time=0.001833
cache_size=65536        stride=128      avg_misses=0.000199     avg_time=0.001885
cache_size=65536        stride=256      avg_misses=0.000147     avg_time=0.001857
cache_size=65536        stride=512      avg_misses=0.000141     avg_time=0.001908
cache_size=65536        stride=1024     avg_misses=0.000085     avg_time=0.001876
cache_size=65536        stride=2048     avg_misses=0.013467     avg_time=0.002209
cache_size=65536        stride=4096     avg_misses=0.000093     avg_time=0.005107
cache_size=65536        stride=8192     avg_misses=0.000017     avg_time=0.002188
cache_size=65536        stride=16384    avg_misses=0.000004     avg_time=0.002169
cache_size=65536        stride=32768    avg_misses=0.000006     avg_time=0.002078
cache_size=131072       stride=1        avg_misses=0.002003     avg_time=0.001980
cache_size=131072       stride=2        avg_misses=0.001992     avg_time=0.001892
cache_size=131072       stride=4        avg_misses=0.002546     avg_time=0.002126
cache_size=131072       stride=8        avg_misses=0.002659     avg_time=0.002238
cache_size=131072       stride=16       avg_misses=0.002820     avg_time=0.002180
cache_size=131072       stride=32       avg_misses=0.001752     avg_time=0.002116
cache_size=131072       stride=64       avg_misses=0.002240     avg_time=0.001856
cache_size=131072       stride=128      avg_misses=0.001587     avg_time=0.001904
cache_size=131072       stride=256      avg_misses=0.001747     avg_time=0.001874
cache_size=131072       stride=512      avg_misses=0.002397     avg_time=0.001895
cache_size=131072       stride=1024     avg_misses=0.001889     avg_time=0.001896
cache_size=131072       stride=2048     avg_misses=0.064918     avg_time=0.002251
cache_size=131072       stride=4096     avg_misses=0.000582     avg_time=0.008138
cache_size=131072       stride=8192     avg_misses=0.000025     avg_time=0.005026
cache_size=131072       stride=16384    avg_misses=0.000005     avg_time=0.002146
cache_size=131072       stride=32768    avg_misses=0.000006     avg_time=0.002141
cache_size=131072       stride=65536    avg_misses=0.000002     avg_time=0.002040
cache_size=262144       stride=1        avg_misses=0.020354     avg_time=0.001953
cache_size=262144       stride=2        avg_misses=0.039201     avg_time=0.001871
cache_size=262144       stride=4        avg_misses=0.077566     avg_time=0.002121
cache_size=262144       stride=8        avg_misses=0.153943     avg_time=0.002220
cache_size=262144       stride=16       avg_misses=0.302971     avg_time=0.002173
cache_size=262144       stride=32       avg_misses=0.568091     avg_time=0.002045
cache_size=262144       stride=64       avg_misses=1.068163     avg_time=0.001974
cache_size=262144       stride=128      avg_misses=1.387180     avg_time=0.002216
cache_size=262144       stride=256      avg_misses=2.072647     avg_time=0.002447
cache_size=262144       stride=512      avg_misses=2.271960     avg_time=0.002588
cache_size=262144       stride=1024     avg_misses=2.470185     avg_time=0.002714
cache_size=262144       stride=2048     avg_misses=1.540982     avg_time=0.005518
cache_size=262144       stride=4096     avg_misses=2.248144     avg_time=0.008878
cache_size=262144       stride=8192     avg_misses=0.251521     avg_time=0.008775
cache_size=262144       stride=16384    avg_misses=0.000092     avg_time=0.007746
cache_size=262144       stride=32768    avg_misses=0.000011     avg_time=0.002291
cache_size=262144       stride=65536    avg_misses=0.000002     avg_time=0.002247
cache_size=262144       stride=131072   avg_misses=0.000002     avg_time=0.002037
cache_size=524288       stride=1        avg_misses=0.032072     avg_time=0.001991
cache_size=524288       stride=2        avg_misses=0.063742     avg_time=0.001884
cache_size=524288       stride=4        avg_misses=0.127877     avg_time=0.002091
cache_size=524288       stride=8        avg_misses=0.254907     avg_time=0.002161
cache_size=524288       stride=16       avg_misses=0.508326     avg_time=0.002133
cache_size=524288       stride=32       avg_misses=0.960865     avg_time=0.002031
cache_size=524288       stride=64       avg_misses=1.840644     avg_time=0.002061
cache_size=524288       stride=128      avg_misses=2.519617     avg_time=0.002527
cache_size=524288       stride=256      avg_misses=3.825169     avg_time=0.003020
cache_size=524288       stride=512      avg_misses=4.006594     avg_time=0.003113
cache_size=524288       stride=1024     avg_misses=4.241896     avg_time=0.003200
cache_size=524288       stride=2048     avg_misses=4.868297     avg_time=0.004770
cache_size=524288       stride=4096     avg_misses=2.692468     avg_time=0.008727
cache_size=524288       stride=8192     avg_misses=1.481119     avg_time=0.008351
cache_size=524288       stride=16384    avg_misses=0.200419     avg_time=0.007925
cache_size=524288       stride=32768    avg_misses=0.000100     avg_time=0.007968
cache_size=524288       stride=65536    avg_misses=0.000003     avg_time=0.002351
cache_size=524288       stride=131072   avg_misses=0.000003     avg_time=0.002274
cache_size=524288       stride=262144   avg_misses=0.000001     avg_time=0.002079
cache_size=1048576      stride=1        avg_misses=0.033543     avg_time=0.001950
cache_size=1048576      stride=2        avg_misses=0.067205     avg_time=0.001880
cache_size=1048576      stride=4        avg_misses=0.135157     avg_time=0.002134
cache_size=1048576      stride=8        avg_misses=0.272159     avg_time=0.002179
cache_size=1048576      stride=16       avg_misses=0.542322     avg_time=0.002166
cache_size=1048576      stride=32       avg_misses=1.029736     avg_time=0.002068
cache_size=1048576      stride=64       avg_misses=1.975202     avg_time=0.002078
cache_size=1048576      stride=128      avg_misses=2.866833     avg_time=0.002593
cache_size=1048576      stride=256      avg_misses=4.488878     avg_time=0.003148
cache_size=1048576      stride=512      avg_misses=4.839688     avg_time=0.003336
cache_size=1048576      stride=1024     avg_misses=5.284025     avg_time=0.003445
cache_size=1048576      stride=2048     avg_misses=3.012843     avg_time=0.003115
cache_size=1048576      stride=4096     avg_misses=3.217015     avg_time=0.008765
cache_size=1048576      stride=8192     avg_misses=2.912622     avg_time=0.008835
cache_size=1048576      stride=16384    avg_misses=4.652890     avg_time=0.008186
cache_size=1048576      stride=32768    avg_misses=0.000170     avg_time=0.007995
cache_size=1048576      stride=65536    avg_misses=0.000031     avg_time=0.005708
cache_size=1048576      stride=131072   avg_misses=0.000003     avg_time=0.002342
cache_size=1048576      stride=262144   avg_misses=0.000001     avg_time=0.002274
cache_size=1048576      stride=524288   avg_misses=0.000001     avg_time=0.002078
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
