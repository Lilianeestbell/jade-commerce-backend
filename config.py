class Config:
    SECRET_KEY = '98b6f635464ba8a85f0585d136a7b4b75635d6ed49237352c1fa4d5c1b2a0f94'  # 应用的通用密钥
    JWT_SECRET_KEY = '75ca5abe26d94f859f1ea80e1b043918d6843ef779ebe19d75637812f9b70d96e'  # JWT 的密钥
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:free1997@localhost/jade_commerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False