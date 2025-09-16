from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from flask import current_app
import os

config = context.config

# Загружаем конфиг логирования ТОЛЬКО если файл реально существует
if config.config_file_name and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# Метаданные моделей берём из Flask-Migrate
target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {},
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        url=current_app.config.get('SQLALCHEMY_DATABASE_URI'),
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
