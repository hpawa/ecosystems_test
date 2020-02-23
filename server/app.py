from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import INCLUDE, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root3832@localhost:5432/eco_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

CORS(app)


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
    users = fields.Nested(lambda: UserSchema(many=True, only=('id', 'username')))
    groups = fields.Nested(lambda: GroupSchema(many=True, only=('id', 'name')))
    class Meta:
        model = Role


class GroupSchema(ma.ModelSchema):
    role = fields.Nested(RoleSchema(only=('id', 'name')))
    users = fields.Nested(lambda: UserSchema(many=True, only=('id', 'username', 'role')))

    class Meta:
        model = Group
        unknown = INCLUDE


class UserSchema(ma.ModelSchema):
    group = fields.Nested(GroupSchema(only=('id', 'name')))
    role = fields.Nested(RoleSchema(only=('id', 'name')))

    class Meta:
        model = User
        unknown = INCLUDE


@app.route('/users', methods=['GET', 'POST'])
def all_users():
    response_object = {}
    if request.method == 'GET':
        users = User.query.filter()
        #filters
        username = request.args.get('username', None)
        group = request.args.get('group', None)
        role = request.args.get('role', None)
        order_by = request.args.get('order_by', None)
        if username:
            users = users.filter(User.username.startswith(username))
        if group:
            users = users.filter_by(group_id=group)
        if role:
            users = users.filter_by(role_id=role)
        if order_by:
            users = users.order_by(order_by)
        response_object['users'] = UserSchema(many=True).dump(users.all())
    if request.method == 'POST':
        new_user = UserSchema().load(request.get_json())
        db.session.add(new_user)
        db.session.commit()
        response_object['message'] = f'User {new_user.username} created'
    return jsonify(response_object)


@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def single_user(user_id):
    response_object = {}
    user = User.query.filter_by(id=user_id)
    if request.method == 'GET':
        response_object = UserSchema().dump(user.first())
    if request.method == 'PUT':
        post_data = request.get_json()
        user.update(post_data)
        db.session.commit()
        response_object['message'] = f'User {user.first().username} updated'
    if request.method == 'DELETE':
        username = user.first().username
        user.delete()
        db.session.commit()
        response_object['message'] = f'User {username} delete'
    return jsonify(response_object)


@app.route('/groups', methods=['GET', 'POST'])
def all_groups():
    response_object = {}
    if request.method == 'GET':
        groups = Group.query.filter()
        #filters
        name = request.args.get('name', None)        
        role = request.args.get('role', None)
        order_by = request.args.get('order_by', None)
        if name:
            groups = groups.filter(Group.name.startswith(name))        
        if role:
            groups = groups.filter_by(role_id=role)
        if order_by:
            groups = groups.order_by(order_by)
        response_object['groups'] = GroupSchema(many=True).dump(groups)
    if request.method == 'POST':
        new_group = GroupSchema().load(request.get_json())
        db.session.add(new_group)
        db.session.commit()
        response_object['message'] = 'Group created'
    return jsonify(response_object)


@app.route('/groups/<group_id>', methods=['GET', 'PUT', 'DELETE'])
def single_group(group_id):
    response_object = {}
    group = Group.query.filter_by(id=group_id)
    if request.method == 'GET':
        response_object = GroupSchema().dump(group.first())
    if request.method == 'PUT':
        post_data = request.get_json()
        group.update(post_data)
        db.session.commit()
        response_object['message'] = f'Group {group.first().name} updated'
    if request.method == 'DELETE':
        group_name = group.first().name
        group.delete()
        db.session.commit()
        response_object['message'] = f'Group {group_name} delete'
    return jsonify(response_object)

@app.route('/roles', methods=['GET', 'POST'])
def all_roles():
    response_object = {}
    if request.method == 'GET':
        roles = Role.query.all()
        response_object['roles'] = RoleSchema(many=True).dump(roles)
    if request.method == 'POST':
        new_role = RoleSchema().load(request.get_json())
        db.session.add(new_role)
        db.session.commit()
        response_object['message'] = f'Role {new_role.name} created'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
