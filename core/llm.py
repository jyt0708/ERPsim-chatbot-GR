import getpass
import os
from langsmith import Client
from langchain_ibm import ChatWatsonx
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI


LANGCHAIN_API_KEY = "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"
WATSONX_APIKEY = "Vy_inytzWJVdtVCWh1vHz1uL1QQJ3Wc1N2Jfsz1qqzxZ"

# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "erpsim-multi-agent"
# os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["WATSONX_APIKEY"] = WATSONX_APIKEY


llm_model = ChatWatsonx(
    model_id="openai/gpt-oss-120b",  # openai/gpt-oss-120b, mistralai/mistral-medium-2505
    url="https://us-south.ml.cloud.ibm.com",
    project_id="7246d96f-2ba2-4231-97c7-79153513cb4c",
    params={
        GenParams.DECODING_METHOD: "greedy",
        GenParams.TEMPERATURE: 0
    },
)

def get_llm(model_id: str = "openai/gpt-oss-120b"):
    llm_model = ChatWatsonx(
        model_id=model_id,  # openai/gpt-oss-120b, mistralai/mistral-medium-2505
        url="https://us-south.ml.cloud.ibm.com",
        project_id="7246d96f-2ba2-4231-97c7-79153513cb4c",
        params={
            GenParams.DECODING_METHOD: "greedy",
            GenParams.TEMPERATURE: 0
        },
    )
    return llm_model