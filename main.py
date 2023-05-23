from datetime import timedelta
from flask import Flask, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

import models.products as product_db
import models.user as user_db

import config.secrets as secrets

from controllers.products_controller import product
from controllers.auth_controller import auth
from controllers.cart_controller import cart
from controllers.category_controller import category


app = Flask(__name__)
app.secret_key = secrets.APP_SECRET
app.config['JWT_SECRET_KEY'] = secrets.JWT_SECRET
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)


jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for('auth.login'))


@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return redirect(url_for('auth.login'))


@app.route('/')
def home():
    featured = product_db.get_products("featured")
    return render_template('home.html', featured=featured)


@app.route('/profile')
@jwt_required(locations='cookies')
def profile():
    user = get_jwt_identity()

    user_data = user_db.get_user_details(user['sub'])
    return render_template('profile.html', user=user_data)


# Register Blueprints
app.register_blueprint(product, url_prefix='/product')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(cart, url_prefix='/cart')
app.register_blueprint(category, url_prefix='/category')


if __name__ == "__main__":
    app.run(debug=True)
