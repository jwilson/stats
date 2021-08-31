## start app
docker-compose up
docker exec stats_django_1 /bin/sh -c "/app/./init.sh"


## run
browse to http://localhost:8000