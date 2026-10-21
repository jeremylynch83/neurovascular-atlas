#!/usr/bin/env python3
"""Read-only live hosting checks. Timings are HTTP probes, not browser metrics."""
import argparse
import concurrent.futures
import datetime
import gzip
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []
    def redirect_request(self, request, fp, code, message, headers, newurl):
        self.chain.append({'status':code,'from':request.full_url,'to':newurl})
        return super().redirect_request(request,fp,code,message,headers,newurl)

def request(url, method='HEAD'):
    redirects=Redirects()
    opener=urllib.request.build_opener(redirects)
    started=time.perf_counter()
    response=opener.open(urllib.request.Request(url,method=method,headers={'Accept-Encoding':'gzip'}),timeout=20)
    headers_ms=(time.perf_counter()-started)*1000
    with response:
        raw=response.read() if method=='GET' else b''
        headers=dict(response.headers)
        record={'url':url,'finalUrl':response.url,'status':response.status,'redirects':redirects.chain,'headers':headers,'headersMs':round(headers_ms,2),'totalMs':round((time.perf_counter()-started)*1000,2)}
        if method=='GET':
            record['transferBytes']=len(raw)
            body=gzip.decompress(raw) if response.headers.get('Content-Encoding')=='gzip' else raw
            record['decodedBytes']=len(body)
            return record,body
        return record,b''

def safe(url,method='HEAD'):
    try:return request(url,method)
    except Exception as error:return {'url':url,'error':str(error)},b''

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--url',default='https://www.neurovascularatlas.com/')
    parser.add_argument('--output',default='docs/revision149-live-hosting.json')
    args=parser.parse_args()
    home,html=safe(args.url,'GET')
    origin=home.get('finalUrl',args.url)
    parsed=urllib.parse.urlsplit(origin)
    bare=parsed.netloc.removeprefix('www.')
    targets=['http://'+bare+'/', 'https://'+bare+'/',urllib.parse.urljoin(origin,'robots.txt'),urllib.parse.urljoin(origin,'sitemap.xml'),urllib.parse.urljoin(origin,'anatomy/manifest.json')]
    text=html.decode('utf8',errors='replace')
    targets.extend(urllib.parse.urljoin(origin,u) for u in re.findall(r'(?:src|href)="([^"]+\.(?:js|css))"',text))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        probes=[r[0] for r in pool.map(safe,targets)]
    manifest_record,body=safe(urllib.parse.urljoin(origin,'anatomy/manifest.json'),'GET')
    try:
        manifest=json.loads(body)
        manifest_record['release']=manifest.get('release')
        files=sorted({s['asset']['file'] for s in manifest['structures'] if s.get('asset') and s.get('system') in ('bone','artery')})
        for file in files:
            revision=manifest.get('assetRevisions',{}).get(file,manifest.get('release',''))
            probes.append(safe(urllib.parse.urljoin(origin,'anatomy/'+file)+'?v='+urllib.parse.quote(revision))[0])
    except Exception as error:manifest_record['parseError']=str(error)
    report={'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'home':home,'catalogue':manifest_record,'probes':probes,'limitations':['Single HTTP probes from the test environment, not mobile browser timings.','GitHub Pages controls its own compression and cache headers; local Nginx settings do not change GitHub Pages.','No hosting, DNS, account or live source changes are made by this audit.']}
    with open(args.output,'w') as handle:json.dump(report,handle,indent=2)
    print(json.dumps({'output':args.output,'liveRelease':manifest_record.get('release'),'probes':len(probes),'errors':[p for p in probes if p.get('error')]}))

if __name__=='__main__':main()
