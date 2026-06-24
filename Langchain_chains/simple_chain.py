from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import strOutputParser

load_dotenv()

llm = ChatOpenAI()

prompt = PromptTemplate(
    Template='Generate 5 interesting facts about {topic}.',
    input_variables=['topic'],
)

parser = strOutputParser()

chain = prompt | llm | parser

reseult = chain.invoke({'topic': 'Astronomy'})
