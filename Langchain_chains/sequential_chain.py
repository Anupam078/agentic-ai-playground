from langchain_openai import ChatOpenAI
from llangchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import strOutputParser
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI()
prompt = PromptTemplate(
    Template='Generate a detailed report about {topic}.',
    input_variables=['topic'],
)

prompt2 = PromptTemplate(
    Template='Generate 5 line summary of the following report: {report}.',
    input_variables=['report'],
)

parser = strOutputParser()

chain = prompt | llm | parser | prompt2 | llm | parser

chain_result = chain.invoke({'topic': 'Astronomy'})
print(chain_result)


