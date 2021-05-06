import scrapy
from scrapy_splash import SplashRequest
from scrapy import *
import requests
from bs4 import BeautifulSoup


class TheGioiDiDong_iphone(scrapy.Spider):
    name = 'iphone_TGDD'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://www.thegioididong.com/dtdd-apple-iphone"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("viewmore")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        items = response.css('li.item')
        print(len(items))
        for item in items:
            price = item.css('div.price')[0].css('strong::text').get()
            price = price[0:len(price) - 1] + ' VNĐ'
            thongtin = item.css('figure.bginfo')[0].css('span::text').getall()
            screen = thongtin[0]
            memory = thongtin[1]
            Camera_sau = str(thongtin[2]).replace('Camera sau:', '')
            Camera_truoc = str(thongtin[3]).replace('Camera trước:', '')
            pin = str(str(thongtin[4]).split(',')[0]).replace('Pin ', '')
            sac = str(str(thongtin[4]).split(',')[1]).replace(' Sạc ', '')
            yield {
                'Tên sản phẩm': item.css('h3::text').get(),
                'Giá sản phẩm': price,
                'Màn hình': screen,
                'Bộ nhớ': memory,
                'Camera sau': Camera_sau,
                'Camera trước': Camera_truoc,
                'Pin': pin,
                'Sạc': sac
            }


class TheGioiDiDong_macbook(scrapy.Spider):
    name = 'mackbook_TGDD'
    start_urls = ["https://www.thegioididong.com/laptop-apple-macbook"]

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response, ):
        items = response.css('li.item')
        for item in items:
            price = str(item.css('div.price')[0].css('strong::text').get())
            price = price[0: len(price) - 1] + ' VNĐ'
            thongtin = item.css('figure.bginfo')[0].css('span::text').getall()
            link = 'https://www.thegioididong.com/' + str(item.css('a').attrib['href'])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            color = soup.find('div', class_='rowdetail').find('li', class_='item').text.replace(' ', '').replace('\n',
                                                                                                                 '').replace(
                '\r', '')
            yield {
                "Tên sản phẩm": item.css('h3::text').get(),
                "Giá sản phẩm": price,
                "Ram": item.css('div.props').css('span::text').getall()[0],
                "Ổ cứng": item.css('div.props').css('span::text').getall()[1],
                "Màn hình": thongtin[0],
                "CPU": thongtin[1],
                'Card đồ họa': str(thongtin[2]).replace('Card đồ họa:', ''),
                "Khối lượng": str(str(thongtin[3]).split(',')[0]).replace('Nặng:', ''),
                'Thời gian sử dụng': str(str(thongtin[3]).split(',')[1]),
                "Màu sắc": color
            }


class TheGioiDiDong_ipad(scrapy.Spider):
    name = 'ipad_TGDD'
    start_urls = ["https://www.thegioididong.com/may-tinh-bang-apple-ipad"]

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        items = response.css('li.item')
        for item in items:
            link = 'https://www.thegioididong.com/' + str(item.css('a').attrib['href'])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            _items = soup.find('ul', class_='owl-carousel').find_all('li', class_='item')
            mau = ''
            for _item in _items:
                if _item.get_attribute_list('data-order')[0] != None:
                    mau += _item.text.replace('\n', '').replace(' ', '').replace('\r', '') + ' ,'
            mau = mau[0: len(mau) - 2]

            price = item.css('div.price strong::text').get()
            price = price[0: len(price) - 1] + " VNĐ"
            thongtin = item.css('figure.bginfo')[0].css('span::text').getall()

            yield {
                'Tên sản phẩm': item.css('h3::text').get(),
                "Giá sản phẩm": price,
                'Màu sắc': mau,
                'Màn hình': str(thongtin[0]).replace('"', ' inch').replace(',', ''),
                'Chip': str(thongtin[1]).replace('Chip ', ''),
                'Ram': str(str(thongtin[2]).split(', ')[0]).replace('RAM ', ''),
                'Bộ nhớ': str(str(thongtin[2]).split(', ')[1]).replace('ROM ', ''),
                'Pin sạc': thongtin[4]
            }


