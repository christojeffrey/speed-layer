FROM postgres
COPY ./postgres_initial.sql /docker-entrypoint-initdb.d/