from typing import Any, Text, Dict, List
import requests
import json
import pandas as pd
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,UserUtteranceReverted


class NameAction(Action):
    def name(self) -> Text:
        return "action_your_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            slot_name=str(tracker.get_slot("NAME"))

            message = "Hi {}  Do you want more about Corna Virus in Your Place!!example:--im leaving in statename, my district is.. and the ISO code is.. !".format(slot_name)

            dispatcher.utter_message(text=message)
            return []


class ActionState(Action):
    def name(self) -> Text:
        return "action_total_cases_in_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("https://api.covid19india.org/data.json").json()
        slot_iso_state = str(tracker.get_slot("iso_state"))
        entities = tracker.latest_message['entities']
        state = None

        ##print("In ActionState ",slot_iso_state)

        for e in entities:
            if e['entity'] == 'state':
                state = e['value']

        message = "Please enter correct state name"

        if state == 'India':
            state = 'Total'

        for data in response['statewise']:
            ##print(data['state']," ",data['statecode'])
            if data['statecode'] == slot_iso_state:
                ##print("INNNNNNNN")
                message = "Total Data : Active "+data['active']+" Confirmed "+data['confirmed']+" Recovered "+data['recovered']

        print(message)

        dispatcher.utter_message(text=message)
        return []