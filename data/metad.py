import sqlalchemy
from .db_session import SqlAlchemyBase


class Metad(SqlAlchemyBase):
    __tablename__ = 'metad'

    customer_num = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    seller_num = sqlalchemy.Column(sqlalchemy.Integer)
    product_num = sqlalchemy.Column(sqlalchemy.Integer)
    order_num = sqlalchemy.Column(sqlalchemy.Integer)
    profit_rate = sqlalchemy.Column(sqlalchemy.DECIMAL)
