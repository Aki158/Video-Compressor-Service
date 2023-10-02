import json
import os
import socket
import sys


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(('localhost', 9001))
    except socket.error as err:
        print(err)
        sys.exit(1)

    try:
        print(sock.recv(1024).decode('utf-8'))
        
        # サーバにファイルをアップロードする
        filepath = input('Type in a file to upload: ')

        with open(filepath, 'rb') as f:
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0,0)

            filename = os.path.basename(f.name)

            if filesize > pow(2,32):
                raise Exception('File must be below 4GB.')

            if filename[-3:] != 'mp4':
                raise Exception('File extension must be mp4.')
        
            data_json = {
                'filename' : filename,
                'filename_length' : len(filename),
                'filesize' : filesize
                }

            sock.send(json.dumps(data_json).encode('utf-8'))

            data = f.read(1400)
            print('Sending...')
            while data:
                sock.send(data)
                data = f.read(1400)
            
            print(sock.recv(16).decode('utf-8'))

        while True:
            # Video Compressor Serviceを実行する
            cmd = ''
            height = ''
            width = ''
            start = ''
            end = ''
            flamerate = ''
            resize = ''

            select_mode = input('Please enter a number from 0 to 4\n' + \
                                '0 : 動画ファイルを圧縮する\n' + \
                                '1 : 動画の解像度を変更する\n' + \
                                '2 : 動画の縦横比を変更する\n' + \
                                '3 : 動画をオーディオに変換する\n' + \
                                '4 : 時間範囲からGIFを作成する\n')
            
            if select_mode == '0':                
                select_level = input('Please select the degree of compression\n' + \
                                    '0 : low\n' + \
                                    '1 : medium\n' + \
                                    '2 : high\n')
                if select_level == '0':
                    cmd = 'ffmpeg -i ' + filename + ' -c:v libx264 output/output_low.mp4'
                elif select_level == '1':
                    cmd = 'ffmpeg -i ' + filename + ' -c:v libx265 output/output_medium.mp4'
                elif select_level == '2':
                    cmd = 'ffmpeg -i ' + filename + ' -c:v libx265 -b:v 500k output/output_high.mp4'
                
            elif select_mode == '1':
                height = input('Please enter the height (ex. 1280) : ')
                width = input('Please enter the width (ex. 720) : ')
                cmd = 'ffmpeg -i ' + filename + ' -filter:v scale=' + height + ':' + width + ' -c:a copy output/output_scale.mp4'

            elif select_mode == '2':
                height = input('Please enter the height (ex. 16) : ')
                width = input('Please enter the width (ex. 9) : ')
                cmd = 'ffmpeg -i ' + filename + ' -pix_fmt yuv420p -aspect ' + height + ':' + width + ' output/output_aspect.mp4'

            elif select_mode == '3':
                cmd = 'ffmpeg -i ' + filename + ' -vn output/output_audio.mp3'

            elif select_mode == '4':
                start = input('Input start position (ex. 00:00:20) : ')
                end = input('Input end position (ex. 10) : ')
                flamerate = input('Input flame rate (ex. 10) : ')
                resize = input('Input resize (ex. 300) : ')
                cmd = 'ffmpeg -ss ' + start + ' -i ' + filename + ' -to ' + end + ' -r ' + flamerate + ' -vf scale=' + \
                    resize + ':-1 output/output_gif.gif'
            
            sock.send(cmd.encode('utf-8'))
            
            print(sock.recv(1024).decode('utf-8'))

            # サービスを続けるか確認
            continue_question = input('Do you want to continue ?\n' + \
                                '0 : No\n' + \
                                '1 : Yes\n')
            
            sock.send(continue_question.encode('utf-8'))
            
            if continue_question == '0':
                print(sock.recv(1024).decode('utf-8'))
                break
                
    finally:
        print('closing socket')
        sock.close()


if __name__ == '__main__':
    main()