from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity


import models.user as user_db
import models.products as product_db

cart = Blueprint('cart', __name__, template_folder="templates")


@cart.route('/')
@jwt_required(locations='cookies')
def view_cart():
    user = get_jwt_identity()

    user_data = user_db.get_user_details(user['sub'])
    user_cart = user_data['cart']

    cart = []

    for item in dict(user_cart['items']).keys():
        cart.append(dict(product_db.get_product(item)))
        cart[-1]['quantity'] = dict(user_cart)['items'][f'{item}']['quantity']

    return render_template('cart.html', cart=cart, total=user_cart['total'])


@cart.route('/checkout')
@jwt_required(locations='cookies')
def checkout_cart():
    user = get_jwt_identity()

    if (user_db.checkout_cart(user['sub'])):
        return redirect('/profile')
    else:
        return redirect('/')


@cart.route('/add/<productid>')
@jwt_required(locations='cookies')
def add_product(productid):
    user = get_jwt_identity()

    product_info = product_db.get_product(productid)

    if (user_db.add_to_cart(user['sub'], product_info['price'], productid)):
        return redirect(url_for('cart.view_cart'))
    else:
        return redirect('/')


@cart.route('/remove/<productid>')
@jwt_required(locations='cookies')
def remove_product(productid):
    user = get_jwt_identity()

    user_cart = user_db.get_user_details(user['sub'])['cart']
    quantity = dict(user_cart)['items'][f'{productid}']['quantity']
    product_info = product_db.get_product(productid)

    if (user_db.remove_from_cart(user['sub'], product_info['price'], productid, quantity)):
        return redirect(url_for('cart.view_cart'))
    else:
        return redirect('/')


@cart.route('/addquantity/<productid>')
@jwt_required(locations='cookies')
def add_quantity(productid):
    user = get_jwt_identity()

    product_info = product_db.get_product(productid)
    if (user_db.add_quantity(user['sub'], productid, product_info['price'])):
        return redirect(url_for('cart.view_cart'))
    else:
        return redirect('/')


@cart.route('/reducequantity/<productid>')
@jwt_required(locations='cookies')
def remove_quantity(productid):
    user = get_jwt_identity()

    product_info = product_db.get_product(productid)
    if (user_db.reduce_quantity(user['sub'], productid, product_info['price'])):
        return redirect(url_for('cart.view_cart'))
    else:
        return redirect('/')
