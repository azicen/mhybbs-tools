import toml
from pydantic import BaseModel


class Act(BaseModel):
    genshin_impact: bool
    honkai_star_rail: bool


class Job(BaseModel):
    trigger_time: str


class Config(BaseModel):
    cookie: str
    act: Act
    job: Job

    @staticmethod
    def load(path) -> "Config":
        with open(path, "r") as f:
            config_data = toml.load(f)
            return Config(**config_data)
