import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager


class Seller(SqlAlchemyBase, UserMixin):
    __tablename__ = 'sellers'

    sellID = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    country = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, pas):
        self.password = generate_password_hash(pas)

    def check_password(self, pas):
        return check_password_hash(self.password, pas)