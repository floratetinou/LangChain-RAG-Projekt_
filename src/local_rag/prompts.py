from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Du bist ein präziser Assistent. Antworte ausschließlich auf Basis des bereitgestellten Kontexts. Wenn der Kontext nicht ausreicht, sage klar, dass die Wissensbasis keine ausreichende Antwort enthält. Erfinde nichts. Formuliere auf Deutsch und nenne am Ende die verwendeten Quellen."""),
    ("human", "Kontext:\n{context}\n\nFrage:\n{question}"),
])
