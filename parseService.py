from util.mongoConn import getClient
from DTO.ParsedArticle import ParsedArticle
import time
from dotenv import load_dotenv
load_dotenv()

from util.parser.OllamaParser import OllamaParser
from util.parser.GeminiParser import GeminiParser

PARSISNG_MODEL = "gemma3:4b"
SCRAPED_ARTICLES_COLLECTION = "scrapedArticles"
PARSED_ARTICLES_COLLECTION = "parsedArticles"
OLLAMA_PROMPT = """
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



def storeParsedRecord(db, parsedRecord):
    collection = db[PARSED_ARTICLES_COLLECTION]
    result = collection.insert_one(parsedRecord.model_dump())
    if result.acknowledged:
        print(f"Stored parsed record with ID {result.inserted_id}.")
    else:
        print("Failed to store parsed record.")

def markAsParsed(db, collection_name, article_id):
    collection = db[collection_name]
    query = {"_id": article_id}
    update = {"$set": {"is_ai_parsed": True}}
    result = collection.update_one(query, update)
    if result.modified_count > 0:
        print(f"Marked article with ID {article_id} as parsed.")
    else:
        print(f"Failed to mark article with ID {article_id} as parsed.")

# def parseRecord(article):
#     print(f"Parsing article: {article['title']}")
#     # print(OLLAMA_PROMPT.format(article['content']))
#     timeBefore = time.time()
#     response = ollama.chat(model=PARSISNG_MODEL, messages=[
#         {
#             'role': 'user',
#             'content': OLLAMA_PROMPT.format(article['content']),
#         },
#     ])
#     timeAfter = time.time()
#     print(f"Parsing took {timeAfter - timeBefore} seconds")
#     return response['message']['content']

def getArticlesToParse(db, collection_name, limit=10):
    collection = db[collection_name]
    query = {"is_ai_parsed": False}
    oldest_records = collection.find(query).sort("creationDate", 1).limit(limit)
    return list(oldest_records)

if __name__ == "__main__":
    mongoClient = getClient()
    db = mongoClient["reportDB"]
    # parser = OllamaParser()
    parser = GeminiParser()
    while True:
        articles = getArticlesToParse(db, SCRAPED_ARTICLES_COLLECTION, limit=10)
        if articles is None or len(articles) == 0:
            print("No records found")
            time.sleep(10)
        else:
            print(f"Found { len(articles) } records to parse.")
        for article in articles:
            parsedRecord = parser.parseArticle(article['content'])
            if parsedRecord is None:
                print(f"Failed to parse article: {article['title']}")
                continue
            markAsParsed(db, SCRAPED_ARTICLES_COLLECTION, article['_id'])
            print(f"Parsed article: {article['title']}")
            # print(f"Original content: {article['content']}")
            # print(f"Parsed content: {parsedRecord}")
            parsedRecord = ParsedArticle(
                title=article['title'],
                content=parsedRecord,
                url=article['url'],
                source=article['source'],
                published_at=article['published_at'],
                source_id=str(article['_id'])
            )
            storeParsedRecord(db, parsedRecord)