class TheGioiDiDong_watch(scrapy.Spider):
    name = 'apple_watch_tgdd'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://www.thegioididong.com/dong-ho-thong-minh-apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("viewmore")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("viewmore")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        items = response.css('li.item')
        for item in items:
            price = str(item.css('div.price strong::text')[0].get())
            price = price[0:len(price) - 2] + ' VNĐ'
            link = 'https://www.thegioididong.com/' + item.css('a').attrib['href']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            color = soup.find('li', class_='item').find('span').text
            thongtin = item.css('figure.bginfo span::text')
            yield {
                'Tên sản phẩm': item.css('h3::text').get(),
                'Giá sản phẩm': price,
                "Giảm giá": item.css('div.price i::text').get(),
                "Nghe gọi": item.css('div.props span::text').get(),
                'Màu': color,
                'Màn hình': thongtin[0].get(),
                "Hệ điều hành": thongtin[1].get(),
                'Thời gian sử dụng': thongtin[2].get(),
                'Tính năng': thongtin[3].get()

            }


class TheGioiDiDong_watch(scrapy.Spider):
    name = 'xtmobile_iphone'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://www.xtmobile.vn/apple"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("pagination-more")[0].getElementsByClassName("fa fa-caret-down")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                assert(splash:runjs('try{document.getElementsByClassName("pagination-more")[0].getElementsByClassName("fa fa-caret-down")[0].click();}catch(e){}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        items = response.css('div.product-base-grid')
        for item in items:
            price = item.css('div.price::text').get()
            price = price[0:len(price) - 1] + ' VNĐ'
            link = 'https://www.xtmobile.vn' + item.css('h3')[0].css('a').attrib['href']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            colors = soup.find('ul', class_='color-list-show').find_all('li')
            mau = ''
            for c in colors:
                mau += c.find('p').text + ' '

            thongtin = soup.find('ul', class_='parametdesc').find_all('strong')

            yield {
                'Tên sản phẩm': item.css('h3 a::text')[0].get(),
                'Giá sản phẩm': price,
                'Màu': mau,
                'Màn hình': thongtin[0].text,
                'Camera trước': thongtin[1].text,
                'Camera sau': thongtin[2].text,
                'Chip': thongtin[3].text,
                'Ram': thongtin[4].text,
                'Bộ nhớ trong': thongtin[5].text,
                'Thẻ sim': thongtin[6].text,
                'Pin': thongtin[7].text,
                'Hệ điều hành': thongtin[8].text
            }


