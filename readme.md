# SGA API with FastAPI + SqlAlchemy + Alembic

# install dependencies
  - pip install "fastapi[standard]"
  - pip install sqlalchemy
  - pip install alembic
  - pip install pyjwt
  - pip install "passlib[bcrypt]"
  
# alembic
  - alembic revision --autogenerate -m "Initial migration"
  - alembic revision -m "xxxx"
  - alembic upgrade head

# run in dev
  - fastapi dev sga/main.py
  - uvicorn sga.main:app --host 0.0.0.0 --port 9090 --reload