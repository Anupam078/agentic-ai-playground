from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import strOutputParser
from langchain.schema.runnable import RunnableParallel
from dotenv import load_dotenv
load_dotenv()

model1 = ChatOpenAI()
model2 = ChatAnthropic(model='claude-2')

prompt1 = PromptTemplate(
    Template='Generate short and simple notes from the following text: {text}.',
    input_variables=['text']
)

prompt2 = PromptTemplate(
    Template='Generate 5 quiz questions from the following text: {text}.',
    input_variables=['text']
)

prompt3 = PromptTemplate(
    Template='Generate a merged single documnet from the following notes: {notes} and quiz questions: {questions}.',
    input_variables=['notes', 'questions']
)

parser = strOutputParser()

parrallel_chain = RunnableParallel(
    {  notes: prompt1 | model1 | parser,
        questions: prompt2 | model2 | parser
        }   
)

merged_chain = parrallel_chain | prompt3 | model1 | parser

result = merged_chain.invoke({'text': 'Astronomy is the scientific study of celestial objects, space, and the universe as a whole. It encompasses the observation and analysis of stars, planets, galaxies, and other cosmic phenomena. Astronomers use telescopes and other instruments to gather data, which helps them understand the origins, evolution, and behavior of celestial bodies. The field of astronomy also explores fundamental questions about the nature of the universe, including its formation, structure, and eventual fate.'})
print(result)
