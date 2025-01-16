import requests
from bs4 import BeautifulSoup
from crewai.tools import tool

from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class UrlQaToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    link: str = Field(..., description="source link to check")

class UrlQaTool(BaseTool):
    name: str = "Link Quality Checker"
    description: str = "This tool can be used to check if a link is working or not."
    args_schema: Type[BaseModel] = UrlQaToolInput

    def _run(self, link: str) -> str:
        """
        Validates if a URL is working and checks the quality of its content.

        Args:
            url (str): The URL to validate and analyze.

        Returns:
            dict: A dictionary containing 'is_working' (bool), 'quality' (bool),
                  and 'reason' (str) explaining the quality evaluation.
        """
        try:
            # Send a GET request to the URL with a timeout
            response = requests.get(link, timeout=10)
            
            # Check if the response status code indicates success
            if response.status_code // 100 not in [2, 3]:
                return {
                    "is_working": False,
                    "quality": False,
                    "reason": f"Invalid status code: {response.status_code}",
                }
            
            # Analyze the page content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the text content for analysis
            page_text = soup.get_text(strip=True).lower()
            
            # Check basic quality indicators
            title = soup.title.string.strip() if soup.title else None
            word_count = len(page_text.split())
            headers = soup.find_all(["h1", "h2", "h3"])
            
            if not title or word_count < 100 or len(headers) < 1:
                return {
                    "is_working": True,
                    "quality": False,
                    "reason": "Page lacks sufficient content or structure (e.g., missing title, low word count, or headers).",
                }
            
            # The page is considered quality if it passes all criteria
            return {
                "is_working": True,
                "quality": True,
                "reason": "Page has a title, sufficient content, and structured headers.",
            }
        
        except requests.RequestException as e:
            # Handle network errors
            return {
                "is_working": False,
                "quality": False,
                "reason": f"Request failed: {e}",
            }