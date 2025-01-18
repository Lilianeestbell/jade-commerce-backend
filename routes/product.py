from flask import Blueprint, request, jsonify
from models.product import Product
from extensions import db

product_bp = Blueprint('products', __name__)

@product_bp.route('/all', methods=['GET'])
def get_all_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)

    query = Product.query.filter(Product.is_deleted == False)
    if search:
        query = query.filter(Product.name.contains(search))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = [product.to_dict() for product in pagination.items]

    return jsonify({
        "products": products,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

@product_bp.route('/add', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data.get('name') or not data.get('price') or not data.get('stock'):
        return jsonify({"error": "Missing required fields: name, price, stock"}), 400

    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully", "product": new_product.to_dict()}), 201


@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']

    db.session.commit()
    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200

# delete product(logical delete)

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    product.is_deleted = True
    try:
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete product", "details": str(e)}), 500

