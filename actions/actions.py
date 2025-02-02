from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
    
class ActionScheduleAppointment(Action):
    def name(self) -> Text:
        return "action_schedule_appointment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        appointment_date = tracker.get_slot("appointment_date")
        appointment_time = tracker.get_slot("appointment_time")

        if appointment_date and appointment_time:
            dispatcher.utter_message(text=f"Your appointment has been scheduled for {appointment_date} at {appointment_time}.")
        else:
            dispatcher.utter_message(text="Please provide a date and time for the appointment.")

        return []

class ActionRescheduleAppointment(Action):
    def name(self) -> Text:
        return "action_reschedule_appointment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        appointment_date = tracker.get_slot("appointment_date")
        appointment_time = tracker.get_slot("appointment_time")

        if appointment_date and appointment_time:
            dispatcher.utter_message(text=f"Your appointment has been rescheduled to {appointment_date} at {appointment_time}.")
        else:
            dispatcher.utter_message(text="Please provide the new date and time for rescheduling.")

        return []

class ActionRecordSymptoms(Action):
    def name(self) -> Text:
        return "action_record_symptoms"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = tracker.latest_message.get("text")
        dispatcher.utter_message(text=f"Got it! I've recorded the following symptoms: {symptoms}.")
        return [SlotSet("symptoms", symptoms)]

class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Let me check the doctor's availability. Please wait a moment...")
        # Simulate checking availability (this could be extended to connect to a database)
        dispatcher.utter_message(text="The doctor is available tomorrow at 3 PM. Would you like to book this slot?")
        return []

class ActionSymptomFollowUp(Action):
    def name(self) -> Text:
        return "action_symptom_follow_up"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        previous_symptoms = tracker.get_slot("symptoms")
        if previous_symptoms:
            dispatcher.utter_message(text=f"Following up on your symptoms: {previous_symptoms}. Have there been any changes?")
        else:
            dispatcher.utter_message(text="I don't have any recorded symptoms for you. Could you share them with me?")
        return []


class ActionCallOllama(Action):
    def name(self) -> Text:
        return "action_call_ollama"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get user message
        user_message = tracker.latest_message.get("text")

        # Call Ollama API
        ollama_url = "http://localhost:11434/api/generate"  # Ollama API endpoint
        payload = {
            "model": "llama2",  # Replace with your model name
            "prompt": user_message,
            "stream": False  # Disable streaming for simplicity
        }

        try:
            response = requests.post(ollama_url, json=payload)
            if response.status_code == 200:
                # Extract the generated response
                generated_text = response.json().get("response")
                dispatcher.utter_message(text=generated_text)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't generate a response.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []
