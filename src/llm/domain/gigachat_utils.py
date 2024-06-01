from langchain_core.messages import SystemMessage, HumanMessage

from llm.domain.llm import giga_chat_llm, openai_llm

llm = openai_llm

SYSTEM_PROMPT = (
    "Ты — русскоязычный автоматический ассистент финансового отдела. Ты отвечаешь на вопросы пользователя, на основе базы вопросов и ответов."
    "Отвечай на вопрос пользователя только на основе информации из базы знаний. Давай развернутый ответ, не обрезай информацию. Если ответ является инструкцией, приводи его полностью. Если база знаний не содержит"
    "релевантной информации, отвечай: не достаточно информации для ответа."
)

SYSTEM_PROMPT_EN = (
    "You are an automated assistant in the patent department. You help people find accurate information in the body of a report."
    "Answer the user's query only based on information from the report."
    " If the report fragment does not contain relevant information, answer: not enough information to answer."
                 )

async def simple_prompt(message: str):
    messages = [SystemMessage(content=message)]
    output = await llm.ainvoke(messages)
    return output.content


async def rag_prompt(query: str, context: str):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f'Информация из базы знаний:\n{context}\nВопрос пользователя:\n{query}')
    ]
    output = await llm.ainvoke(messages)
    return output.content






