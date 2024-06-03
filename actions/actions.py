# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from rasa_sdk.events import AllSlotsReset
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import process
from rasa_sdk.events import UserUtteranceReverted
import requests
import os
import openai
import json
import random
import requests
import pandas as pd
from rasa_sdk import Action, Tracker 
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher


class ActionDefaultFallback(Action):

    """Rasa action to parse user text and pulls a corresponding answer 
    from ChatGPT."""

    def name(self) -> Text:
        return "action_default_fallback" 
    
    def get_answers_from_chatgpt(self, user_text):
        

        def load_api_key(secrets_file="secret.json"):
            with open(secrets_file) as f:
                secrets = json.load(f)
            return secrets["OPENAI_API_KEY"]
        
    # OpenAI API Key from secret.json
    
        api_key = load_api_key()
        
        client = openai.OpenAI(api_key=api_key)

        # Define the prompt
        prompt = f"User: {user_text}\nAI (Δώσε σύντομη απάντηση στα Ελληνικά με μέγιστο 300 tokens): "

        # Call the OpenAI API to generate a completion
        response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7
        )

        # Extract the generated text from the API response
        generated_text = response.choices[0].text.strip()

        return generated_text

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the latest user text 
        user_text = tracker.latest_message.get('text')
        response = self.get_answers_from_chatgpt(user_text)
        # Dispatch the response from OpenAI to the user
        dispatcher.utter_message('Απάντηση από το ChatGPT: ' + response)

        return []

        
class ActionTeacherInfo(Action):
    def name(self) -> Text:
        return "action_teacher_info"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lookup table for teacher first names and their contact information
        contact_info = {
            "Αγγελης": {
                "email": "lef@csd.auth.gr",
                "phone": "2310 99-8230"
            },
            "Βακαλη": {
                "email": "avakali@csd.auth.gr",
                "phone": "2310 99-8415"
            },
            "Βασιλειαδης": {
                "email": "nbassili@csd.auth.gr",
                "phone": "2310 99-7913"
            },
            "Βλαχαβας": {
                "email": "vlahavas@csd.auth.gr",
                "phone": "2310 99-8145"
            },
            "Βρακας": {
                "email": "dvrakas@csd.auth.gr",
                "phone": "2310 99-8885"
            },
            "Γουναρης": {
                "email": "gounaria@csd.auth.gr",
                "phone": "2310 99-1933"
            },
            "Δημητριαδης": {
                "email": "sdemetri@csd.auth.gr",
                "phone": "2310 99-1938"
            },
            "Δραζιωτης": {
                "email": "drazioti@csd.auth.gr",
                "phone": "2310 99-1928"
            },
            "Καντελης": {
                "email": "kos@csd.auth.gr",
                "phone": "2310 99-7974"
            },
            "Κατσανος": {
                "email": "ckatsanos@csd.auth.gr",
                "phone": "2310 99-1925"
            },
            "Κατσαρος": {
                "email": "katsaros@csd.auth.gr",
                "phone": "2310 99-8532"
            },
            "Κεραμιδας": {
                "email": "gkeramidas@csd.auth.gr",
                "phone": "2310 99-1926"
            },
            "Κονοφαος": {
                "email": "nkonofao@csd.auth.gr",
                "phone": "2310 99-1929"
            },
            "Κοτροπουλος": {
                "email": "costas@aiia.csd.auth.gr",
                "phone": "2310 99-8225"
            },
            "Λασκαρης": {
                "email": "laskaris@csd.auth.gr",
                "phone": "2310 99-8706"
            },
            "Μεδιτσκος": {
                "email": "gmeditsk@csd.auth.gr",
                "phone": "2310 99-8896"
            },
            "Μηλιου": {
                "email": "amiliou@csd.auth.gr",
                "phone": "2310 99-8407"
            },
            "Νικολαιδης": {
                "email": "nnik@csd.auth.gr",
                "phone": "2310 99-8566"
            },
            "Νικοπολιτιδης": {
                "email": "petros@csd.auth.gr",
                "phone": "2310 99-8538"
            },
            "Ουζουνης": {
                "email": "cao@csd.auth.gr",
                "phone": "2310 99-8412"
            },
            "Παπαδημητριου": {
                "email": "gp@csd.auth.gr",
                "phone": "2310 99-8221"
            },
            "Παπαδοπουλος": {
                "email": "papadopo@csd.auth.gr",
                "phone": "2310 99-1918"
            },
            "Πητας": {
                "email": "pitas@csd.auth.gr",
                "phone": "2310 99-6304"
            },
            "Πλερος": {
                "email": "npleros@csd.auth.gr",
                "phone": "2310 99-8776"
            },
            "Πολιτης": {
                "email": "dpolitis@csd.auth.gr",
                "phone": "2310 99-8406"
            },
            "Σταμελος": {
                "email": "stamelos@csd.auth.gr",
                "phone": "2310 99-1910"
            },
            "Τεφας": {
                "email": "tefas@csd.auth.gr",
                "phone": "2310 99-1932"
            },
            "Τσιατσος": {
                "email": "tsiatsos@csd.auth.gr",
                "phone": "2310 99-8990"
            },
            "Τσιτσας": {
                "email": "ntsitsas@csd.auth.gr",
                "phone": "2310 99-1866"
            },
            "Τσουμακας": {
                "email": "greg@csd.auth.gr",
                "phone": "2310 99-8887"
            },
            "Χριστοδουλου": {
                "email": "gichristo@csd.auth.gr",
                "phone": "2310 99-1934"
            }
        }


        # Get the teacher's name provided by the user
        teacher_name = tracker.latest_message['entities'][0]['value'] if tracker.latest_message['entities'] else None

        if teacher_name and teacher_name in contact_info:
            teacher_contact_info = contact_info[teacher_name]
            response = f"Στοιχεία επικοινωνίας κ. {teacher_name}:\nEmail: {teacher_contact_info.get('email', 'N/A')}\nPhone: {teacher_contact_info.get('phone', 'N/A')}"
        else:
            # Use fuzzy matching to find the closest match
            matched_name, score = process.extractOne(teacher_name, contact_info.keys())
            if score >= 80:  # Adjust the threshold as needed
                teacher_contact_info = contact_info[matched_name]
                response = f"Στοιχεία επικοινωνίας κ. {matched_name}:\nEmail: {teacher_contact_info.get('email', 'N/A')}\nPhone: {teacher_contact_info.get('phone', 'N/A')}"
            else:
                response = "Δεν μπορώ να βρω πληροφορίες για αυτόν τον καθηγητή."

        dispatcher.utter_message(text=response)

        return []

class ActionResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    async def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]