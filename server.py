import json
import socket
import subprocess
import os
from pathlib import Path


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 9001))
    sock.listen(1)
    
    OUTPUT_PATH = 'output'

    while True:
        connection, _ = sock.accept()
        try:
            data = connection.recv(1024).decode('utf-8')
            data_json = json.loads(data)
            filename = data_json["filename"]
            filename_length = data_json["filename_length"]
            filesize = data_json["filesize"]
            STREAM_RATE = 1400
            print('filename : {}, filename_length {}, Data Length {}' \
                  .format(filename,filename_length, filesize))
            
            if filesize == 0:
                raise Exception('No data to read from client.')
        
            with open(os.path.join(OUTPUT_PATH, filename),'wb+') as f:
                while filesize > 0:
                    data = connection.recv(filesize if filesize <= STREAM_RATE else STREAM_RATE)
                    f.write(data)
                    filesize -= len(data)
            
            connection.send('Download finish'.encode('utf-8'))

            cmd_str = connection.recv(1024).decode('utf-8')
            cmp_arr = cmd_str.split(" ")
            print(cmd_str)
            subprocess.run(cmp_arr)

        except Exception as e:
            print('Error: ' + str(e))

        finally:
            print("Closing current connection")
            connection.close()


if __name__ == '__main__':
    main()