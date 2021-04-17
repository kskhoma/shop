import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Product(SqlAlchemyBase, UserMixin):
    __tablename__ = 'product'

    prodID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    amount = sqlalchemy.Column(sqlalchemy.Integer)
    category = sqlalchemy.Column(sqlalchemy.String)
    cost_price = sqlalchemy.Column(sqlalchemy.DECIMAL)
    sell_price = sqlalchemy.Column(sqlalchemy.DECIMAL)
    about = sqlalchemy.Column(sqlalchemy.String)
    sellID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sellers.sellID"))