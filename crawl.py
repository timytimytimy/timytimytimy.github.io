#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import urlparse
import codecs

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
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=1&n=1&pid=hp&mkt=zh-CN'
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
    html_tpl = u'''
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
  	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
    <style>
  		.col-md-4 {padding: 0;}
  		#download {display: block; line-height: 30px;text-align: center;font-size:1rem;background:rgba(255,255,255,0.8);position: fixed;right: 50px;bottom: 25px;border-radius:5px;padding-left:10px;padding-right:10px;}
  	    .download-btn {display:none;font-size:1.5rem;height:2rem;width:2rem;position:absolute;right:10px;bottom:10px;border-radius:5px;background:rgba(255,255,255,0.8);text-align: center;}
        .download-btn::before {color:#007bff;line-height: 2rem;}
        .col-md-4:hover .download-btn {display:block}
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
        if not filename.endswith('.jpg') or not filename.endswith('.png'):
            continue
        repl += '<div class="col-md-4 col-sm-6 col-xs-12"><img src="data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs=" data-src="images/{}" class="img-fluid lazyload" width="1920" height="1080"><a class="download-btn fas fa-arrow-down" href="images/{}"></a></div>\n'.format(filename, filename)
    html = html_tpl % (dir_list[0], title, repl)
    with codecs.open('index.html', 'w') as f:
        f.write(html)


if __name__ == '__main__':
    title = crawl_daily()
    gen_html(title)
