from flask import Blueprint, request, jsonify
from models.order import Order, OrderItem
from models.product import Product
from models.user import User
from extensions import db

order_bp = Blueprint('orders', __name__)
# get all orders
@order_bp.route('/all', methods=['GET'])
def get_all_orders():
    page = request.args.get('page', 1, type=int)  
    per_page = request.args.get('per_page', 10, type=int)  
    user_id = request.args.get('userId', type=int)

    query = Order.query.filter_by(is_deleted=False)

    if user_id:
        query = query.filter_by(user_id=user_id)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    orders = [order.to_dict() for order in pagination.items]

    return jsonify({
        "orders": orders,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }), 200

# create order
@order_bp.route('/create', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('userId')  # 注意这里使用 userId
    if not user_id:
        return jsonify({"error": "Missing userId"}), 400

    items = data.get('items')  # List of {"productId": int, "quantity": int}
    if not items or not isinstance(items, list):
        return jsonify({"error": "Invalid items format"}), 400

    total_price = 0
    order_items = []

    for item in items:
        product = Product.query.filter_by(id=item['productId'], is_deleted=False).first()
        if not product:
            return jsonify({"error": f"Product with ID {item['productId']} not found"}), 404

        quantity = item['quantity']
        if quantity <= 0:
            return jsonify({"error": "Quantity must be greater than 0"}), 400

        if quantity > product.stock:
            return jsonify({"error": f"Insufficient stock for product ID {item['productId']}"}), 400

        total_price += product.price * quantity
        order_items.append(OrderItem(product_id=product.id, quantity=quantity, unit_price=product.price))

        product.stock -= quantity

    new_order = Order(user_id=user_id, total_price=total_price)
    db.session.add(new_order)
    db.session.flush()

    for order_item in order_items:
        order_item.order_id = new_order.id
        db.session.add(order_item)

    db.session.commit()

    return jsonify({"message": "Order created successfully", "order": new_order.to_dict()}), 201

# get order
@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.filter_by(id=order_id, is_deleted=False).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order.to_dict()), 200

# update order status
@order_bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    print(f"Request received for order_id: {order_id}")
    print(f"Request data: {request.get_json()}")

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['pending', 'paid', 'shipped', 'completed']:
        return jsonify({"error": "Invalid status"}), 400

    order = Order.query.filter_by(id=order_id, is_deleted=False).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.status = new_status
    db.session.commit()

    return jsonify({"message": "Order status updated successfully", "order": order.to_dict()}), 200

# delete order ; logical delete
@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.filter_by(id=order_id, is_deleted=False).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.is_deleted = True
    db.session.commit()

    return jsonify({"message": "Order deleted successfully", "order": order.to_dict()}), 200
