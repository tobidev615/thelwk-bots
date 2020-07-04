import scrapy
import time
from datetime import date

def image_handler(value):
    new=value.split('40w')
    newest=new[0].replace('40x40bb.jpg ', '740x740bb.jpg')
    return newest

class AppleChartSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'chartsng.pipelines.AppleChartPipeline': 300,
        }
    }
    name = 'apple_chart'
    allowed_domains = ['music.apple.com/sz/playlist/top-100-nigeria/pl.2fc68f6d68004ae993dadfe99de83877']
    start_urls = [
        'https://music.apple.com/sz/playlist/top-100-nigeria/pl.2fc68f6d68004ae993dadfe99de83877/',
        'https://music.apple.com/ng/playlist/alt%C3%A9-cruise/pl.2786e86e72014805bcb2f84d4e68fded',
        'https://music.apple.com/ng/playlist/naija-hits/pl.59d18bb92273474dbb69bb6be0dcda3f',   
        ]

    def parse(self, response):
        today = date.today()
        dater = today.strftime("%Y-%m-%d")

        time.sleep(5)
        counter=0

        songs_row = response.xpath("//div[@class='row web-preview song']")
        playlist = response.xpath("normalize-space(//div[@class = 'header-and-songs-list']//div[@class = 'album-header-metadata']/h1)").get()        
        
        if 'Cruise' in playlist:
            playlist = 'alternative'
        elif 'Top 100' in playlist:
            playlist = 'top_100'
        elif 'Naija' in playlist:
            playlist = 'naija_hits'
        else:
            playlist=playlist

        for songs in songs_row:
            counter = counter + 1
            title = songs.xpath(".//div[@class='song-name typography-label']/text()").getall()
            artist = songs.xpath(".//div[@class='by-line typography-caption']/a/text()").get()
            image = songs.xpath(".//img[@class='media-artwork-v2__image']/@srcset").get()
            song_link = songs.xpath(".//div[@class='col col-album']/a/@href").get()

            yield{  'date' : dater,
                    'playlist': playlist,
                    'rank': int(counter),
                    'title': title[1],
                    'artist': artist,
                    'art_work': image_handler(image),
                    'link_to' : song_link
                    #this is the extension to add to the end of the image for full view 
                    #   /760x760bb.jpg}
                
            }