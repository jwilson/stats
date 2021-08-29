## start
docker-compose -d up

## connect to app server
docker exec -it joshwilsonappserver bash

## initialize database
./manage.py migrate
./manage import_rushing_stats