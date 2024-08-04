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
