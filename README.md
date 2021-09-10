Installation and running this solution

## start app
docker-compose up -d\
docker exec stats_django_1 /bin/sh -c "/app/./init.sh"


## run
browse to http://localhost:8000


## post coding session
- the reason i don't think to use f strings is that the existing codebase is py2