import Drogasil.utils.process as p
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import mysql.connector

class DrogasilCleaning:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        # values are being returnedo lists
        for field in fields:
            if field not in ["sub_category"]:
                value = adapter.get(field)
                adapter[field] = p.try_index_strip(value)

        # treating the description field, that was stored as a list
        value = adapter.get('description')
        adapter['description'] = '. '.join(value)

        for field in fields:
            if field in ['product', 'brand', 'manufacturer', 'description']:
                value = adapter.get(field)
                adapter[field] = p.try_decode_upper(value)

        value = adapter.get('weight')
        adapter['weight'] = p.try_turn(value)

        for field in fields:
            if field in ['sku', 'EAN']:
                value = adapter.get(field)
                adapter[field] = p.try_turn(value)

        value = adapter.get('category')
        adapter['category'] = p.parse_category(value)

        value = adapter.get('sub_category')
        adapter['sub_category'] = p.parse_category(value, sub_category = True)

        value = adapter['sku']
        if not value:
            raise DropItem('item removed, missing sku')

        return item

class SaveToMySQL:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.conn = mysql.connector.connect(

            host = settings.get('MYSQL_HOST'),
            user = settings.get('MYSQL_USER'),
            password = settings.get('MYSQL_PASSWORD'),
            port = settings.get('MYSQL_PORT'),
            database = settings.get('MYSQL_DATABASE')

        )

        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        self.cur.execute("""
            INSERT INTO drogasil (
                    url,
                    sku,
                    EAN,
                    product,
                    brand,
                    quantity,
                    weight,
                    manufacturer,
                    description,
                    category,
                    sub_category,
                    price,
                    discount
            ) VALUES (
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,
                    %s,%s,%s,%s
            )""", (
                         item['url'], item['sku'], item['EAN'], item['product'], item['brand'],
                         item['quantity'], item['weight'], item['manufacturer'], item['description'],
                         item['category'], item['sub_category'], item['price'], item['discount'])
                         )

        self.conn.commit()
        return item