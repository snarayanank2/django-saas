# Django SaaS Framework

This is a starter project for building a multi-tenant SaaS backend. Every SaaS product has a bunch of common
things and we've tried to incorporate all of them so you can focus on user experience side of things.

Warning: This is under active development and is not ready for production use. Needs a bunch
of documentation as well. Contact siva@fylehq.com if you're interested in this.


## Run the migrations

```
python manage.py migrate
```

## Start the development server

```
export SECRET_KEY=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_STORAGE_BUCKET_NAME=xxx
export AWS_ACCESS_KEY_ID=xxx
export AWS_S3_REGION_NAME=xxx

python manage.py runserver
```

## Run tests

```
python -m pytest
```

This produces a coverage report in cov_html folder. We try to hit 90% coverage in every file.