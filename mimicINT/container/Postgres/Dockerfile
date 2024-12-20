FROM postgres:9.6.19

COPY ./container/Postgres/postgres.conf /etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]
CMD ["-c", "listen_addresses=*"]

COPY ./container/Postgres/mimicINT_db.sql /etc/postgresql/mimicINT_db.sql



