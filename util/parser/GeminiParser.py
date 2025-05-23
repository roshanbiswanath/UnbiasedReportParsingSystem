from google import genai
import os
from .AbstractParser import AbstractParser

class GeminiParser(AbstractParser):
    """
    Parser implementation using the Gemini API.
    """
    def __init__(self, model_name: str = "gemma-3n-e4b-it"):
        super().__init__(model_name)
        # Configure the Gemini API key from environment variable
        # Ensure you have GOOGLE_API_KEY set in your environment
        try:
            self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        except KeyError:
            raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")
        except Exception as e:
            raise RuntimeError(f"Failed to configure Gemini API: {e}")

    def parseArticle(self, article_content: str) -> str:
        """
        Parses the given article content using the Gemini model.

        Args:
            article_content: The raw text content of the news article.

        Returns:
            The parsed content of the article as a string.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.prompt.format(article_content),
            )
            return response.text
        except Exception as e:
            # Handle potential errors during API call
            print(f"Error during Gemini API call: {e}")
            return None
