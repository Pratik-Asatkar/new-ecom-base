from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import get_jwt_identity, jwt_required


import models.products as product_db
import tools.image as image_db


product =  Blueprint('product', __name__, template_folder="templates")


@product.route('/<productid>')
def product_info(productid):
    product = product_db.get_product(productid)
    return render_template('product.html', product=product)


@product.route('/add', methods=['GET', 'POST'])
@jwt_required(locations='cookies')
def add_product():
    user = get_jwt_identity()

    if user['sub'] != 'admin':
        return "UNAUTHORIZED", "403"

    if request.method == 'GET':
        return render_template('add_product.html')
    elif request.method == 'POST':
        img_file = request.files['img']

        name = request.form.get('name')
        short_desc = request.form.get('short_desc')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        img = image_db.upload(img_file, ''.join(name.lower().split()), 'Products')['secure_url']

        product_data = {
            "_id": ''.join(name.lower().split()),
            "name": name,
            "short_desc": short_desc,
            "desc": description,
            "category": category,
            "price": int(price),
            "img": img
        }

        if product_db.add_product(product_data):
            return redirect('/')
        else:
            print("Something went wrong!")
            return redirect('/')
