# Interop-rabilit-avanc-e


## Explication migration with alembic

Before running the migration, you need to  launch the docker-compose file with the following command:

```bash
docker compose up
```

Use the following command to generate a migration script:

```bash
docker compose exec back alembic revision --autogenerate -m "<your name of migration>"
```

Then, apply the migration with the following command:

```bash
docker compose exec back alembic upgrade head
```

if you want to downgrade the migration, use the following command:

```bash
docker compose exec back alembic downgrade -1
```





