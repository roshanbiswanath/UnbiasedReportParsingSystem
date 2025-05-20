from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

from typing import TypedDict, NotRequired


class Article(BaseModel):
    _id: Optional[ObjectId]
    title: str = Field(..., description="The title of the article")
    content: str = Field(..., description="The content of the article")
    url: str = Field(..., description="The URL of the article")
    source: str = Field(..., description="The source of the article")
    published_at: Optional[str] = Field(None, description="The publication date of the article")
    is_ai_parsed: bool = Field(False, description="Flag to indicate if the article has been passed into the AI pipeline")
    class Config:
        schema_extra = {
            "example": {
                "title": "Sample Article Title",
                "content": "This is a sample content for an article.",
                "url": "https://www.example.com/article",
                "source": "Example News Source",
                "published_at": "2023-10-01T12:00:00Z",
            }
        }
    def __str__(self):
        return f"Article(title={self.title}, content={self.content}, url={self.url}, source={self.source}, published_at={self.published_at})"










