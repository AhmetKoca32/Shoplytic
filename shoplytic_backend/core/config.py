from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Shoplytic"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # DeepSeek API
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-v4-flash"
    deepseek_base_url: str = "https://api.deepseek.com"

    # ChromaDB
    chroma_persist_directory: str = "./chroma_legal_db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
