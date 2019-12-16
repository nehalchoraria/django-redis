import requests,os
import zipfile

baseLink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ101219_CSV.ZIP'
def download_file(url):
    filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: 
                    f.write(chunk)
    return filename

def unzip(filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(filename)
    
fileName = download_file(baseLink)
unzip(fileName)