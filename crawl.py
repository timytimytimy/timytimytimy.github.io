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
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&pid=hp'
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


def gen_html():
    import os
    import datetime
    # for parent, dirnames, filenames in os.walk('images'):
    #     filenames = sorted(list(filenames), reverse=True)
    #     for filename in filenames:
    #         print '<div class="col-md-4"><img src="images/{}" class="img-responsive"></div>'.format(filename)
    dir_list = os.listdir('images')
    if not dir_list:
        return
    else:
        dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(os.path.split(os.path.realpath(__file__))[0] + '/images', x)), reverse=True)
        for filename in dir_list:
            if not filename.endswith('.jpg'):
                continue
            print '<div class="col-md-4 col-sm-6 col-xs-12"><img src="data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs=" data-src="images/{}" class="img-responsive lazyload" width="1117" height="628"></div>'.format(filename)


if __name__ == '__main__':
    crawl_daily()
    gen_html()
