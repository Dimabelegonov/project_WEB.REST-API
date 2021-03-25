import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


from data.db_session import SqlAlchemyBase


class Department(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relation('User')

    def __repr__(self):
        s = ", ".join(["<Job>", str(self.job)])
        return s
