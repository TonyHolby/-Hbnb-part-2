from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Ajouter le chemin du projet au sys.path pour que les modules puissent être trouvés
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# il s'agit de l'objet Alembic Config, qui fournit
# l'accès aux valeurs du fichier .ini utilisé.
config = context.config

# Interpréter le fichier de configuration pour la journalisation Python.
# Cette ligne met en place les loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ajoutez l'objet MetaData de votre modèle ici
# pour le support 'autogénérer
# from myapp import mymodel
from src.models import Base
target_metadata = Base.metadata

# autres valeurs de la configuration, définies par les besoins de env.py,
# peuvent être acquises :
# mon_option_importante = config.get_main_option("mon_option_importante")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
