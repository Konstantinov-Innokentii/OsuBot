import scrapy

group_urls = open('/home/flamingshalom/PycharmProjects/OSUshedulebot/shedule/shedule/spiders/group_urls.txt','r')

groups = []
start_urls_global = []
line_counter = 0
for line in group_urls.readlines():
    if line_counter % 2 == 0:
        groups.append(line.replace('\n', ''))
    else:
        start_urls_global.append(line.replace('\n', ''))
    line_counter += 1


class OsuSpider (scrapy.Spider):
    name = "OsuSpider"
    allowed_domains = ["osu.ru"]
    group_urls = open('/home/flamingshalom/OSUshedulebot/shedule/shedule/spiders/group_urls.txt','r')
    start_urls = []
    line_counter = 0
    for line in group_urls.readlines():
        if line_counter % 2 != 0:
            start_urls.append(line.replace('\n',''))
        line_counter += 1

    def parse(self, response):
        global groups
        global start_urls_global
        #TODO: get path with os moodule
        path = '/home/flamingshalom/OSUshedulebot/shedule/{}.json'.format(groups[start_urls_global.index(response.url)])
        f = open(path, 'w')

        #'/home/flamingshalom/PycharmProjects/OSUshedulebot/shedule/15КБРЗПО.json'
        f.write('[\n{')
        #for sel in response.xpath('//tr[@style="background:#dfd;font-weight:bold"]/td[@pare_id]'):
        for sel in response.xpath('//tr[@style="background:#dfd;font-weight:bold"]'):
            #'Группа' : response.url
            #'Пара' : sel.xpath('./td[@pare_id]/@pare_id').extract(),
            f.write('"Пара":'+str(sel.xpath('./td[@pare_id]/@pare_id').extract()).replace("'",'"')+',')
            f.write('"Аудитория":'+str(sel.xpath('./td[@pare_id]/a[1]/span/text()').extract()).replace("'",'"')+',')
            f.write('"Дисциплина":'+str(sel.xpath('./td[@pare_id]/span[@class="dis"]/text()').extract()).replace("'",'"')+',')
            f.write('"Тип":'+str(sel.xpath('./td[@pare_id]/span[2]/text()').extract()).replace("'",'"')+',')
            f.write('"Групповые занятия":'+str(sel.xpath('./td/table//td//*/text()').extract()).replace("'",'"')+'}\n')
            f.write(']')
            f.close()
            #'Пара': sel.xpath('./td[@pare_id]/@pare_id').extract(),
            #'Аудитория': sel.xpath('./td[@pare_id]/a[1]/span/text()').extract(),
            #'Дисциплина': sel.xpath('./td[@pare_id]/span[@class="dis"]/text()').extract(),
            #'Тип': sel.xpath('./td[@pax  re_id]/span[2]/text()').extract(),
            #'Физ-ра': sel.xpath('./td/table//td//*/text()').extract()


        #yield response.xpath('//tr[@style="background:#dfd;font-weight:bold"]/td/table//td//*/text()').extract()
        # 'Физ-ра' :sel.xpath('./td/table//td//*/text()').extract()
        #filename = 'data.txt'
        #with open(filename,'wb') as f:
        #   f.write(data)
        # response.xpath('//tr[@style="background:#dfd;font-weight:bold"]/td/table')
        # response.xpath('//tr[@style="background:#dfd;font-weight:bold"]/td/table//td//*/text()').extract()





