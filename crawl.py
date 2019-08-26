import sys
import requests
import urlparse

def crawl_all():
    for i in xrange(8):
        url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx={}&n=1&pid=hp'.format(i)
        data = requests.get(url).json()
        image_data = data['images'][0]
        img_url = urlparse.urljoin(url, image_data['url'])
        title = image_data['copyright']
        date = image_data['startdate']
        filename = 'images/{}.jpg'.format(date)
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
    date = image_data['startdate']
    filename = 'images/{}.jpg'.format(date)
    rsp = requests.get(img_url)
    with open(filename, 'wb') as file:
        file.write(rsp.content)
    print 'save image to', filename


def gen_html():
    import os
    import datetime
    for parent, dirnames, filenames in os.walk('images'):
        filenames = sorted(list(filenames), reverse=True)
        for filename in filenames:
            print '<div class="col-md-4"><img src="images/{}" class="img-responsive"></div>'.format(filename)


if __name__ == '__main__':
    crawl_daily()
