import json


def notice(product_id, product_name):
    with open('./not_notice.json', 'r') as f:
        data = json.load(f)
    try:
        if data[product_name]:
            return False
    except KeyError:
        data[product_name] = product_id
        with open('./not_notice.json', 'w') as f:
            json.dump(data, f)
        return True


if __name__ == "__main__":
    print(notice(123, 'asf'))