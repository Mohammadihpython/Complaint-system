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

# AWS tools 
## i use localstack that run aws services locally and free

1. Install LocalStack using the instructions provided in the LocalStack documentation.

2. Create a bucket using the AWS CLI:
### first you need install aws cli on your machine

`aws --endpoint-url=http://localhost:4572 s3 mb s3://my-bucket`

##3. Get the access key and secret key for your bucket by running the following command: 

aws --endpoint-url=http://localhost:4572 configure get aws_access_key_id aws_secret_access_key
## if your keys are None you can set with `aws configure`