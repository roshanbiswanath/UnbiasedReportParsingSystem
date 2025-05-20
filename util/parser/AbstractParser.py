from abc import ABC, abstractmethod

class AbstractParser(ABC):
    """
    Abstract base class for a news article parser.
    Subclasses should implement the parsing logic using a specific
    LLM (e.g., Ollama, Gemini).
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.prompt = """
You are an expert text processing assistant. Your task is to carefully read the following text, which was scraped from a news website, and extract ONLY the main body content of the news article itself.

Please identify and isolate the primary narrative or report.

Specifically EXCLUDE the following types of content:
- Website headers, logos, and top navigation bars
- Sidebars with links, ads, or other widgets
- Footer information (copyright, contact links, site map)
- Advertisements (text or placeholders)
- Lists or grids of "Related Articles", "More Stories", "Recommended Videos"
- Comment sections and user-generated content
- Social media sharing buttons or links
- Author bylines, publication dates, and image captions (unless they are embedded directly within the flow of the main article sentences).
- Cookie consent banners or subscription prompts.

Output ONLY the clean, extracted text of the news article's main content. Do not include any explanatory text before or after the extracted article.

[--- START OF SCRAPED TEXT ---]

{}

[--- END OF SCRAPED TEXT ---]
"""

    @abstractmethod
    def parseArticle(self, article_content: str) -> str:
        """
        Parses the given article content based on the provided prompt.

        Args:
            article_content: The raw text content of the news article.

        Returns:
            The parsed content of the article as a string.
            Should raise NotImplementedError if not implemented by a subclass.
        """
        pass
