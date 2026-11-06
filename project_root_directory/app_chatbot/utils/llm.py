import os
import re
from typing import List

import litellm
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models import ChatLiteLLM
from langchain_huggingface import HuggingFaceEmbeddings

# Drop params a model rejects (e.g. temperature=0 on reasoning models)
litellm.drop_params = True

LLM_MODEL = os.environ.get("LLM_MODEL", "azure/gpt-4o")
EMBEDDING_MODEL = os.environ.get(
    "EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")

EMBEDDING_DIMENSIONS = 768
_embeddings = None


class LiteLLMEmbeddings(Embeddings):
    def __init__(self, model: str, dimensions: int = EMBEDDING_DIMENSIONS):
        self.model = model
        self.dimensions = dimensions

    def _embed(self, texts: List[str]) -> List[List[float]]:
        out = []
        for i in range(0, len(texts), 64):
            resp = litellm.embedding(
                model=self.model, input=texts[i:i + 64],
                dimensions=self.dimensions)
            out.extend(d["embedding"] for d in resp.data)
        return out

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])[0]


def get_llm(json_mode=False, temperature=0):
    forced = os.environ.get("LLM_TEMPERATURE")
    if forced:
        temperature = float(forced)
    elif re.search(r"(gpt-5|/o[134](-|$))", LLM_MODEL):
        temperature = 1  # reasoning models only accept the default
    model_kwargs = {}
    if json_mode and not LLM_MODEL.startswith(("anthropic/", "claude")):
        model_kwargs["response_format"] = {"type": "json_object"}
    return ChatLiteLLM(
        model=LLM_MODEL, temperature=temperature, model_kwargs=model_kwargs)


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        if EMBEDDING_MODEL.startswith(("azure/", "openai/")):
            _embeddings = LiteLLMEmbeddings(EMBEDDING_MODEL)
        else:
            _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings
