import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from models.base import Base
from models.user import User
from models.location import UserLocation
from models.session import UserSession
from models.profiles import Profile
from models.habits import Habits
from models.file import UserPhoto
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option(
    "sqlalchemy.url", "postgresql+asyncpg://admin:admin@localhost:5432/pet_db"
)
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    ignore_tables = [
        "spatial_ref_sys",
        "geography_columns",
        "geometry_columns",
        "raster_columns",
        "raster_overviews",
        "place",
        "place_lookup",
        "tiger",
        "tiger_data",
        "cousub",
        "county",
        "state",
        "countysub_lookup",
        "direction_lookup",
        "secondary_unit_lookup",
        "state_lookup",
        "street_type_lookup",
        "zip_lookup",
        "zip_state",
        "zip_state_loc",
    ]
    if name in ignore_tables:
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,  # Добавляем фильтр
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,  # Добавляем фильтр
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run async migrations."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
