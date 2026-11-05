
import os
import time

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0.2
    )


def build_chain(system_prompt: str):
    llm = get_llm()

    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}"),
        ])
        | llm
        | StrOutputParser()
    )


# Divide long transcripts into smaller sections
def split_transcript(transcript: str, chunk_size: int = 3000):
    transcript = transcript.strip()

    return [
        transcript[i:i + chunk_size]
        for i in range(0, len(transcript), chunk_size)
    ]


# Process each section separately
def extract_from_chunks(transcript: str, system_prompt: str, empty_message: str):
    chunks = split_transcript(transcript)

    if not chunks:
        return empty_message

    chain = build_chain(system_prompt)
    results = []

    for i, chunk in enumerate(chunks):
        print(f"Extracting section {i + 1}/{len(chunks)}...")

        try:
            result = chain.invoke(chunk)
            results.append(result.strip())

        except Exception as e:
            print(f"Extraction error in section {i + 1}: {e}")
            raise

        # Space out requests to help manage Groq rate limits
        if i < len(chunks) - 1:
            time.sleep(15)

    return "\n\n".join(results)


def extract_action_items(transcript: str) -> str:
    return extract_from_chunks(
        transcript,
        "You are an expert meeting analyst. From this transcript section, "
        "extract all action items. For each provide:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'Not specified')\n\n"
        "Do not invent information. Format as a numbered list. "
        "If none found say 'No action items found.'",
        "No action items found."
    )


def extract_key_decisions(transcript: str) -> str:
    return extract_from_chunks(
        transcript,
        "You are an expert meeting analyst. From this transcript section, "
        "extract all key decisions actually made. Do not include suggestions "
        "as confirmed decisions. Format as a numbered list. "
        "If none found say 'No key decisions found.'",
        "No key decisions found."
    )


def extract_questions(transcript: str) -> str:
    return extract_from_chunks(
        transcript,
        "From this transcript section, extract all unresolved questions "
        "or topics needing follow-up. Do not invent questions. "
        "Format as a numbered list. "
        "If none found say 'No open questions found.'",
        "No open questions found."
    )
