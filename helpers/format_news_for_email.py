from pydantic_types.news_results import NewsResults
from datetime import datetime  # Add this line

def format_news_for_email(news_results: NewsResults, current_date: datetime) -> str:

    formatted_report_date = current_date.strftime("%B %d, %Y")
    email_body = f"<h1>Research Agents Update</h1>\n"
    email_body += f"<h2><strong>Report Date:</strong> {formatted_report_date}</h2>\n"
    email_body += "<hr>\n"

    for idx, news in enumerate(news_results, start=1):
        email_body += f"<p><strong>{news.category}</strong></p>\n"
        email_body += f"<h3>{idx}. {news.headline}</h3>\n"
        email_body += f"<p>{news.description}</p>\n"

        formatted_date = news.date.strftime("%B %d, %Y")
        email_body += f"<p><strong>Date:</strong> {formatted_date}</p>\n"
        email_body += "<p><strong>Sources:</strong> "

        source_links = []
        for source in news.sources:
            source_links.append(f"<a href='{source.url}'>{source.name}</a>")

        email_body += ", ".join(source_links) + "</p>\n"
        email_body += "<hr>\n"
    
    return email_body