import scrapy

class ImageSpider(scrapy.Spider):
    name = "words"
    import urllib
    index = 0

    #removed=['们','这','为','说','时','对','过','发','种','经', '么', '动']
    word_list= ['的','一', '是','不','了','在','人','有','我','他',
    '个','中','来','上','大','和','国',
    '地','到', '以','要','就','出','会','可',
    '也','你','生','能','而','子','那','得','于',
    '着','下', '自','之','年','后','作','里',
    '用','道', '行','所','然','家','事','成','方',
    '多','去','法','学','如','都','同','现',
    '当','没','面','起','看','定','天','分','还',
    '进','好', '小','部','其','些','主','样','理','心',
    '她','本', '前','开','但','因','只','从','想','实',
    '日','军', '者','意','无','力','它','与','长','把',
    '机','十', '民','第','公','此','已','工','使','情',
    '明','性', '知','全','三','又','关','点','正','业',
    '外','将', '两','高','间','由','问','很','最','重',
    '并','物', '手','应','战','向','头','文','体','政',
    '美','相', '见','被','利','什','二','等','产','或',
    '新','己', '制','身','果','加','西','斯','月','话',
    '合','回', '特','代','内','信','表','化','老','给',
    '世','位', '次','度','门','任','常','先','海','通',
    '教','儿', '原','东','声','提','立','及','比','员',
    '们','这','为','说','时','对','过','发','种','经', '么', '动'
    ]
    
    custom_settings = {
        'ITEM_PIPELINES': {'chinese_words.pipelines.CustomPipeline': 1},
        'IMAGES_STORE': 'images/',
    }
    

    def start_requests(self):
        base_url = 'http://www.fonts.net.cn/commercial-free-32767/fonts-zh/tag-heiti-1.html?previewText={word}'

        for word_str in self.word_list:
            url = base_url.format(word=word_str )
            yield scrapy.Request( url, callback=self.parse )

    def parse(self,response):
        image_urls = []
        image_names = []
        images = response.css('div.site_font_list_item_body > a')
        count = 0
        for image in images:   
            image_urls.append(image.css("img::attr(src)").extract_first())
            image_names.append(str(self.index) + "__" + str(count))
            count += 1
            print(image.css("img::attr(src)").extract_first())

        self.index+=1
        yield {
            'image_urls': image_urls,
            'image_name': image_names
        }
        #item["image_urls"] = image_urls
        #print(image_urls)
    