class Mac_One_macbook(scrapy.Spider):
    name = 'macbook_mac_one'
    # allowed_domains = ["thegioididong.com"]
    start_urls = ["https://macone.vn/macbook-cu-moi/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("nextpostslink")[0].click();'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        items = response.xpath('//*[@id="main"]/div[2]/div/div[1]/div[2]/div/div[3]/div').css('div.item-product')
        for item in items:
            price = item.css('div.price-box strong::text').get()
            price = price[0:len(price) - 1] + "VNĐ"
            link = item.css('div.product-name h3 a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtin = soup.find('div', class_='table-responsive').find('tbody').find_all('tr')
            # thongtin = soup.find('//*[@id="motasanpham"]/div[1]/div/table/tbody/tr[1]/td[2]').text
            # print(thongtin[0].find_all('td')[1].text)
            yield {
                'Tên sản phẩm': item.css('div.product-name h3 a strong::text').get(),
                'Giá sản phẩm': price,
                'Link': link,
                'CPU': thongtin[0].find_all('td')[1].text,
                'Ram': thongtin[1].find_all('td')[1].text,
                "Màn hình": thongtin[2].find_all('td')[1].text,
                'Ổ cứng': thongtin[4].find_all('td')[1].text,
                'Khối lượng': thongtin[5].find_all('td')[1].text,
                'Camera': thongtin[6].find_all('td')[1].text,
            }

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )


class Mac_One_phu_kien(scrapy.Spider):
    name = 'MacOne_phu_kien'
    start_urls = ["https://macone.vn/phu-kien-apple/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("nextpostslink")[0].click();'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                endpoint="render.html",
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        items = response.xpath('//*[@id="main"]/div[2]/div/div[1]/div/div/div[3]/div').css('div.item-product')
        for item in items:
            price = item.css('div.price-box strong::text').get()
            price = price[0:len(price) - 1] + "VNĐ"
            link = item.css('div.product-name h3 a').attrib['href']
            # req = requests.get(link, headers=headers)
            # soup = BeautifulSoup(req.text, "lxml")
            # thongtin = soup.find('div', class_='table-responsive').find('tbody').find_all('tr')
            # thongtin = soup.find('//*[@id="motasanpham"]/div[1]/div/table/tbody/tr[1]/td[2]').text
            # print(thongtin[0].find_all('td')[1].text)
            yield {
                'Tên sản phẩm': item.css('div.product-name h3 a::text').get(),
                'Giá sản phẩm': price,
                'Link': link,
            }

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )


class Clickbuy_iphone(scrapy.Spider):
    name = 'click_buy_iphone'
    start_urls = ["https://hcm.clickbuy.com.vn/danh-muc/iphone/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementById("sb-infinite-scroll-load-more-1").getElementsByTagName("a")[0].click();}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        items = response.xpath('//*[@id="main"]/ul').css('li.col-6')
        for item in items:
            link = item.css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            try:
                price = str(soup.find('p', class_='price').find('span').text)
                price = price.replace('\xa0₫', ' VNĐ')
            except:
                price = None
            try:
                color = soup.find('tr',
                                  class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_mau-sac').find(
                    'p').text
            except:
                color = None
            try:
                memory = soup.find('tr',
                                   class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_bo-nho-trong').find(
                    'p').text
            except:
                memory = None
            try:
                camera_chinh = soup.find('tr',
                                         class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_camera-chinh').find(
                    'p').text
            except:
                camera_chinh = None
            try:
                camera_phu = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_camera-phu').find(
                    'p').text
            except:
                camera_phu = None
            try:
                CPU = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_cpu').find(
                    'p').text
            except:
                CPU = None
            try:
                dophangiai = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_do-phan-giai-man-hinh').find(
                    'p').text
            except:
                dophangiai = None
            try:
                pin = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_dung-luong-pin').find(
                    'p').text
            except:
                pin = None
            try:
                hedieuhanh = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_he-dieu-hanh').find(
                    'p').text
            except:
                hedieuhanh = None
            try:
                kichthuocmanhinh = soup.find('tr',
                                             class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_kich-thuoc-man-hinh').find(
                    'p').text
            except:
                kichthuocmanhinh = None
            try:
                ram = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_ram').find(
                    'p').text
            except:
                ram = None
            yield {
                'Tên sản phẩm': item.css('h2.woocommerce-loop-product__title::text').get(),
                'Giá sản phẩm': price,
                'Link': link,
                'Màu sắc': color,
                'Bộ nhớ trong': memory,
                'Camera chính': camera_chinh,
                'Camera phụ': camera_phu,
                'CPU': CPU,
                "Độ phân giải màn hình": dophangiai,
                'Pin': pin,
                'Hệ điều hành': hedieuhanh,
                'Kích thước màn hình': kichthuocmanhinh,
                'Ram': ram,
            }


