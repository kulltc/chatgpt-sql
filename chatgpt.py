import os
import openai
import logging
import json

class ChatGPT:

    startMessageStack = []

    def __init__(self, api_key, api_org = "", model = "gpt-3.5-turbo", startMessageStack = []):
        if api_org:
            openai.api_key
        openai.api_key = api_key
        self.model = model
        self.startMessageStack = startMessageStack
        self.messages = self.startMessageStack.copy()

    def message(self, message, sender):
        logging.debug(message)
        if (sender):
            message = json.dumps({'message':message, 'sender':sender})
        self.messages.append({"role": "user", "content": message})
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content 
        logging.debug(response)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.messages = self.startMessageStack.copy()
        print('model was reset to intial state')

