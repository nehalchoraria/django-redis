from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .downloadBhav import xls_to_json
import pandas,json
from django.shortcuts import render
from datetime import datetime as date

day = str(int(date.now().strftime('%d'))-5)
month = date.now().strftime('%m')
year = date.now().strftime('%y')
bhavCopyLink = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ'+day+month+year+'_CSV.ZIP' 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
headingList = ['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','NO_TRADES']

def stockviewcache(request):
    if 'stocks' in cache:
        stocks = cache.get('stocks')
        return render(request, 'index.html',  {'results': stocks,'headingList':headingList } )
    else:
        try:
            xls_to_json(bhavCopyLink)
        except:
            return render(request, 'index.html',  {'results': { 'error' : 'File not available for today.'} } )
        results = [ stock for stock in json.load(open("dump.json","r")) ]
        cache.set('stocks', results, timeout=CACHE_TTL)
        return render(request, 'index.html',  {'results': results, 'headingList':headingList} )