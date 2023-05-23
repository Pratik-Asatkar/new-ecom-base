from models import product_dbs

product_collection = product_dbs['products']


def get_products(category):
    try:
        products = product_collection.find(
            {"category": category}
        )

        return products
    except Exception as e:
        print(f"Error/get_products: {e}")
        return False


def get_product(product_id):
    try:
        product_info = product_collection.find_one(
            {"_id": product_id}
        )

        return product_info
    except Exception as e:
        print("Error/get_product: {e}")
        return False


def add_product(product_data):
    try:
        product_collection.insert_one(product_data)
        return True
    except Exception as e:
        print(f"Error/add_product: {e}")
        return False