class Clickbuy_Apple_Watch(scrapy.Spider):
    name = 'click_buy_apple_watch'
    start_urls = ["https://hcm.clickbuy.com.vn/danh-muc/applewatch/"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('for(var i = 0 ; i < 10 ; i ++){document.getElementById("sb-infinite-scroll-load-more-1").getElementsByTagName("a")[0].click();}'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        items = response.xpath('//*[@id="main"]/ul').css('li.col-6')
        for item in items:
            link = item.css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            try:
                price = str(soup.find('p', class_='price').find('span').text)
                price = price.replace('\xa0₫', '')
            except:
                price = None
            try:
                color = soup.find('tr',
                                  class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_mau-sac').find(
                    'p').text
            except:
                color = None
            try:
                memory = soup.find('tr',
                                   class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_bo-nho-trong').find(
                    'p').text
            except:
                memory = None
            try:
                camera_chinh = soup.find('tr',
                                         class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_camera-chinh').find(
                    'p').text
            except:
                camera_chinh = None
            try:
                camera_phu = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_camera-phu').find(
                    'p').text
            except:
                camera_phu = None
            try:
                CPU = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_cpu').find(
                    'p').text
            except:
                CPU = None
            try:
                dophangiai = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_do-phan-giai-man-hinh').find(
                    'p').text
            except:
                dophangiai = None
            try:
                pin = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_dung-luong-pin').find(
                    'p').text
            except:
                pin = None
            try:
                hedieuhanh = soup.find('tr',
                                       class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_he-dieu-hanh').find(
                    'p').text
            except:
                hedieuhanh = None
            try:
                kichthuocmanhinh = soup.find('tr',
                                             class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_kich-thuoc-man-hinh').find(
                    'p').text
            except:
                kichthuocmanhinh = None
            try:
                ram = soup.find('tr',
                                class_='woocommerce-product-attributes-item woocommerce-product-attributes-item--attribute_pa_ram').find(
                    'p').text
            except:
                ram = None
            yield {
                'Tên sản phẩm': item.css('h2.woocommerce-loop-product__title::text').get(),
                'Giá sản phẩm': price,
                'Link': link,
                'Màu sắc': color,
                'Bộ nhớ trong': memory,
                'Camera chính': camera_chinh,
                'Camera phụ': camera_phu,
                'CPU': CPU,
                "Độ phân giải màn hình": dophangiai,
                'Pin': pin,
                'Hệ điều hành': hedieuhanh,
                'Kích thước màn hình': kichthuocmanhinh,
                'Ram': ram,
            }


