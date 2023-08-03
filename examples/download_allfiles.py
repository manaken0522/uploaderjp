import time
import sys
import uploaderjp

if __name__ == '__main__':
    args = sys.argv
    uploader = uploaderjp.Uploader(args[1])
    files = uploader.get_files()
    for file in files:
        print(file.name)
        file.download()