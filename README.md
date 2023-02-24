# Complaint manager |مدیر شکایت  
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

## create super user COMMAND LINE

`export PYTHONPATH=./`
then
`python commands/create_super_user.py -f admin -l test -e a@a.com -p 1234534563 -i Gw324234234324 -pa 123445`
