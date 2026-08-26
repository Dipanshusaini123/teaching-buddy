from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
llm = ChatGroq(model ="openai/gpt-oss-120b")
history= []
summary = ""

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a helpful AI assistant and teaching buddy.

Use the memory below to personalize your responses.

LONG-TERM MEMORY:
{summary}

RECENT CONVERSATION:
{history}

Instructions:
- Use long-term memory for important facts and preferences.
- Use recent conversation to maintain immediate context.
- Do not mention the memory system unless asked.
- Adapt explanations to the user's understanding level.
- If recent conversation conflicts with old memory, prefer recent information.
""")
])

summary_chain = summary_prompt | llm







prompt = ChatPromptTemplate.from_messages([
   ("system", """
    You are a helpful AI assistant and teaching buddy.
    Explain concepts clearly and adapt to the student's level.you also use previous memory 
    of a student or any person to presonalise response on there understanding levels
    here is a previous chat summary ,{summary}
    here is a recent previous messages , {history}
    """),

    ("human", "{query}")
])

chain = prompt|llm






while True:
    query = input("you:")
    
    if(query=="0"):
        break

    
    response = chain.invoke({"query":query, "history": history, "summary":summary})
    print(f"AI:",response.content)
    history.append({"human":query})
    history.append({"assistant": response.content})

    if len(history)>10:
        old_history = history[:-6]
        history = history[-6:]
        summary_response = summary_chain.invoke({"summary": summary,"old_history": old_history})
        summary = summary_response.content




print(summary)