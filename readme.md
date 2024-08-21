# SGA API with FastAPI + SqlAlchemy + Alembic

# install dependencies
  - pip install "fastapi[standard]"
  - pip install sqlalchemy
  - pip install alembic
  - pip install pyjwt
  - pip install "passlib[bcrypt]"
  - pip install pydantic_settings
  - pip install aiosqlite
  - pip install pytz
  - pip install asyncpg
  - pip install psycopg2-binary 
  
  - or pip install -r requirements.txt

# alembic
  - alembic revision --autogenerate -m "Initial migration"
  - alembic revision -m "xxxx"
  - alembic upgrade head

# run in dev
  - fastapi dev sga/main.py
  - uvicorn sga.main:app --host 0.0.0.0 --port 9090 --reload

# setup database in docker
    docker compose up -d

# dev setup
    * Setup Python environment
        - pyenv virtualenv 3.12.4 v_sga
        - pyenv activate v_sga
        - pip install -r requirements.txt

    * start database in docker container
        - install Docker Ranch Desktop
        - docker compose up -d

    * run migration:
        - alembic upgrade head

    * start the server in PyCharm
        - Script: path to uvicorn
        - Script parameters: sga.main:app --host 0.0.0.0 --port 9090 --reload
        - Run

# generate self signed key for nginx
    openssl req -x509 -nodes -days 365 -subj "/C=US/ST=Oklahoma/O=SGN/CN=sharegrow.local" -newkey rsa:2048 -keyout ssl.key -out ssl.crt;
    - add the ssl.crt into the system certification
      Keychain Access -> System (left side menu) -> Certificates -> import (may need admin permission) -> set always trust by right clicking "get info"

# register host in mac
    /etc/hosts
    127.0.0.1       sharegrow.local

# access to ui
    https://sharegrow.local/

# Testing on aws ec2: 
    https://ec2-3-144-113-209.us-east-2.compute.amazonaws.com/

# legacy Website:
  https://www.sharegrow2.org, https://www.sharegrow.org
