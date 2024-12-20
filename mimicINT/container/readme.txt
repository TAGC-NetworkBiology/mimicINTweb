
This docker-compose file allows to set up the appropriate
environment to use Django.

It includes:
- A Python environment with Django (Python 3)
- A PostgreSQL server (PostgreSQL 9.6.19)
- Adminer (Adminer 4.7.7)


# ===========================================
# Update the config files
# ===========================================

The following config files may eventually be updated and
have to be present prior to set up the services.

PostgreSQL: Postgres/postgres.conf


# ===========================================
# Start the web and PostgreSQL servers
# ===========================================

cd ~/workspace/tagc-mimicintweb/mimicINT/container
docker-compose up -d

NB: You may eventually update the following lines:
- Line 22 to change "/data/choteau/data/tagc-mimicintweb/postgresql" 
  by the path of the directory that aims to contain the PostgreSQL databases.
- Line 39 to change "/data/choteau/data/tagc-mimicintweb/jobs:/jobs"
  by the path of the directory that aims to contain the files the jobs created
  by the web app. 


# ===========================================
# Set connection to the PostgreSQL server
# ===========================================

# Change connection to DB settings
# Edit the code/mimicINT/settings.py file to set up the database


# ===========================================
# Make migrations on Django
# ===========================================

docker-compose exec web python /code/manage.py makemigrations; docker-compose exec web python /code/manage.py migrate


# ===========================================
# Rebuild all the dockers
# =========================================== 

To rebuild all the containers, use:
docker stop tagc-mimicintweb-web tagc-mimicintweb-db tagc-mimicintweb-adminer
docker rm tagc-mimicintweb-web tagc-mimicintweb-db tagc-mimicintweb-adminer
docker-compose up -d
