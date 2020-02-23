import os
import unittest
from server import app
from server.models import User, Group, Role, UserSchema, GroupSchema, RoleSchema, db

class TestCase(unittest.TestCase):
    def setUp(self):        
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db'))

    def test_roles_list(self):
        response = self.app.get('/roles')        
        self.assertEqual(response.status_code, 200)

        #assert Role.query.all() == 


if __name__ == '__main__':
    unittest.main()