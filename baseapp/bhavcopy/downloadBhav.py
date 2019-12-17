import requests,os
import zipfile,pandas as pd

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
    
def xls_to_json(url):
    print('Downloadingfile...')
    filename = download_file(url)
    unzip(filename)
    csv_file = pd.DataFrame(pd.read_csv(filename.replace('_CSV.ZIP','.csv'), sep = ",", header = 0, index_col = False))
    csv_file['PERCENTAGE'] = csv_file.apply(lambda row: round (((row.CLOSE - row.PREVCLOSE)*100/row.CLOSE),2) ,axis = 1) 
    csv_file = csv_file.sort_values(by ='PERCENTAGE' , ascending=False)
    csv_file.to_json("dump.json", orient = "records", double_precision = 10, force_ascii = True)