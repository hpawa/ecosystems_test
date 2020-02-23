from flask import jsonify, request
from server import app
from .models import User, Group, Role, UserSchema, GroupSchema, RoleSchema, db


@app.route('/users', methods=['GET', 'POST'])
def all_users():
    response_object = {}
    try:
        if request.method == 'GET':
            users = User.query.filter()
            # filters
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
    except Exception as e:
        response_object['message'] = str(e)
    return jsonify(response_object)


@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def single_user(user_id):
    response_object = {}
    try:
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
    except Exception as e:
        response_object['message'] = str(e)
    return jsonify(response_object)


@app.route('/groups', methods=['GET', 'POST'])
def all_groups():
    response_object = {}
    try:
        if request.method == 'GET':
            groups = Group.query.filter()
            # filters
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
    except Exception as e:
        response_object['message'] = str(e)
    return jsonify(response_object)


@app.route('/groups/<group_id>', methods=['GET', 'PUT', 'DELETE'])
def single_group(group_id):
    response_object = {}
    try:
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
    except Exception as e:
        response_object['message'] = str(e)
    return jsonify(response_object)


@app.route('/roles', methods=['GET', 'POST'])
def all_roles():
    response_object = {}
    try:
        if request.method == 'GET':
            roles = Role.query.all()
            response_object['roles'] = RoleSchema(many=True).dump(roles)
        if request.method == 'POST':
            new_role = RoleSchema().load(request.get_json())
            db.session.add(new_role)
            db.session.commit()
            response_object['message'] = f'Role {new_role.name} created'
    except Exception as e:
        response_object['message'] = str(e)
    return jsonify(response_object)
