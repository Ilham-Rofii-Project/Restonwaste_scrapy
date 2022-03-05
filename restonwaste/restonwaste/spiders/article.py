import scrapy


class Result10Spider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['www.restonwaste.co.uk']
    start_urls = ['https://www.restonwaste.co.uk/news/']

    def parse(self, response):
        for i in response.xpath("//h2[@class='w-full']/a"):
            title = i.xpath(".//text()").get()
            link = i.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_article, meta={'title': title,
                                                                               'link': link })

        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield (scrapy.Request(url=next_page, callback=self.parse))

    def parse_article(self, response):
        title = response.request.meta['title']
        link = response.request.meta['link']
        image = response.xpath("//p/img/@srcset").getall()
        if image:
            image=image[0]
            image = image.split(',')[0]
            image = image.split(' ')[0]
        else:
            image='Not Found'
        text = ''
        url = response.xpath("//p/a/text()")
        text_link = []
        for i in url:
            text_link += [i.get()]
        url = response.xpath("//p/span/text()")
        text_link = []
        for i in url:
            if len(i.get())<150:
                text_link += [i.get()]
        url = response.xpath("//article/descendant::node()/text()")
        for i in url:
            exists = False
            for j in text_link:
                if i.get().strip() == j.strip():
                    exists = True
            if exists == True:
                text = text[:-1]
                text += ' ' + i.get() + ' '
            else:
                text += i.get().strip() + '\n'
        text2 = ''
        for i in text.split('\n'):
            if i != '':
                text2 += i + '\n'
        yield {'title': title,
               'link': link,
               'text': text2,
               'image': image}
