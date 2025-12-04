from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os
import sys

# ---------------------------------------------------------
# [수정 1] 현재 프로젝트 경로를 파이썬 경로에 추가
# (이게 없으면 models.py를 못 찾습니다)
sys.path.append(os.getcwd())

# [수정 2] 우리가 만든 모델과 데이터베이스 설정을 가져옵니다.
from database import Base
from models import Question
# ---------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------
# [수정 3] None을 Base.metadata로 변경
# (이게 있어야 테이블을 자동으로 감지합니다)
target_metadata = Base.metadata
# ---------------------------------------------------------

def run_migrations_offline() -> None:
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