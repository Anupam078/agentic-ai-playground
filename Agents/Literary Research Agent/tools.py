from langchain.tools import tool
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import ssl
import certifi

@tool
def fetch_text_from_url(url: str) -> str:
    """
    Fetches the text content from a given URL.
    
    Args:
        url (str): The URL to fetch the text from.
    
    Returns:
        str: The text content of the URL.
    """
    try:  
        ssl_context = ssl.create_default_context(
            cafile=certifi.where()
      )
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req,timeout=10,context=ssl_context) as response:
            return response.read().decode('utf-8')

    except HTTPError as e:
        return f"HTTP Error: {e.code} - {e.reason}"
    except URLError as e:
        return f"URL Error: {e.reason}"
    except Exception as e:
        return f"An error occurred: {str(e)}"