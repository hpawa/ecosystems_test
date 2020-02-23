from datetime import datetime
from marshmallow import INCLUDE, fields
from server import db, ma

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    dtcreate = db.Column(db.DateTime, default=datetime.now)
    groups = db.relationship('Group')
    users = db.relationship('User')


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    role = db.relationship('Role')
    users = db.relationship('User')
    dtcreate = db.Column(db.DateTime, default=datetime.now)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship('Group')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    role = db.relationship('Role')
    dtcreate = db.Column(db.DateTime, default=datetime.now)


class RoleSchema(ma.ModelSchema):
    users = fields.Nested(lambda: UserSchema(
        many=True, only=('id', 'username')))
    groups = fields.Nested(lambda: GroupSchema(many=True, only=('id', 'name')))

    class Meta:
        model = Role


class GroupSchema(ma.ModelSchema):
    role = fields.Nested(RoleSchema(only=('id', 'name')))
    users = fields.Nested(lambda: UserSchema(
        many=True, only=('id', 'username', 'role')))

    class Meta:
        model = Group
        unknown = INCLUDE


class UserSchema(ma.ModelSchema):
    group = fields.Nested(GroupSchema(only=('id', 'name')))
    role = fields.Nested(RoleSchema(only=('id', 'name')))

    class Meta:
        model = User
        unknown = INCLUDE