import urllib

url = ['http://google.com','http://bing.com']

for i in url:
    html = urllib.urlopen(i).read()
    print(html.encode('utf-8')) 
