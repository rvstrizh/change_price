import pymysql
from config import host, user, password, db_name
import time

from main import new_price

category = 358, 17
connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT nsrf_vm_product.product_id, nsrf_vm_product.product_in_stock, nsrf_vm_product_category_xref.category_id as category, product_sku, url_SMM, local_delivery_cost as price_dbs,  rating, product_order_levels, min_price_smm, max_price_SMM, sensitivity, step
        FROM nsrf_vm_product LEFT JOIN nsrf_vm_product_type_103 
        ON nsrf_vm_product.product_id = nsrf_vm_product_type_103.product_id
        LEFT JOIN nsrf_vm_product_category_xref
        ON  nsrf_vm_product.product_id = nsrf_vm_product_category_xref.product_id
        WHERE nsrf_vm_product.product_in_stock > 0 AND nsrf_vm_product_category_xref.category_id IN (323)
        AND nsrf_vm_product.product_id IN (15010)
    """)
    rows = cursor.fetchall()
    print(rows)
    # for row in rows:
    #     product_id = row['product_id']
    #     # Пример SQL запроса для обновления значения столбца rating для строки с указанным product_id
    #     sql_query_update = f"""
    #             UPDATE nsrf_vm_product
    #             SET product_order_levels = '0,124'
    #             WHERE product_id = {product_id}
    #         """
    #     # Выполнение запроса UPDATE
    #     cursor.execute(sql_query_update)
    #     connection.commit()  # Подтверждение изменений в базе данных
    for row in rows:
        print(row)
        old_value = row
        url_smm = row['url_SMM']
        min_price = row['min_price_smm']
        max_price = row['max_price_SMM']
        sensitivity = row['sensitivity']
        step = row['step']
        stock = row['product_in_stock']
        new_price = new_price(url_smm, min_price, max_price, sensitivity, step, stock)
        print(new_price)

