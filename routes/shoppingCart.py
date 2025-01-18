from models.shoppingCart import Cart
from flask import Blueprint, request, jsonify
from models.product import Product
from extensions import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')
    quantity = data.get('quantity')

    if not user_id or not product_id or not quantity:
        return jsonify({"error": "Missing required fields"}), 400

    # 检查产品是否存在
    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product.stock < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity + quantity > product.stock:
            return jsonify({"error": f"Insufficient stock. Available stock: {product.stock - cart_item.quantity}"}), 400

        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    product.stock -= quantity

    db.session.commit()
    return jsonify({"message": "Product added to cart successfully"}), 201

# get cart
@cart_bp.route('/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 200

    cart_data = []
    total_price = 0

    for item in cart_items:
        product = Product.query.filter_by(id=item.product_id, is_deleted=False).first()
        if product:
            item_data = {
                "productId": product.id,
                "productName": product.name,
                "unitPrice": product.price,
                "quantity": item.quantity,
                "totalPrice": product.price * item.quantity
            }
            total_price += product.price * item.quantity
            cart_data.append(item_data)

    return jsonify({"cart": cart_data, "totalPrice": total_price}), 200

# update cart
@cart_bp.route('/update', methods=['PUT'])
def update_cart():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')
    quantity = data.get('quantity')

    if not user_id or not product_id or not quantity:
        return jsonify({"error": "Missing required fields"}), 400

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    product = Product.query.filter_by(id=product_id, is_deleted=False).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product.stock < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    cart_item.quantity = quantity
    db.session.commit()
    return jsonify({"message": "Cart updated successfully"}), 200

# delete from cart
@cart_bp.route('/delete', methods=['DELETE'])
def delete_from_cart():
    data = request.get_json()
    user_id = data.get('userId')
    product_id = data.get('productId')

    if not user_id or not product_id:
        return jsonify({"error": "Missing required fields"}), 400

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Product removed from cart successfully"}), 200

# clear cart
@cart_bp.route('/clear/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is already empty"}), 200

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    return jsonify({"message": "Cart cleared successfully"}), 200

@cart_bp.route('/select-items', methods=['POST'])
def select_cart_items():
    data = request.get_json()
    user_id = data.get('userId')
    selected_item_ids = data.get('cartItemIds')

    if not user_id or not selected_item_ids:
        return jsonify({"error": "Missing userId or cartItemIds"}), 400

    selected_items = Cart.query.filter(Cart.id.in_(selected_item_ids), Cart.user_id == user_id).all()
    if not selected_items:
        return jsonify({"error": "No valid items found in cart"}), 404

    items = [{
        "cartItemId": item.id,
        "productId": item.product_id,
        "quantity": item.quantity
    } for item in selected_items]

    return jsonify({"selectedItems": items}), 200
