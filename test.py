import hashlib
import time
import matplotlib.pyplot as plt
import random

fileName = 'random string 4GB'
# 存储各个函数花费时间
time_spend = dict()
# 导入测试数据
# with open(fileName, 'rb') as f:
#     test_data = f.read()
# print("finish reading data")
print("start generating data")
test_data = [random.randint(0, 255) for _ in range(1024 * 1024 * 4)]
test_data = bytes(test_data)
print("finish generating data")
test_data *= 1024

all_method = {'MD5': hashlib.md5, 'SHA1': hashlib.sha1, 'SHA256': hashlib.sha256, 'SHA512': hashlib.sha512,
              'SHA3_256': hashlib.sha3_256, 'SHA3_384': hashlib.sha3_384, 'SHA3_512': hashlib.sha3_512,
              'BLAKE2b': hashlib.blake2b, 'BLAKE2s': hashlib.blake2s, 'SHAKE_128': hashlib.shake_128,
              'SHAKE_256': hashlib.shake_256, 'SHA224': hashlib.sha224, 'SHA384': hashlib.sha384,
              'SHA3_224': hashlib.sha3_224}

for i in range(3):
    prev = time_spend
    for method in all_method.keys():
        time_spend[method] = []
    size = 1
    while size < len(test_data):
        for method in all_method:
            start = time.time()
            all_method[method](test_data[:size])
            end = time.time()
            time_spend[method].append(end - start)

        size *= 2
        print('current size: ', size)

    for method in time_spend.keys():
        if method in prev.keys() and len(time_spend[method]) == len(prev[method]):
            time_spend[method] = [time_spend[method][i] + prev[method][i] for i in range(len(time_spend[method]))]

for method in all_method:
    time_spend[method] = [time_spend[method][i] / 3 for i in range(len(time_spend[method]))]

plt.figure(figsize=(10, 8))
for method in all_method:
    plt.plot(time_spend[method], label=method)
plt.title(fileName)
plt.xlabel('size(log2)')
plt.ylabel('time/s')
plt.legend()
plt.savefig(f'{fileName}.png')
plt.show()


with open(f'{fileName}result.txt', 'w') as f:
    for method in all_method:
        f.write(method + '\n')
        for i in range(len(time_spend[method])):
            f.write(str(time_spend[method][i]) + '\n')
        f.write('\n')

