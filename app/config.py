from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    vector_store_type: str = "chroma"  
    embedder_type: str = "sentence_transformer"
    generator_type: str = "openai"

    OPENAI_API_KEY: str | None = None
    BASE_URL: str | None = None

    pinecone_api_key: str | None = None
    pinecone_index: str | None = None

    class Config:
        env_file = ".env"