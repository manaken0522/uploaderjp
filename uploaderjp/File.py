import requests
from bs4 import BeautifulSoup

class File():
    def __init__(self, download_url:str):
        response = requests.get(download_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        fileinfo_elements = soup.find_all('table', attrs={'class':'table space'})[0].find_all('tr')
        self.name = fileinfo_elements[0].find('td').contents[0]
        self.comment = fileinfo_elements[1].find('td').find('strong').text
        self.original_name = fileinfo_elements[2].find('td').contents[0]
        self.size = fileinfo_elements[3].find('td').contents[0]
        self.uploaded_datetime = fileinfo_elements[4].find('td').contents[0]
        self.download_count = fileinfo_elements[5].find('td').contents[0]
        fileinfo_elements = soup.find_all('div', attrs={'class':'form-group'})
        self.download_url = fileinfo_elements[0].find('input').attrs['value']
        self.md5 = fileinfo_elements[1].find('input').attrs['value']

    def download(self, filepath:str=None, password:str=None):
        if filepath == None:
            filepath = f'./{self.name}'
        response = requests.get(self.download_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        token = soup.find('input', attrs={'name':'token'}).attrs['value']
        response = requests.post(self.download_url, data={'token': token})
        soup = BeautifulSoup(response.text, 'html.parser')
        download_link = soup.find_all('a', attrs={'title': f'{self.name} をダウンロード'})[0].attrs['href']
        downloaded_binarydata = requests.get(download_link).content
        with open(filepath, mode='wb') as f:
            f.write(downloaded_binarydata)