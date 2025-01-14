from flask import Blueprint, request, jsonify
from models.product import Product
from extensions import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({"products": [product.to_dict() for product in products]}), 200
