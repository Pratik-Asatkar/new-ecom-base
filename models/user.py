from models import user_dbs

import tools.utils as utils


user_collection = user_dbs['user']


def get_user_details(username):
    # return user information
    try:
        user_data = user_collection.find_one(
            {"_id": username}
        )

        return user_data
    except Exception as e:
        return False


def register(data):
    try:
        user_collection.insert_one(data)
        return True
    except Exception as e:
        print(f"Error/register: {e}")
        return False


def checkout_cart(username):
    try:
        user_data = user_collection.find_one({"_id": username})
        cart = user_data['cart']
        cart['time'] = utils.current_time()

        user_collection.update_one(
            {"_id": username},
            {"$push": {"previous_orders": cart}}
        )

        user_collection.update_one(
            {"_id": username},
            {"$set": {"cart": {"total": 0, "items": {}, "cartid": utils.get_cart_id()}}}
        )

        return True
    except Exception as e:
        print(f"Error/checkout_cart: {e}")
        return False


def add_to_cart(username, price, productid):
    try:
        user_cart = user_collection.find_one({"_id": username})['cart']

        if productid in user_cart['items'].keys():
            return add_quantity(username, productid, price)

        user_collection.update_one(
            {"_id": username},
            {"$set": {f"cart.items.{productid}": {"price": price, "quantity": 1}}}
        )

        user_collection.update_one(
            {"_id": username},
            {"$inc": {"cart.total": price}}
        )

        return True
    except Exception as e:
        print(f"Error/add_to_cart: {e}")
        return False


def add_quantity(username, productid, price):
    try:
        user_collection.update_one(
            {"_id": username},
            {"$inc": {f"cart.items.{productid}.quantity": 1}}
        )

        user_collection.update_one(
            {"_id": username},
            {"$inc": {"cart.total": price}}
        )

        return True
    except Exception as e:
        print(f"Error/add_quantity: {e}")
        return False


def reduce_quantity(username, productid, price):
    try:
        user_cart = get_user_details(username)['cart']

        if user_cart['items'][f'{productid}']['quantity'] <= 1:
            return remove_from_cart(username, price, productid, 1)

        user_collection.update_one(
            {"_id": username},
            {"$inc": {f"cart.items.{productid}.quantity": -1}}
        )

        user_collection.update_one(
            {"_id": username},
            {"$inc": {"cart.total": -price}}
        )

        return True
    except Exception as e:
        print(f"Error/add_quantity: {e}")
        return False


def remove_from_cart(username, price, productid, quantity):
    try:
        user_cart = get_user_details(username)['cart']
        product_detail = user_cart['items'][f'{productid}']

        user_collection.update_one(
            {"_id": username},
            {"$unset": {f"cart.items.{productid}": product_detail}}
        )

        user_collection.update_one(
            {"_id": username},
            {"$inc": {"cart.total": -(price * quantity)}}
        )

        return True
    except Exception as e:
        print(f"Error/remove_from_cart: {e}")
        return False
