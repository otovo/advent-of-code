DC_FILE   = docker/docker-compose.yaml
SVC_NAME  = otovo-adventofcode_pg15

run:
	docker compose --file ${DC_FILE} up -d

stop:
	docker compose --file ${DC_FILE} down

rm:
	docker compose --file ${DC_FILE} rm

solution-sql: run
	docker exec -it ${SVC_NAME} psql -U postgres -f /sql/day_$(day)/solution.sql | grep -i 'solution'