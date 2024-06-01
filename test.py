from langchain_core.prompts import prompt, PromptTemplate
from langchain_openai import OpenAI


llm = OpenAI(openai_api_key="AQVN1QYhY-29ScLDCbm8O0LnQ2b9kvEviIV-B7EF", openai_organization="ajel0ogm7rdt971c62dp")


template = """Question: {question}"""

prompt = PromptTemplate.from_template(template)

llm_chain = prompt | llm

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

llm_chain.invoke(question)