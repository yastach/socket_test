
import socket
import pickle
import time

import numpy as np


def run_server(PORT):
    BUFFER_SIZE = 1024 #データ転送時のバッファサイズ

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # サーバ立ち上げ
            s.bind(('0.0.0.0', PORT)) # PORT番号をサーバにアサイン
            s.listen(1) # １クライアントだけ受け入れる
            print('waiting for connection')

            while True: 
                try:
                    (connection, client) = s.accept() # クライアントから接続待ち
                    #print('Client connected', client)

                    data = connection.recv(BUFFER_SIZE) # バッファサイズ毎にデータ受け入れ
                    data = pickle.loads(data) # クライアント側で、pickleを使ってバイナリデータに変換しているので、dataに戻す
                    print(type(data), data)
                    #data = data.upper()

                    time.sleep(1) # 重い処理を模擬したスリープ１秒
        
                    if data == 'true':
                        data = np.zeros([2000,1500,3]) # 画像データを模擬したnumpy array
                        data = data.astype('uint8')
                        connection.sendall(pickle.dumps(data)) # pickleを使ってバイナリデータに変換し、クライアントへ送信
                    else:
                        data = np.zeros([224,224,3])
                        data = data.astype('uint8')
                        connection.sendall(pickle.dumps(data))

                    #data = connection.recv(BUFFER_SIZE)
                    #print(data)

                finally:
                    connection.close() # 最後にコネクションを切断する。しないと２回目の接続時に、うまく接続できないことがある。
        finally:
            print("socket close")
            s.close() # 最後にサーバーを落とす。しないと２回目の接続時に、うまく接続できないことがある。

if __name__ == "__main__":
    PORT = 51000
    run_server(PORT)
