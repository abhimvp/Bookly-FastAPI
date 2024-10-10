from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str  # to read our database url from .env file
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    # for every model we have a config class
    # SettingsConfigDict is a class that allows us to configure/ point to where our .env file is located
    # extra = ignore means that any extra variables in the .env file that are not defined in our model will be ignored


Config = Settings()  # type: ignore
print(f"DATABASE_URL: {Config.DATABASE_URL}")
