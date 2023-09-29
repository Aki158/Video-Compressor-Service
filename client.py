import json
import socket
import sys
import os


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", 9001))
    except socket.error as err:
        print(err)
        sys.exit(1)

    try:
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

            print(data_json['filename'])
            print(data_json['filename_length'])
            print(data_json['filesize'])

            sock.send(json.dumps(data_json).encode('utf-8'))

            data = f.read(1400)
            print("Sending...")
            while data:
                sock.send(data)
                data = f.read(1400)
            
            print(sock.recv(16).decode('utf-8'))

            cmd = input("Input FFMPEG shell command : ")
            sock.send(cmd.encode('utf-8'))

    finally:
        print('closing socket')
        sock.close()


if __name__ == '__main__':
    main()