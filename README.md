## Config setup
edit SQLALCHEMY_DATABASE_URI on server/config.py
## Server setup
```
pip install -r server/requirements.txt
py server/manage.py init_db
py server/manage.py runserver
```
## Client setup
```
cd client
npm install
npm run serve
```
