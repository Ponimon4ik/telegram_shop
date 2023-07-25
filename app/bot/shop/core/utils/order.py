from pathlib import Path

import openpyxl

EXEL_PATH = Path('order')
EXEL_PATH.mkdir(exist_ok=True)


def get_description_order(order: dict):
    city = order.get('city', ())
    address = order.get('address', '')
    name = order.get('name', '')
    phone = order.get('phone', '')
    return city[1], address, name, phone


def create_exel(file_name, product_data, order_data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(order_data)
    for row_data in product_data:
        sheet.append(row_data)
    file_name = file_name + '.xlsx'
    file_name = EXEL_PATH / file_name
    workbook.save(file_name)
