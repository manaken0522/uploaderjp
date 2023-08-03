import time
import urllib
import requests
from bs4 import BeautifulSoup

from .File import *

class Uploader():
    def __init__(self, uploader_url):
        self.url = uploader_url
        self.id = urllib.parse.urlparse(self.url).path.split('/')[1]

        response = requests.get(f'https://ux.getuploader.com/{self.id}/')
        soup = BeautifulSoup(response.text, 'html.parser')
        self.name = soup.find('div', attrs={'class':'page-header'}).contents[1].contents[0]
        uploaderinfo_table = soup.find_all('table', attrs={'class':'table'})[1].find_all('tr')
        diskinfo = uploaderinfo_table[0].find('td').contents[0]
        self.disk_used = diskinfo.split('/')[0].replace(' ', '')
        self.disk_max = diskinfo.split('/')[1].split('(')[0].replace(' ', '')
        self.disk_used_percent = int(diskinfo.split('/')[1].split('(')[1].replace(' ', '').replace(')', '').replace('%', ''))
        self.file_count = int(uploaderinfo_table[1].find('td').contents[0].replace(' ファイル', ''))
        self.download_count = int(uploaderinfo_table[2].find('td').contents[0].replace(' ダウンロード', ''))

    def get_files(self, page:int=None):
        if page != None:
            response = requests.get(f'https://ux.getuploader.com/{self.id}/index/date/desc/{page}')
            soup = BeautifulSoup(response.text, 'html.parser')
            file_table = soup.find('table', attrs={'class':'table table-small-font table-hover'}).find('tbody').find_all('tr')
            files = []
            for file_element in file_table:
                download_url = file_element.find('td').contents[0].attrs['href']
                file = File(download_url)
                files.append(file)
        else:
            page = 1
            while True:
                response = requests.get(f'https://ux.getuploader.com/{self.id}/index/date/desc/{page}')
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    file_table = soup.find('table', attrs={'class':'table table-small-font table-hover'}).find('tbody').find_all('tr')
                    files = []
                    for file_element in file_table:
                        download_url = file_element.find('td').contents[0].attrs['href']
                        file = File(download_url)
                        files.append(file)
                else:
                    break
        return files