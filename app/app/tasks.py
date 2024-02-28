# tasks.py
from celery import shared_task
import openai
import json
from django.db import IntegrityError
from blog.models import Professor
from langchain.llms import OpenAI
from .apikey import apikey
import os
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from account.models import *
# from websockets.consumers import *

# Define a function to generate research areas using OpenAI's GPT model
def generate_research_areas(text):
    os.environ['OPENAI_API_KEY'] = apikey



    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")


    prompt = f"Based on the provided text, generate research areas that closely match the content. Each research area should be concise, keyword-like. Please format the response as a python code, list of strings, where each string represents a research area.\n\n{text}\n\nResearch areas:"

    if prompt:
        response = llm.predict(prompt)
        
    return response


@shared_task
def process_json_data(json_data):
    channel_layer = get_channel_layer()
    try:
        data = json.loads(json_data)
        total_items = len(data)
        processed_items = 0


        for item in data:
            try:
                # If research areas are not provided, generate them based on the text in the "direction" field
                if item.get('direction'):
                    generated_direction = generate_research_areas(item.get('direction', ''))
                    item['direction'] = generated_direction

                professor_data = {
                    'name': item.get('name', ''),
                    'introduction': item.get('introduction', ''),
                    'phone': item.get('phone', ''),
                    'address': item.get('address', ''),
                    'achievements': item.get('achievements', ''),
                    'url': item.get('url', ''),
                    'city': item.get('city', ''),
                    'province': item.get('province', ''),
                    'country': "US",
                    'title': item.get('title', ''),
                    'email': item.get('email', ''),
                    'image_url': item.get('photo', ''),
                    'research_areas': item.get('direction',''),
                    'university': item.get('school', ''),
                    'department': item.get('college', ''),
                    'university_world_ranking': 324
                }

                Professor.objects.create(**professor_data)
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                # Send integrity error and no professor data
                async_to_sync(channel_layer.group_send)(
                    'logs_group',
                    {
                        'type': 'logs_group.send_logs',
                        'message': f"IntegrityError: {e}",
                        'professor_data': None,
                        'error': None,
                    }
                )
                continue
             # Increment processed items count
            processed_items += 1
            # Send progress update, professor data, and no error
           
            async_to_sync(channel_layer.group_send)(
                'logs_group',
                {
                    'type': 'logs_group.send_logs',
                    'message': f"Processed {processed_items}/{total_items} items.",
                    'professor_data': professor_data,
                    'error': None,
                }
            )
    except Exception as e:
        print(f"Error processing JSON data: {e}")
        # Send error message and no professor data
        async_to_sync(channel_layer.group_send)(
            'logs_group',
            {
                'type': 'logs_group.send_logs',
                'message': f"Error processing JSON data: {e}",
                'professor_data': None,
                'error': str(e),
            }
        )


@shared_task
def update_name(new_name,user_id):
    users = MyUser.objects.filter(id=user_id)
    user = users.first()
    user.name=new_name
    user.save()