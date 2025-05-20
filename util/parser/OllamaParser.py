import ollama
from .AbstractParser import AbstractParser

class OllamaParser(AbstractParser):
    """
    Parser implementation using the Ollama library.
    """

    def __init__(self, model_name: str = "gemma3:4b"):
        super().__init__(model_name)

    def parseArticle(self, article_content: str) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': self.prompt.format(article_content),
                    },
                ],
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error during Ollama API call: {e}")
            return "Error: Could not parse article using Ollama."
