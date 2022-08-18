import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
import re


# folders
source_path = r'E:/迅雷下载/'
video_folder = r'E:/download/videos/'
music_folder = r'E:/download/musics/'
document_folder = r'E:/download/docs/'
zip_folder = r'E:/download/zips/'
torrent_folder = r'E:/download/torrents/'
exe_folder = r'E:/download/exes/'
others = r'E:/download/others/'
sets = {0: source_path, 1: video_folder, 2: music_folder, 3: document_folder, 4: zip_folder,
       5: torrent_folder, 6: exe_folder, 99: others}

# finder
finder = re.compile(r'\.[\w]{2,7}$')

# file list,file dictionary
file_list = os.listdir(source_path)
file_dic = {'zip': 4, 'pdf': 3, 'exe': 6, 'rar': 4, 'msi': 3,
            'srt': 1, 'dll': 3, 'mp4': 1, '006': 3, 'epub': 3, '7z': 4,
            'pptx': 3, 'txt': 3, 'xltd': 3, 'cfg': 3, 'xlsx': 3, 'rmvb': 1,
            'mkv': 1, 'torrent': 5, 'other': 99}


class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        print("Got event for file %s" % event.src_path)
        if finder.findall(event.src_path):
            matches = finder.findall(event.src_path)[0][1:]
        else:
            matches = 'other'
        if matches != 'xltd' and matches != 'cfg' and matches != 'txt':
            shutil.move(event.src_path, sets[file_dic[matches]] + event.src_path[8:])


observer = Observer()
event_handler = ExampleHandler() # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path=source_path)
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
def main():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
