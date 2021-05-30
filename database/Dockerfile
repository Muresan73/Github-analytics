FROM postgres

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD dbpass
ENV POSTGRES_DB postgres
COPY starting_point.sql /docker-entrypoint-initdb.d/
RUN chmod a+r /docker-entrypoint-initdb.d/*
