from flask import Blueprint, render_template


import models.products as product_db

category = Blueprint('category', __name__, template_folder="templates")


@category.route('/<categoryid>')
def category_home(categoryid):
    products = product_db.get_products(categoryid)
    return render_template('category.html', products=products, category=categoryid)
