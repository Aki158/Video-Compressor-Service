import json
import socket
import subprocess
import os


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 9001))
    sock.listen(1)
    
    while True:
        connection, _ = sock.accept()
        try:
            connection.send('Start the Video Compressor Service.'.encode('utf-8'))

            data = connection.recv(1024).decode('utf-8')
            data_json = json.loads(data)
            filename = data_json['filename']
            filename_length = data_json['filename_length']
            filesize = data_json['filesize']
            STREAM_RATE = 1400
            print('filename : {}, filename_length {}, Data Length {}' \
                .format(filename,filename_length, filesize))
            
            if filesize == 0:
                raise Exception('No data to read from client.')

            # サーバにファイルをアップロードする
            with open(os.path.join(filename),'wb+') as f:
                while filesize > 0:
                    data = connection.recv(filesize if filesize <= STREAM_RATE else STREAM_RATE)
                    f.write(data)
                    filesize -= len(data)
            
            connection.send('Upload finish'.encode('utf-8'))

            while True:
                # Video Compressor Serviceを実行する
                cmd_str = connection.recv(1024).decode('utf-8')
                cmp_arr = cmd_str.split(' ')
                subprocess.run(cmp_arr)

                connection.send('File generated.\n'.encode('utf-8'))

                # サービスを続けるか確認
                continue_question = connection.recv(1024).decode('utf-8')

                if continue_question == '0':
                    # サーバにアップロードしたファイルを削除する
                    os.remove(filename)
                    connection.send('End the Video Compressor Service.'.encode('utf-8'))
                    break

        except Exception as e:
            print('Error: ' + str(e))

        finally:
            print('Closing current connection')
            connection.close()


if __name__ == '__main__':
    main()