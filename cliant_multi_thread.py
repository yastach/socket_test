
import socket
import pickle
import time
import sys
from concurrent import futures

import numpy as np

# サーバーとの通信関数　1サーバーずつ接続
def server_treat(IP, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT)) # サーバーに接続

        data = "true" # トリガー(flag)として、データ送信　サーバー側での条件分岐の試験用
        print(data, 'is sent data')
        s.sendall(pickle.dumps(data)) # pickleでバイナリデータにして送信

        # 以下でデータ受信　画像データなど、重いデータは分割して受信し、合成したのちに、pickleで画像に戻す
        data = b""
        itr = 0
        while True:
            packet = s.recv(1024*1024)
            if not packet: break
            data += packet
            itr +=1
        data = pickle.loads(data)
        print(data.shape, 'was sent arr size')

        s.close()

        return data

# 複数サーバーへの接続テスト関数。並列処理なしver
def start_non_threading(num, ports, ips):
    PORT1 = 51000
    PORT2 = 51001

    time_bf = time.time()
    for i in range(num):
        print('=====%i  message ======'%(i+1))

        for sv_num in range(len(ports)):
            server_treat(ips[sv_num], ports[sv_num])

    time_aft = time.time()
    print('===== test completed ======')
    print(round(1000*(time_aft - time_bf)/num,1), ' ms for %i times average'%(num))
    print('')

# 複数サーバーへの接続テスト関数。並列処理ありver
def start_wz_threading(num, ports, ips):

    time_bf = time.time()
    for i in range(num):
        print('=====%i  message ======'%(i+1))

        future_list = []
        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(fn=server_treat, IP=ips[0], PORT=ports[0])
            future2 = executor.submit(fn=server_treat, IP=ips[1], PORT=ports[1])
            future_list.append(future1)
            future_list.append(future2)
            _ = futures.as_completed(fs=future_list)

        for i in future_list:
            data = i.result()
            print(data.shape)

    time_aft = time.time()
    print('===== test completed ======')
    print(round(1000*(time_aft - time_bf)/num,1), ' ms for %i times average'%(num))
    print('')



if __name__ == "__main__":
    ports = [51000, 51001]
    ips = ['192.168.56.101', '192.168.57.3']

    start_non_threading(3, ports, ips)
    start_wz_threading(3, ports, ips)

    