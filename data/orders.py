import sqlalchemy
from .db_session import SqlAlchemyBase
import datetime


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    orderID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    custID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.custID"))
    prodID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("product.prodID"))
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    cost_price = sqlalchemy.Column(sqlalchemy.DECIMAL)
    sell_price = sqlalchemy.Column(sqlalchemy.DECIMAL)
    status = sqlalchemy.Column(sqlalchemy.Integer)