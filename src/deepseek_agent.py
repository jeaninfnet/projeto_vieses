from langchain_deepseek import ChatDeepSeek
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from config_template import template

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
        

class DeepSeekAgent:
    def __init__(self, model="deepseek-reasoner", temperature=2):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatDeepSeek(
                        model=self.model,
                        temperature=temperature,
                        response_format={'type': 'json_object'},
                        api_key=self.deepseek_api_key,
                    )

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

        jsonDict = clean_and_parse_json(output)
        return jsonDict
