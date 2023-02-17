# store
## an fastapi store with s3 storage

## install requirements
`
pip install -r requirements.txt
`
## Run postgresql
`
docker-compose up --build
`
#
## makemigrations and migrate

`alembic init migrations`
### then add DATABASE URL in **alembic.ini** file => **sqlalchemy.url =DATABASE_URL**

### configure env file in migration **target_metadata**
#
`alembic revision --autogenerate -m "intial tables"`
#
`alembic upgrade head`