class Cell_phone_iphone(scrapy.Spider):
    name = 'cell_phone_iphone'
    start_urls = ["https://cellphones.com.vn/mobile/apple.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("pagination")[1].getElementsByTagName("a")[0].click();'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('li.cate-pro-short')
        for item in items:
            price = str(item.css('span.price::text').get())
            link = item.css('div.lt-product-group-info')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtin = soup.find('div', class_='content')

            yield {
                "Tên sản phẩm": str(item.css('div.lt-product-group-info')[0].css('h3::text').get()).replace('\t', ''),
                "Link": link,
                "Giá sản phẩm": price.replace('\xa0₫', ' VNĐ'),
                "Kích thước màn hình": thongtin.find_all('tr')[0].find_all('td')[1].text,
                "Công nghệ màn hình": thongtin.find_all('tr')[1].find_all('td')[1].text,
                "Camera sau": thongtin.find_all('tr')[2].find_all('td')[1].text,
                "Camera trước": thongtin.find_all('tr')[3].find_all('td')[1].text,
                "Chip": thongtin.find_all('tr')[4].find_all('td')[1].text,
                "Ram": thongtin.find_all('tr')[5].find_all('td')[1].text,
                "Bộ nhớ trong": thongtin.find_all('tr')[6].find_all('td')[1].text,
                "Pin": thongtin.find_all('tr')[7].find_all('td')[1].text,
                "Thẻ sim": thongtin.find_all('tr')[8].find_all('td')[1].text,
                'Hệ điều hành': thongtin.find_all('tr')[9].find_all('td')[1].text,
            }
        if str(response.css('ul.pagination')[1].css('a::text').get()) == 'Tiếp ':
            yield SplashRequest(
                response.url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )


class Cell_phone_macbook(scrapy.Spider):
    name = 'cell_phone_macbook'
    start_urls = ["https://cellphones.com.vn/laptop/mac.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(1))
                assert(splash:runjs('document.getElementsByClassName("pagination")[1].getElementsByTagName("a")[0].click();'))
                assert(splash:wait(1))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.products-container')[0].css('li')
        for item in items:
            price = str(item.css('span.price::text').get()).replace('\xa0₫', ' VNĐ')
            link = item.css('div.lt-product-group-image')[0].css('a').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtin = soup.find('div', class_='content')
            if price == 'Đăng ký nhận tin':
                CPU = None
                RAM = None
                O_cung = None
                Kich_thuoc_man_hinh = None
                Do_phan_giai = None
                He_dieu_hanh = None
            else:
                CPU = thongtin.find_all('tr')[0].find_all('td')[1].text
                RAM = thongtin.find_all('tr')[2].find_all('td')[1].text
                O_cung = thongtin.find_all('tr')[3].find_all('td')[1].text
                Kich_thuoc_man_hinh = thongtin.find_all('tr')[4].find_all('td')[1].text
                Do_phan_giai = thongtin.find_all('tr')[5].find_all('td')[1].text
                He_dieu_hanh = thongtin.find_all('tr')[7].find_all('td')[1].text
            yield {
                "Tên sản phẩm": item.css('div.lt-product-group-info')[0].css('h3::text').get(),
                "Giá sản phẩm": price,
                "CPU": CPU,
                "RAM": RAM,
                'Ổ cứng': O_cung,
                'Kích thước màn hình': Kich_thuoc_man_hinh,
                "Độ phân giải màn hình": Do_phan_giai,
                "Hệ điều hành": He_dieu_hanh,
                "Link": link
            }

        if str(response.css('ul.pagination')[1].css('a::text').get()) == 'Tiếp ':
            yield SplashRequest(
                response.url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )


class dienthoaimoi_iphone(scrapy.Spider):
    name = 'dienthoaimoi_iphone'
    start_urls = ["https://dienthoaimoi.vn/dien-thoai-apple-iphone-pcm135.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next-page")[0].click();'))
                assert(splash:wait(3))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.product_grid')[0].css('div.item')
        for item in items:
            price = item.css('div.price_current::text').get()
            link = item.css('a.name').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtins = soup.find('table', class_='charactestic_table').find_all('tr')
            pin = ''
            for thongtin in thongtins:
                if str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                    '') == 'Công nghệ màn hình':
                    Cong_nghe_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n',
                                                                                                        '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Độ phân giải':
                    Do_phan_giai = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Màn hình rộng':
                    Kich_thuoc_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n',
                                                                                                         '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Camera sau':
                    Camera_sau = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                                  '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Camera trước':
                    Camera_truoc = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Camera trước':
                    Camera_truoc = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Đèn Flash':
                    flash = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Hệ điều hành':
                    he_dieu_hanh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Dung lượng pin':
                    pin = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r', '')
            yield {
                "Tên sản phẩm": str(item.css('h2 a::text').get()).replace('\n', '').replace('\t', ''),
                "Giá sản phẩm": price.replace('₫', ' VNĐ'),
                "Công nghệ màn hình": Cong_nghe_man_hinh,
                "Độ phân giải": Do_phan_giai,
                "Kích thước màn hình": Kich_thuoc_man_hinh,
                "Camera sau": Camera_sau,
                "Camera trước": Camera_truoc,
                "Đèn flash": flash,
                "Pin": (pin == '' and None or pin),
                "Hệ điều hành": he_dieu_hanh,
                "Link": link
            }

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )


class dienthoaimoi_ipad(scrapy.Spider):
    name = 'dienthoaimoi_ipad'
    start_urls = ["https://dienthoaimoi.vn/tablet--may-tinh-bang-apple-ipad-pcm137.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next-page")[0].click();'))
                assert(splash:wait(3))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.product_grid')[0].css('div.item')
        for item in items:
            price = item.css('div.price_current::text').get()
            link = item.css('a.name').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtins = soup.find('table', class_='charactestic_table').find_all('tr')
            loai_man_hinh = ''
            mau_man_hinh = ''
            CPU = ''
            He_dieu_hanh = ''
            for thongtin in thongtins:
                if str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                    '') == 'Loại màn hình':
                    loai_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Màu màn hình':
                    mau_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Loại CPU (Chipset)':
                    CPU = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Hệ điều hành':
                    He_dieu_hanh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')

            yield {
                "Tên sản phẩm": str(item.css('h2 a::text').get()).replace('\n', '').replace('\t', ''),
                "Giá sản phẩm": price.replace('₫', ' VNĐ'),
                "Loại màn hình": (loai_man_hinh == '' and None or loai_man_hinh),
                "Màu màn hình": (mau_man_hinh == '' and None or mau_man_hinh),
                "CPU": (CPU == '' and None or CPU),
                'Hệ điều hành': (He_dieu_hanh == '' and None or He_dieu_hanh),
                "Link": link
            }

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )


