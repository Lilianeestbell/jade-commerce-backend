from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, paid, shipped, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "totalPrice": self.total_price,
            "status": self.status,
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updatedAt": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
            "isDeletedOrder": self.is_deleted,
            "items": [item.to_dict() for item in self.order_items]
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "orderId": self.order_id,
            "productId": self.product_id,
            "quantity": self.quantity,
            "unitPrice": self.unit_price
        }
