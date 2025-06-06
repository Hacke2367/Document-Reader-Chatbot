from langchain.chains.question_answering.map_rerank_prompt import output_parser
from langchain_community.llms import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from typing import List
from langchain_core.documents import Document
import os
from chroma_utlis import vectorstore

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

output_pars = StrOutputParser()

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

load_dotenv()

def get_rag_chain(model="mistralai/Mistral-7B-v0.1"):
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    client = InferenceClient(token=token)

    class HFHubLLMWrapper:
        def __init__(self, client, model):
            self.client = client
            self.model = model

        def __call__(self, prompt: str):
            response = self.client.text_generation(
                model=self.model,
                inputs=[prompt],
                parameters={"max_new_tokens": 512, "temperature": 0.7}
            )
            # Agar API ka response structure alag ho to yahan adjust kar lena
            return response[0].generated_text

    llm = HFHubLLMWrapper(client, model)

    history_aware_retreiver = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retreiver, question_answer_chain)

    return rag_chain
