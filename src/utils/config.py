import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Any, Dict
import logging


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize configuration from environment variables.
        
        Args:
            env_file (str): Path to the .env file
        """
        # Load environment variables
        env_path = Path(env_file)
        load_dotenv(dotenv_path=env_path)
        
        # Application settings
        self.app_name = self._get_env("APP_NAME", "Digital Content Generator")
        self.environment = self._get_env("ENVIRONMENT", "development").lower()
        self.debug = self._get_env("DEBUG", "True").lower() == "true"
        self.port = int(self._get_env("PORT", "8501"))
        
        # Security
        self.secret_key = self._get_env("SECRET_KEY", required=True)
        self.allowed_hosts = self._get_env("ALLOWED_HOSTS", "localhost").split(",")
        
        # LLM (Language Model) settings
        self.llm_provider = self._get_env("LLM_PROVIDER", "ollama").lower()  # Nuevo: Proveedor de LLM
        self.openai_api_key = self._get_env("OPENAI_API_KEY", required=True)
        self.ollama_host = self._get_env("OLLAMA_HOST", "http://localhost:11434")
        
        # Image generation
        self.stable_diffusion_host = self._get_env("STABLE_DIFFUSION_HOST")
        self.unsplash_api_key = self._get_env("UNSPLASH_API_KEY")
        
        # Database settings
        self.chroma_persist_directory = self._get_env("CHROMA_PERSIST_DIRECTORY", "./data/chroma")
        self.neo4j_uri = self._get_env("NEO4J_URI")
        self.neo4j_user = self._get_env("NEO4J_USER")
        self.neo4j_password = self._get_env("NEO4J_PASSWORD")
        
        # External APIs
        self.arxiv_email = self._get_env("ARXIV_EMAIL")
        self.financial_api_key = self._get_env("FINANCIAL_API_KEY")
        self.news_api_key = self._get_env("NEWS_API_KEY")
        
        # Monitoring
        self.langsmith_api_key = self._get_env("LANGSMITH_API_KEY")
        self.langchain_project = self._get_env("LANGCHAIN_PROJECT")
        
        # Paths
        self.data_dir = Path(self._get_env("DATA_DIR", "./data"))
        self.temp_dir = Path(self._get_env("TEMP_DIR", "./temp"))
        self.log_dir = Path(self._get_env("LOG_DIR", "./logs"))
        
        # Create necessary directories
        self._create_directories()
        
        # Setup logging
        self._setup_logging()
    
    def _get_env(self, key: str, default: Any = None, required: bool = False) -> str:
        """Get environment variable with error handling.
        
        Args:
            key (str): Environment variable key
            default (Any): Default value if not found
            required (bool): Whether the variable is required
            
        Returns:
            str: Environment variable value
            
        Raises:
            ValueError: If required variable is not found
        """
        value = os.getenv(key, default)
        if required and value is None:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value
    
    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [self.data_dir, self.temp_dir, self.log_dir]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_level = getattr(logging, self._get_env("LOG_LEVEL", "INFO").upper())
        log_format = self._get_env("LOG_FORMAT",
                                 "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(self.log_dir / "app.log")
            ]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for easy access.
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
    def validate(self) -> bool:
        """Validate the configuration.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        # Add validation logic here
        required_keys = [
            "secret_key",
            "openai_api_key" if self.llm_provider == "openai" else None,
            "ollama_host" if self.llm_provider == "ollama" else None,
        ]
        
        missing_keys = [
            key for key in required_keys
            if key is not None and not getattr(self, key, None)
        ]
        
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")
        
        return True


# Usage example
if __name__ == "__main__":
    config = Config()
    try:
        config.validate()
        print("Configuration loaded successfully")
        print(config.to_dict())
    except ValueError as e:
        print(f"Configuration error: {e}")
