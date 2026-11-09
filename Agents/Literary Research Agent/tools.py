from langchain.tools import tool
from urllib.request import urlopen
@tool
def fetch_text_from_url(url:str):
    """ Use this tool to fetch text from given url for research purpose"""
    response = urlopen(url)
    return response.read().decode('utf-8')