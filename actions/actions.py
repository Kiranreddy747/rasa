# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random

class ActionSayData(Action):
    def name(self) -> Text:
        return "action_say_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the latest user intent
        intent = tracker.latest_message.get("intent", {}).get("name")

        # Map all intents to their corresponding utter responses
        intent_to_utter = {
            "greet": "utter_greet",
            "goodbye": "utter_goodbye",
            "ask_deadline": "utter_ask_deadline",
            "ask_documents": "utter_ask_documents",
            "ask_eligibility": "utter_ask_eligibility",
            "ask_fees": "utter_ask_fees",
            "ask_scholarships": "utter_ask_scholarships",
            "ask_facilities": "utter_ask_facilities",
            "ask_contact": "utter_ask_contact"
        }

        if intent in intent_to_utter:
            utter_key = intent_to_utter[intent]
            responses = domain.get("responses", {}).get(utter_key, [])
            
            if responses:
                # Randomly select and send one response
                chosen_response = random.choice(responses)
                dispatcher.utter_message(text=chosen_response.get("text", ""))
            else:
                dispatcher.utter_message(text="I don't have a response for that yet.")
        else:
            # Use random default response for unmapped intents
            default_responses = domain.get("responses", {}).get("utter_default", [])
            
            if default_responses:
                dispatcher.utter_message(text=random.choice(default_responses).get("text", ""))
            else:
                dispatcher.utter_message(text="Could you please rephrase that?")

        return []