import sqlalchemy
from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    __tablename__ = 'Cart'

    forpk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    custID = sqlalchemy.Column(sqlalchemy.Integer)
    prodID = sqlalchemy.Column(sqlalchemy.Integer)
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
