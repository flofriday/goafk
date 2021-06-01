from datetime import datetime

from sqlalchemy.sql.schema import UniqueConstraint
from app.models import Job, User
import sqlalchemy
import databases
from secrets import token_urlsafe

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("platform", sqlalchemy.String),
    sqlalchemy.Column("user_name", sqlalchemy.String),
    sqlalchemy.Column("token", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    UniqueConstraint("platform", "user_name"),
    UniqueConstraint("token"),
)

jobs = sqlalchemy.Table(
    "jobs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("uuid", sqlalchemy.String),
    sqlalchemy.Column("command", sqlalchemy.String),
    sqlalchemy.Column("exit_code", sqlalchemy.Integer),
    sqlalchemy.Column("os", sqlalchemy.String),
    sqlalchemy.Column("prompt", sqlalchemy.String),
    sqlalchemy.Column("seconds", sqlalchemy.Float),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    UniqueConstraint("uuid"),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


async def insert_job(job: Job) -> int:
    query = jobs.insert().values(
        uuid=token_urlsafe(16),
        command=job.command,
        exit_code=job.exit_code,
        os=job.os,
        prompt=job.prompt,
        seconds=job.seconds,
        user_id=job.user_id,
        created_at=datetime.now(),
    )
    return await database.execute(query)


async def select_job_by_uuid(uuid: str) -> Job:
    query = jobs.select().where(jobs.c.uuid == uuid)
    return await database.fetch_one(query)


async def insert_user(user: User) -> int:
    query = users.insert().values(
        platform=user.platform,
        user_name=user.user_name,
        token=user.token,
        created_at=datetime.now(),
    )
    return await database.execute(query)


async def select_user_by_token(token: str) -> User:
    query = users.select().where(users.c.token == token)
    return await database.fetch_one(query)


async def select_user_by_username(platform: str, user_name: str) -> User:
    query = users.select().where(
        users.c.platform == platform and users.c.user_name == user_name
    )
    return await database.fetch_one(query)