class dienthoaimoi_applewatch(scrapy.Spider):
    name = 'dienthoaimoi_applewatch'
    start_urls = ["https://dienthoaimoi.vn/dong-ho-apple-watch-pc298.html"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("next-page")[0].click();'))
                assert(splash:wait(3))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.product_grid')[0].css('div.item')
        for item in items:
            price = item.css('div.price_current::text').get()
            link = item.css('a.name').attrib['href']
            req = requests.get(link, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
            thongtins = soup.find('table', class_='charactestic_table').find_all('tr')
            man_hinh = ''
            kich_thuoc_man_hinh = ''
            thoi_gian_su_dung = ''
            CPU = ''
            He_dieu_hanh = ''
            ngon_ngu = ''
            for thongtin in thongtins:
                if str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                    '') == 'Màn hình':
                    man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                                '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Kích thước màn hình':
                    kich_thuoc_man_hinh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n',
                                                                                                         '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Thời gian sử dụng':
                    thoi_gian_su_dung = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n',
                                                                                                       '').replace('\r',
                                                                                                                   '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Hệ điều hành':
                    He_dieu_hanh = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace(
                        '\r', '')
                elif str(thongtin.find_all('td')[0].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                      '') == 'Ngôn ngữ':
                    ngon_ngu = str(thongtin.find_all('td')[1].text).replace('\t', '').replace('\n', '').replace('\r',
                                                                                                                '')

            yield {
                "Tên sản phẩm": str(item.css('h2 a::text').get()).replace('\n', '').replace('\t', ''),
                "Giá sản phẩm": price.replace('₫', ' VNĐ'),
                "màn hình": (man_hinh == '' and None or man_hinh),
                "Kích thước màn hình": (kich_thuoc_man_hinh == '' and None or kich_thuoc_man_hinh),
                "Thời gian sử dụng": (thoi_gian_su_dung == '' and None or thoi_gian_su_dung),
                'Hệ điều hành': (He_dieu_hanh == '' and None or He_dieu_hanh),
                "Ngôn ngữ": (ngon_ngu == '' and None or ngon_ngu),
                "Link": link
            }

        yield SplashRequest(
            response.url,
            callback=self.parse,
            headers=headers,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )


class dien_may_xanh_iphone(scrapy.Spider):
    name = 'dien_may_xanh_iphone'
    start_urls = ["https://www.dienmayxanh.com/dien-thoai-apple-iphone"]
    script = """
            function main(splash)
                local url = splash.args.url
                assert(splash:go(url))
                assert(splash:wait(2))
                assert(splash:runjs('document.getElementsByClassName("loadmore")[0].click();'))
                assert(splash:wait(2))
                return {
                    html = splash:html(),
                    url = splash:url(),
                }
            end
            """

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        for url in self.start_urls:
            yield SplashRequest(
                url,
                callback=self.parse,
                headers=headers,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        items = response.css('div.prdWrFixHe')
        print(len(items))
        for item in items:
            thongtins = item.css('div.prdTooltip')[0]
            yield {
                "Tên sản phẩm": item.css('div.prdName span::text').get(),
                "Giá sản phẩm": str(item.css('strong.prPrice::text').get()).replace('₫', ' VNĐ'),
                "Màn hình": str(thongtins.css('span::text')[0].get()).split(', ')[0].replace('"', ' inch'),
                "Chip": str(thongtins.css('span::text')[0].get()).split(', ')[1],
                'RAM': str(thongtins.css('span::text')[1].get()).split(', ')[0].replace('RAM ', ''),
                'Bộ nhớ trong': str(thongtins.css('span::text')[1].get()).split(', ')[1].replace('ROM ', ''),
                'Camera sau': str(thongtins.css('span::text')[2].get()).replace('Camera sau: ', ''),
                'Camera trước': str(thongtins.css('span::text')[3].get()).replace('Camera trước:  ', ''),
                'Pin': str(thongtins.css('span::text')[4].get()).split(', ')[0].replace('Pin ', ''),
                'Sạc': str(thongtins.css('span::text')[4].get()).split(', ')[1].replace('Sạc ', '')
            }

