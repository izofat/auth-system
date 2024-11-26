import os

import pydash
import toml

_script_dir = os.path.dirname(__file__)

config_path = os.path.join(_script_dir, "config.toml")

assert os.path.exists(
    config_path
), "config.toml not found. Use make config to create one."

config = toml.load(config_path)

assert config, "config.toml is empty, please fill it with the necessary data"

DEBUG = pydash.get(config, "debug", True)

ENV = "dev" if DEBUG else "prod"

API_PORT = pydash.get(config, f"api.{ENV}.port")

assert API_PORT, "API port not found in config.toml"

JWT_SECRET = pydash.get(config, "jwt_secret")

assert JWT_SECRET, "JWT secret not found in config.toml"


class MySqlConfig:
    HOST = pydash.get(config, f"db.{ENV}.host")
    PORT = pydash.get(config, f"db.{ENV}.port")
    USER = pydash.get(config, f"db.{ENV}.username")
    PASSWORD = pydash.get(config, f"db.{ENV}.password")
    DATABASE = pydash.get(config, f"db.{ENV}.database")
    POOL_SIZE = pydash.get(config, f"db.{ENV}.pool_size", 5)
    POOL_NAME = pydash.get(config, f"db.{ENV}.pool_name", "pool")


assert MySqlConfig.HOST, "Database host not found in config.toml"
assert MySqlConfig.PORT, "Database port not found in config.toml"
assert MySqlConfig.USER, "Database user not found in config.toml"
assert MySqlConfig.PASSWORD, "Database password not found in config.toml"
assert MySqlConfig.DATABASE, "Database name not found in config.toml"
