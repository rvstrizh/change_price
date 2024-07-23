import pymysql
import json
from config import host, user, password, db_name
import time

category = 358, 17
connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)


def read_sql():
    connection.ping()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nsrf_vm_product.product_id, nsrf_vm_product.product_in_stock, nsrf_vm_product_category_xref.category_id as category, product_sku, url_SMM, local_delivery_cost as price_dbs,  rating, product_order_levels, min_price_smm, max_price_SMM, sensitivity, step, activate_bot
            FROM nsrf_vm_product LEFT JOIN nsrf_vm_product_type_103 
            ON nsrf_vm_product.product_id = nsrf_vm_product_type_103.product_id
            LEFT JOIN nsrf_vm_product_category_xref
            ON  nsrf_vm_product.product_id = nsrf_vm_product_category_xref.product_id
            WHERE nsrf_vm_product_type_103.url_SMM LIKE '%megamarket%' AND nsrf_vm_product.product_in_stock > 0
            AND activate_bot = 'да'
        """)
        with open('bd_sql.json', 'w') as f:
            json.dump(cursor.fetchall(), f, indent=4)
            # connection.close()
#WHERE nsrf_vm_product.product_in_stock > 0 AND nsrf_vm_product_category_xref.category_id IN (194, 219, 299, 300, 323, 206, 257, 204, 319, 167)


def write_sql(new_price, product_id):
    connection.ping()
    with connection.cursor() as cursor:
        sql_query = """
            UPDATE nsrf_vm_product
            SET product_order_levels = %s
            WHERE product_id = %s
        """
        new_price = f'0,{new_price}'
        cursor.execute(sql_query, (new_price, product_id))
        connection.commit()
        connection.close()


if __name__ == "__main__":
    # new_price = '0,10770'
    # product_id = 15056
    # write_sql(new_price, product_id)

    read_sql()


