import sys
import requests
import urlparse

def crawl_all():
    for i in xrange(8, -1, -1):
        url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx={}&n=1&pid=hp'.format(i)
        data = requests.get(url).json()
        image_data = data['images'][0]
        img_url = urlparse.urljoin(url, image_data['url'])
        title = image_data['copyright']
        filename = image_data['urlbase'].replace('/th?id=OHR.', '').split('_')[0]
        filename = 'images/{}.jpg'.format(filename)
        rsp = requests.get(img_url)
        with open(filename, 'wb') as file:
            file.write(rsp.content)
        print 'save image to', filename


def crawl_daily():
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp&mkt=zh-CN'
    data = requests.get(url).json()
    image_data = data['images'][0]
    img_url = urlparse.urljoin(url, image_data['url'])
    title = image_data['copyright']
    filename = image_data['urlbase'].replace('/th?id=OHR.', '').split('_')[0]
    filename = 'images/{}.jpg'.format(filename)
    rsp = requests.get(img_url)
    with open(filename, 'wb') as file:
        file.write(rsp.content)
    print 'save image to', filename
    return title


def gen_html(title):
    import os
    import re
    html_tpl = '''
<html lang="en-US">
  <head>
  	<title>Hi</title>
  	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta property="og:image" content="https://clover123.cn/images/%s" />
    <meta property="og:type" content="webpage" />
    <meta property="og:site_name" content="clover123" />
    <meta property="og:url" content="https://clover123.cn" />
    <meta property="og:title" content="%s" />
    <meta property="og:description" content="" />
  	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  	<style>
  		.col-md-4 {padding: 0;}
  		#download {display: block; line-height: 30px;text-align: center;height: 30px; width: 100px; background:rgba(255,255,255,0.8);position: fixed;right: 50px;bottom: 25px;border-radius:5px;}
  	</style>
  	<script src="https://cdn.jsdelivr.net/npm/lazyload@2.0.0-rc.2/lazyload.js"></script>
  </head>
  <body>
  	<div class="container-fluid">
	  <div class="row">
	  %s
	  </div>
	</div>
	<a id="download" href="https://github.com/timytimytimy/timytimytimy.github.io/archive/master.zip" target="_blank">
		Download ZIP.
	</a>
	<script>lazyload();</script>
  </body>
</html>
    '''
    dir_list = os.listdir('images')
    dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(os.path.split(os.path.realpath(__file__))[0] + '/images', x)), reverse=True)
    repl = ''
    for filename in dir_list:
        if not filename.endswith('.jpg'):
            continue
        repl += '<div class="col-md-4 col-sm-6 col-xs-12"><img src="data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs=" data-src="images/{}" class="img-responsive lazyload" width="1920" height="1080"></div>\n'.format(filename)
    html = html_tpl % (dir_list[0], title, repl)
    with open('index.html', 'w') as f:
        f.write(html)


if __name__ == '__main__':
    title = crawl_daily()
    gen_html(title)
