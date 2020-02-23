import os
import unittest
from server import app
from server.models import User, Group, Role, UserSchema, GroupSchema, RoleSchema, db
import json

class TestCase(unittest.TestCase):
    def setUp(self):        
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        self.app = app.test_client()
        db.create_all()
        db.session.add(User(username='Oleg', password='qwerty'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db'))

    def test_roles_list(self):
        response_object = {}
        roles = Role.query.all()
        response = self.app.get('/roles')        
        response_object['roles'] = RoleSchema(many=True).dump(roles)        
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), response_object)

    def test_get_user(self):
        response = self.app.get('/users/1')        
        user = User.query.filter_by(id='1')        
        self.assertDictEqual(response.get_json(), UserSchema().dump(user.first()))        

    def test_create_user(self):
        req_data = {
            'username': 'Ivan',
            'password': '12345'
        }        
        response = self.app.post('/users', data=json.dumps(req_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(req_data['username'], User.query.order_by(User.id.desc()).first().username)
        self.assertEqual(req_data['password'], User.query.order_by(User.id.desc()).first().password)


if __name__ == '__main__':
    unittest.main()