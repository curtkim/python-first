python my_app.py
db:
  name: mysql
server:
  name: apache
  port: 80

python my_app.py +experiment=nglite
db:
  name: sqlite
server:
  name: apache
  port: 8080
