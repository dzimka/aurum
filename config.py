import os

from atlassian import Confluence
from dotenv import find_dotenv, load_dotenv
from langchain_ollama import OllamaEmbeddings, OllamaLLM


class AppConfig:
    llm_model: str
    llm_base_url: str
    data_path: str
    atlassian_url: str
    atlassian_username: str
    atlassian_token: str

    def __init__(self, **kwargs):
        self.llm_base_url = kwargs.get("llm_base_url", "http://localhost:11434")
        self.llm_model = kwargs.get("llm_model", "llama3.2:latest")
        self.data_path = kwargs["data_path"]
        self.atlassian_url = kwargs["atlassian_url"]
        self.atlassian_username = kwargs["atlassian_username"]
        self.atlassian_token = kwargs["atlassian_token"]

    def get_llm(self) -> OllamaLLM:
        """
        Returns an instance of the OllamaLLM class, which is used to interact with the LLM model.

        Returns:
            OllamaLLM: An instance of the OllamaLLM class.
        """
        return OllamaLLM(base_url=self.llm_base_url, model=self.llm_model)

    def get_llm_embed(self) -> OllamaEmbeddings:
        """
        Returns an instance of the OllamaEmbeddings class, which is used to interact with the LLM model
        for embedding purposes.

        Returns:
            OllamaEmbeddings: An instance of the OllamaEmbeddings class.
        """
        return OllamaEmbeddings(base_url=self.llm_base_url, model=self.llm_model)

    def get_confluence(self) -> Confluence:
        return Confluence(
            self.atlassian_url, username=self.atlassian_username, password=self.atlassian_token, cloud=True
        )


load_dotenv(find_dotenv(raise_error_if_not_found=True))

params = {
    "atlassian_url": os.environ.get("ATLASSIAN_CLOUD_URL"),
    "atlassian_username": os.environ.get("ATLASSIAN_USERNAME"),
    "atlassian_token": os.environ.get("ATLASSIAN_API_TOKEN"),
    "llm_base_url": os.environ.get("CONFLUETON_LLM_BASE_URL"),
    "llm_model": os.environ.get("CONFLUETON_LLM_MODEL"),
    "data_path": os.environ.get("CONFLUETON_DATA_PATH"),
}

# create a single instance of the app configuration
app_config = AppConfig(**params)
