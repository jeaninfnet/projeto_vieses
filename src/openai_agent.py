from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from config_template import template

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain

import logging
import os
from utils import clean_and_parse_json

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

class TravelTemplate:
    def __init__(self):

        self.system_template = template

        self.human_template = """
        #### {request}
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt,
                                                             self.human_message_prompt])
        

class OpenAIAgent:
    def __init__(self, model="gpt-4", temperature=1):
        self.open_ai_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatOpenAI(model=self.model,
                                     temperature=self.temperature,
                                     openai_api_key=self.open_ai_key)

    def get_opinion(self, request):
        travel_prompt = TravelTemplate()
        parser = LLMChain(
            llm=self.chat_model,
            prompt=travel_prompt.chat_prompt,
            output_key="opinion"
        )

        result = parser.invoke({"request": request})
        output = result['opinion']
        if not output:
            return []

        return clean_and_parse_json(output)
