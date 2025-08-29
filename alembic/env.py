import asyncio
from logging.config import fileConfig

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context
from alembic.config import Config  # ✅ para tipagem correta

from workout_api.contrib.models import BaseModel
from workout_api.contrib.repository import models  # evita import * (boa prática)

# Alembic injeta config dinamicamente, mas tipamos para o editor entender
config: Config = context.config  # type: ignore[attr-defined]

# Configura logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dos modelos
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Executa migrações em modo offline (gera SQL sem precisar do banco)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(  # type: ignore[attr-defined]
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():  # type: ignore[attr-defined]
        context.run_migrations()  # type: ignore[attr-defined]


def do_run_migrations(connection: Connection) -> None:
    """Executa migrações síncronas."""
    context.configure(  # type: ignore[attr-defined]
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():  # type: ignore[attr-defined]
        context.run_migrations()  # type: ignore[attr-defined]


async def run_async_migrations() -> None:
    """Executa migrações usando engine assíncrono."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),  # type: ignore[attr-defined]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """Executa migrações em modo online (conectado ao banco)."""
    asyncio.run(run_async_migrations())


# Decide se roda offline ou online
if context.is_offline_mode():  # type: ignore[attr-defined]
    run_migrations_offline()
else:
    run_migrations_online()
