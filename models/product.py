from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "productName": self.name,
            "productDescription": self.description,
            "productPrice": self.price,
            "productStock": self.stock,
            "is_deleted_product": self.is_deleted
        }

