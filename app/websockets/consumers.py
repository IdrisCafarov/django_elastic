# consumers.py
from account.models import *

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from django.db import IntegrityError
from blog.models import Professor
from channels.layers import get_channel_layer

class LogsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("ve aleykum salam qaqa")
        self.group_name = 'logs_group'
        self.channel_layer = get_channel_layer()
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("salam da qaqa")
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()

    async def receive(self, text_data):
        pass

    async def send_logs(self, event):
        print("qaqa I am working")
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'professor_data': event['professor_data'],
            'error': event['error'],
        }))


from langchain.llms import OpenAI
from app.apikey import apikey
import os
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.output_parsers import JsonOutputParser
from langchain.tools.render import render_text_description

# llm = ChatOpenAI()
os.environ['OPENAI_API_KEY'] = apikey



# @tool
# def change_user_name(user_id: int, new_name: str):
#     """Change user name from database."""
#     users = MyUser.objects.filter(id=user_id)
#     user = users.first()
#     user.first_name = new_name
#     user.save()
#     return "Data saved"



# rendered_tools = render_text_description([change_user_name])


# llm = ChatOpenAI(temperature=0, model_name="ft:gpt-3.5-turbo-1106:personal::8u9uwlvM")
# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers import PydanticOutputParser
# from langchain_core.prompts import ChatPromptTemplate

# class SearchSchema(BaseModel):
#     includedUniversities: list[str] = Field(description="The wide list of universities which is good at in that field")
#     includedCompanies: list[str] = Field(description="The wide list of companies which is good at in that field")
#     includedAreas: list[str] = Field(description="The wide list of areas which is need that field")
    

# pydantic_parser = PydanticOutputParser(pydantic_object=SearchSchema)
# format_instructions = pydantic_parser.get_format_instructions()
# print(format_instructions)
# FIELD_SEARCH_PROMPT = """
# Please provide a list of at least 10 universities and 10 companies known for their expertise in given field. And areas which need that field

# {format_instructions}

# Recipe Search Request:
# {request}
# """

# class PracticeConsumer(AsyncWebsocketConsumer):
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     self.conversation_context = ""


#     async def connect(self):
#         try:
#             await self.accept()
#             print("WebSocket connection established")
#         except Exception as e:
#             print(f"WebSocket connection error: {e}")
#             await self.close()

#     async def disconnect(self, close_code):
#         # Called when the WebSocket closes for any reason
#         # Perform cleanup tasks if necessary
#         print("WebSocket connection closed")

#     async def receive(self, text_data):
        

#         system_prompt = f"""You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:

#             {rendered_tools}

#             Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys."""

#         prompt = ChatPromptTemplate.from_messages(
#         [("system", system_prompt), ("user", "{input}")]
#         )
#         chain = prompt | llm | JsonOutputParser()

#         request = text_data
#         result = chain.invoke(request)

#         await self.send(text_data=result)
from app.tasks import *
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.messages import HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import Type,Optional
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
@tool
def change_user_name(new_name: str,user_id: int) -> str:
    """Change the user's Name"""
    users = MyUser.objects.filter(id=user_id)
    user = users.first()
    user.first_name=new_name
    user.save()
    return "LangChain"

class ChangeNameInput(BaseModel):
    """Inputs for change_user_name function"""
    new_name: str = Field(description="The New name user wants to define for account")
    user_id: int = Field(description="User's account id for to be able to find and changes the user's name in database")

class ChangeUsernameTool(BaseTool):
    name = "change_user_name"
    description = """
        Useful when you want to change your name in your account
        Account id and new account name must be asked from user !
        If any of the data account id or new name not given by user ask again to user. Do not make it random
        """
    args_schema: Type[BaseModel] = ChangeNameInput
    return_direct: bool = True


    def _run(
        self, new_name: str,user_id: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Change the user's Name"""
        update_name.delay(new_name,user_id)
        return "LangChain"


    async def _arun(
        self, new_name: str,user_id: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

llm = ChatOpenAI(
    temperature=0, model="gpt-3.5-turbo-0613"
)
tools = [
    ChangeUsernameTool()
]




chat_history = MessagesPlaceholder(variable_name="chat_history")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


class PracticeConsumer(AsyncWebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.conversation_context = ""


    async def connect(self):
        try:
            await self.accept()
            print("WebSocket connection established")
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        # Called when the WebSocket closes for any reason
        # Perform cleanup tasks if necessary
        print("WebSocket connection closed")

    async def receive(self, text_data):
        

        agent = initialize_agent(
            tools, 
            llm, 
            agent=AgentType.OPENAI_FUNCTIONS, 
            verbose=True,
            agent_kwargs={
                "memory_prompts": [chat_history],
                "input_variables": ["input", "agent_scratchpad", "chat_history"]
            },
            memory=memory
            )
        result = agent.run(text_data)

        await self.send(text_data=result)