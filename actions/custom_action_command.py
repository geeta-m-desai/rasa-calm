from rasa.dialogue_understanding.commands.knowledge import (KnowledgeAnswerCommand)
import openai
import os


class CustomKnowledgeAnswerCommand(KnowledgeAnswerCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch from environment

    def predict_commands(self, message):
        user_question = message.data['text']

        response = openai.Completion.create(
            engine="gpt4-turbo",
            prompt=user_question,
            max_tokens=150,  # Adjust if needed
        )

        llm_answer = response.choices[0].text.strip()
        return StartFlowCommand(flow='respond_to_question', flow_data={'answer': llm_answer})
