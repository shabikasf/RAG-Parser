from app.config import Settings

def get_generator(settings: Settings):
    """
    Factory function that returns the correct Generator implementation
    based on config.
    """

    generator_type = settings.generator_type.lower()

    if generator_type == "openai":
        from app.generation.openai_generation import OpenAIGenerator
        return OpenAIGenerator(base_url=settings.BASE_URL, api_key=settings.OPENAI_API_KEY)

    raise ValueError(f"Unsupported generator type: {generator_type}")