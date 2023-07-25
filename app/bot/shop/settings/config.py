from dataclasses import dataclass

from environs import Env


@dataclass
class RedisConfig:
    rd_host: str
    rd_port: str
    rd_password: str


@dataclass
class TgBot:
    token: str
    canal_id: str
    group_id: str


@dataclass
class Config:
    tg_bot: TgBot
    redis: RedisConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            canal_id=env('CANAL_ID'),
            group_id=env('GROUP_ID')
        ),
        redis=RedisConfig(
            rd_host=env('REDIS_HOST'),
            rd_password=env('REDIS_PASSWORD'),
            rd_port=env('REDIS_PORT')
        ),
    )


config = load_config()
