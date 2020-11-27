from typing import Any, Text, Dict, List
import requests
import json
import pandas as pd
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,UserUtteranceReverted
from actions import emailsend


class NameAction(Action):
    def name(self) -> Text:
        return "action_your_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            slot_name=str(tracker.get_slot("NAME"))

            message = "Hi {}  Do you want more about Corna Virus in Your Place!!example:--Im living in statename, my district is.. and the ISO code is.. !".format(slot_name)

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


class ActionEmailSend(Action):
    def name(self) -> Text:
        return "action_email_send"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            slot_email=str(tracker.get_slot("email_id"))
            print(slot_email)
            emailsend.emailsend(slot_email)

            message = "Email Has Been Sent to {} where we have provided all the necessary COVID updates and information.".format(slot_email)

            dispatcher.utter_message(text=message)
            return []



class ActionHelpline(Action):
    def name(self) -> Text:
        return "action_helpline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            slot_full_state=str(tracker.get_slot("user_state"))
            slot_full_state=slot_full_state.capitalize()
            dfs=pd.read_html("https://www.indiatvnews.com/coronavirus/helpline-numbers")
            df=dfs[0]
            df=df['State Helpline Numbers']
            x=df.loc[lambda df: df['State/UT'] == slot_full_state]
            for i in x.values:
                ans=i[1]

            message = "{} Helpline Number is {}".format(slot_full_state,ans)

            dispatcher.utter_message(text=message)
            return []