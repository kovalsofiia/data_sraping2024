import scrapy
from mkr.items import MkrItem, ShopItem

class AudiosysSpider(scrapy.Spider):
    name = "audiosys"
    allowed_domains = ["hotline.ua"]
    start_urls = [f"https://hotline.ua/ua/av/akusticheskie-kolonki/?p={1}"]

    def parse(self, response):
        items = response.css('.list-body__content .list-item')

        for item in items:
            name = item.css('.item-title::text').get().strip()
            url = response.urljoin(item.css('.item-title::attr(href)').get())
            price = item.css('.list-item__value-price::text').get()
            image_url = response.urljoin(item.css('img::attr(src)').get())

            yield scrapy.Request(
                url=url,
                callback=self.parse_item,
                meta={"name": name, "url": url, "price": price, "image_urls": [image_url]}
            )

    def parse_item(self, response):
        shops = response.css('.content .list .list__item')
        item_name = response.meta["name"]
        item_url = response.meta["url"]
        item_price = response.meta["price"]
        image_urls = response.meta["image_urls"]
        yield MkrItem(
            name=item_name,
            url=item_url,
            price=item_price,
            image_urls=image_urls
        )
        
        for shop in shops:
            shop_name = shop.css('.shop__title::text').get().strip()
            shop_url = response.urljoin(shop.css('.shop__title::attr(href)').get())
            shop_price = shop.css('.price__value::text').get()
            yield ShopItem(
                item_name=item_name,
                shop_name=shop_name,
                shop_price=shop_price,
                shop_url=shop_url,
            )
