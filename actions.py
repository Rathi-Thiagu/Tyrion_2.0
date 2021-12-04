# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action,Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import csv
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
positive = {'never':0,'almost never':1,'sometimes':2,'fairly often':3,'very often':4}
negative = {'never':4,'almost never':3,'sometimes':2,'fairly often':1,'very often':0}
#dataset loading 
df_cd  = pd.read_csv('/data/complaint_details.csv')
df_emp = pd.read_csv('/data/employee_details.csv')
df_app = pd.read_csv('/data/app_details.csv')
df_fc  = pd.read_csv('/data/FC.csv')
df_ven = pd.read_csv('/data/FC_items.csv')

class ActionRaiseComplaints(Action):

    def name(self) -> Text:
        return "action_raise_complaints"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        empId = tracker.get_slot("employeeId")
        if empId:
            dispatcher.utter_message(text=f"Your employee ID is {empId}. Could you please confirm by retyping it?")
        else:
            dispatcher.utter_message(text=f"Please provide the employee ID")
        return [SlotSet('employeeId',tracker.latest_message['text'])]

class ActionAskComplaint(Action):

    def name(self) -> Text:
        return "action_ask_complaint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #df_cd=pd.read_csv('/content/drive/MyDrive/complaint_details.csv')
        dispatcher.utter_message(text=f"Give your complaint description. Please type it in this format (E.g) Description:your_complaint")
        return [SlotSet('complaintType',tracker.latest_message['text'])]

class ActionAskRegister(Action):
    def name(self) -> Text:
        return "action_ask_register"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f'shall I go ahead and raise complaint?')
        return [SlotSet('complaint_description',tracker.latest_message['text'])]

class ActionRegisterComplaint(Action):
    def name(self) -> Text:
        return "action_register_complaint"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #df_cd=pd.read_csv('/content/drive/MyDrive/complaint_details.csv')
        complaintId = 'CMP'+ str(len(df_cd.index))
        comp_type = tracker.get_slot("complaintType")
        empId = tracker.get_slot("employeeId")
        comp_des = tracker.get_slot("complaint_description")
        df_cd.loc[len(df_cd.index)] = [complaintId, comp_type,empId,comp_des,"Open"]
        df_cd.to_csv('/content/drive/MyDrive/complaint_details.csv',index = False)
        dispatcher.utter_message(text=f'Thank you. Your complaint was successfully registered. Our employee service department will contact you for more information.')
        #df_emp = pd.read_csv('/content/drive/MyDrive/employee_details.csv')
        empId = int(empId)
        output_emp =[row for row in df_emp.iterrows() if row[1][0] == empId]
        email=output_emp[0][1][4]
        subject = "Complaint Acknowledgement"
        msg_intro=f"Hi , "
        email_msg1 = f"Your complaint was successfully registered. Our employee service department will contact you for more information. "+'\n'"Below are the details of the complaint,"
        email_msg2 = f"Complaint Id: {complaintId}"+'\n'+f"Complaint Type: {comp_type}"+'\n'+f"{comp_des}"
        msg_tnk= f'Thank you, '+'\n'+'Tyrion-Chatbot powered by RASA'
        email_msg = msg_intro+'\n'+email_msg1+'\n'+email_msg2+'\n'+'\n'+msg_tnk
        SendEmail(email,subject,email_msg)
        return []


class ActionErgonomicsAssessment(Action):

    def name(self) -> Text:
        return "action_ergonomics_assessment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Our company employs ergonomists who can help you with questions.")
        dispatcher.utter_message(text="Below are the ergonomists for your Energy department")
        dispatcher.utter_message(text="1. Rebecca    rebecca_12@domain.com")
        dispatcher.utter_message(text="2. Stephen    stephen_09@domain.com")
        dispatcher.utter_message(text="You may contact them via email to inquire about their availability to assist you with setting up an ergonomically safe workplace.")
        return []

class Actiondescribeissue(Action):

    def name(self) -> Text:
        return "action_describe_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #df_emp=pd.read_csv('/content/drive/MyDrive/employee_details.csv')
        empid =  tracker.get_slot("employeeId")
        empid = int(empid)
        output =[row for row in df_emp.iterrows() if row[1][0] == empid]
        if output:
            message =f'Hey {output[0][1][1]} ...' + 'Please describe your ergonomics issue.'
        else: 
            message ='Please describe your ergonomics issue.'
        dispatcher.utter_message(text = message)
        return [SlotSet('employeeId',tracker.latest_message['text'])]

class Actiondate(Action):

    def name(self) -> Text:
        return "action_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message =f'When would you want to schedule an appointment?'
        dispatcher.utter_message(text = message)
        return [SlotSet('issue',tracker.latest_message['text'])]

class ActionBookAppSubmit(Action):

    def name(self) -> Text:
        return "action_appdate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        empid =  tracker.get_slot("employeeId")
        empid = int(empid)
        iss =  tracker.get_slot("issue")
        dte =  tracker.get_slot("date")
        #df_emp=pd.read_csv('/content/drive/MyDrive/employee_details.csv')
        output =[row for row in df_emp.iterrows() if row[1][0] == empid]
        if output:
            message_Name =f'Name: {output[0][1][1]}  {output[0][1][2]}'
            dispatcher.utter_message(text=message_Name)
        dispatcher.utter_message(text=f'Employee ID: {empid}')
        dispatcher.utter_message(text=f'Issue : {iss}')
        dispatcher.utter_message(text=f'Appointment Date : {dte}')
        dispatcher.utter_message(text=f' ')
        message = f'Shall I goahead and make an appointment with the details?'
        dispatcher.utter_message(text=message)
        return [SlotSet('date',tracker.latest_message['text'])]

class Actionbookapp(Action):

    def name(self) -> Text:
        return "action_book_app"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #df_app=pd.read_csv('/content/drive/MyDrive/app_details.csv')
        #df_emp = pd.read_csv('/content/drive/MyDrive/employee_details.csv')
        empid =  tracker.get_slot("employeeId")
        dt =  tracker.get_slot("date")
        issue_des = tracker.get_slot("issue")
        empid = int(empid)
        output =[row for row in df_app.iterrows() if row[1][0] == empid]
        if output:
            message = f'Your already have an appointment for the following date: {output[0][1][1]}' + '\n' + f'and time : {output[0][1][2]}'
            dispatcher.utter_message(text=message)
        else:
            df_app.loc[len(df_app.index)] = [empid, dt, '3:00 PM']
            df_app.to_csv('/content/drive/MyDrive/app_details.csv',index = False)
            output_emp =[row for row in df_emp.iterrows() if row[1][0] == empid]
            email=output_emp[0][1][4]
            subject="Ergonomic issue consultation appointment details"
            message=f"Hi {output_emp[0][1][1]}," + "\n" + f"Your appointment got scheduled succesfully on {dt} for ergonomic issue consultation." +"\n"+f"Issue Description: "+"\n"+f"          {issue_des}"+"\n"+f" One of our nurses will be in touch with you shortly"+"\n"+f"Thanks,"+"\n"+"\n"+f"Tyrion, chatbot powered by RASA"
            SendEmail(email,subject,message)
            message=f'Appointment got scheduled succesfully. You will get an email confirmation shortly.'
            dispatcher.utter_message(text=message)
        return []


class ActionFcTimings(Action):

    def name(self) -> Text:
        return "action_fc_timings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #df_fc=pd.read_csv('/content/drive/MyDrive/FC.csv')
        dispatcher.utter_message(text=f'The following food courts are serving now')
        for row in df_fc.iterrows():
            if row[1][1] == 'open':
                dispatcher.utter_message(text=f'{row[1][0]}    waitTime :{row[1][2]}')
        dispatcher.utter_message(text=f'Happy meals')
        return []

class ActionEatFood(Action):

    def name(self) -> Text:
        return "action_eat_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #df_ven=pd.read_csv('/content/drive/MyDrive/FC_items.csv')

        food_to_eat = tracker.get_slot("food")
        dispatcher.utter_message(text=f'The following food courts are serving {food_to_eat}')
        for row in df_ven.iterrows():
            a = row[1][2]
            a_low=a.lower()
            b_low = food_to_eat.lower()
            if a_low==b_low:
                dispatcher.utter_message(text=f'{row[1][0]}  Vendor : {row[1][1]} ')
        dispatcher.utter_message(text=f'Happy meals')
        return []

class ActionMotivate(Action):

    def name(self) -> Text:
        return "action_motivate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"I can understand. Take a break and start fresh.")
        dispatcher.utter_message(text=f"Here are some of my suggestions to refresh mind: ")
        dispatcher.utter_message(text=f"   1. Box Breathing exercise and meditate https://www.youtube.com/watch?v=tEmt1Znux58 ")
        dispatcher.utter_message(text=f"   2. Simple stretches https://societyinsurance.com/risk-management/occupational-safety/ ")
        dispatcher.utter_message(text=f"   3. Listen to Calming Music https://www.pandora.com/playlist/PL:56831869:1250724002 ")
        dispatcher.utter_message(text=f"   4. Take a Walk - A little physical activity can naturally increase endorphins leading to more energy, pain relief, and reduced stress ")
        dispatcher.utter_message(text=f"   5. Take a Break from Social Media - Taking a break from social media can help you become more in tune with your thoughts and feelings")
        return []

class ActionStressRelief(Action):

    def name(self) -> Text:
        return "action_stress_relief"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Stress is normal. You may feel down or anxious, and that’s normal too for a while. Its a concern only when it persists for more than several weeks or if it starts to interfere with your home or work life ")
        dispatcher.utter_message(text=f"We have Stress Test to analyze your stress level and examine plans to manage it. It will take less than 10 mins")
        dispatcher.utter_message(text=f"Do you wish to take a Stress Test ?")
        return []

class ActionSuggestPlans(Action):

    def name(self) -> Text:
        return "action_suggest_plans"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"ok. Managing stress is important for your mental and physical health. You can refer to the below links to know more about stress management.")
        dispatcher.utter_message(text=f"https://www.webmd.com/balance/stress-management/stress-management")
        dispatcher.utter_message(text=f"https://www.inc.com/megy-karydes/5-ways-to-motivate-yourself-increase-your-productivity.html")
        return []

class ActionStressTestQ1(Action):

    def name(self) -> Text:
        return "action_stress_test_Q1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"1. How often you have been upset because of something unexpected?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','1')]

class ActionStressTestQ2(Action):

    def name(self) -> Text:
        return "action_stress_test_Q2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"2. How often do you feel unable to control the important things in your life?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','2'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ3(Action):

    def name(self) -> Text:
        return "action_stress_test_Q3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"3. How often do you feel nervous and stressed?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','3'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ4(Action):

    def name(self) -> Text:
        return "action_stress_test_Q4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"4. How often do you feel confident about handling personal problems?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','4'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ5(Action):

    def name(self) -> Text:
        return "action_stress_test_Q5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"5. How often do you feel that things are going well for you?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','5'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ6(Action):

    def name(self) -> Text:
        return "action_stress_test_Q6"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"6. How often do you feel you are unable to cope with all the things you have to do?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','6'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ7(Action):

    def name(self) -> Text:
        return "action_stress_test_Q7"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"7. How often are you able to control things that irritate you?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','7'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ8(Action):

    def name(self) -> Text:
        return "action_stress_test_Q8"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"8. How frequently do you feel in control of your life??")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','8'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ9(Action):

    def name(self) -> Text:
        return "action_stress_test_Q9"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"9. How often you have been angry because of things outside of your control?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','9'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestQ10(Action):

    def name(self) -> Text:
        return "action_stress_test_Q10"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"10. How often do you fell calm and peaceful?")
        dispatcher.utter_message(text=f"        Never ")
        dispatcher.utter_message(text=f"        Almost Never ")
        dispatcher.utter_message(text=f"        Sometimes ")
        dispatcher.utter_message(text=f"        Fairly Often ")
        dispatcher.utter_message(text=f"        Very Often ")
        return [SlotSet('question_count','10'), SlotSet('stressValue',stress_value_temp)]

class ActionStressTestResults(Action):

    def name(self) -> Text:
        return "action_stress_test_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_ans = tracker.get_slot("test_answer")
        question_count = tracker.get_slot("question_count")
        stress_value = tracker.get_slot("stressValue")
        stress_value_temp = evaluate_stress(question_ans,question_count,stress_value)
        dispatcher.utter_message(text=f"Thank you for completing the Stress Test.")
        msg_intro = f"Hi , "+'\n'+f"Thank you for completing the Stress Test."
        message_email=f"Here are some of my suggestions to refresh mind: "+'\n'+f"   1. Box Breathing exercise and meditate  https://www.youtube.com/watch?v=tEmt1Znux58 "+ '\n'+f"   2. Simple stretches https://societyinsurance.com/risk-management/occupational-safety/ "+'\n'+f"   3. Listen to Calming Music https://www.pandora.com/playlist/PL:56831869:1250724002 "+'\n'+f"   4. Take a Walk - A little physical activity can naturally increase endorphins leading to more energy, pain relief, and reduced stress "+'\n'+f"   5. Take a Break from Social Media - Taking a break from social media can help you become more in tune with your thoughts and feelings"
        message_email_1=f"Managing stress is important for your mental and physical health. You can refer to the below links to know more about stress management."+'\n'+f"https://www.webmd.com/balance/stress-management/stress-management"+"\n"+f"https://www.inc.com/megy-karydes/5-ways-to-motivate-yourself-increase-your-productivity.html"+'\n'+f"We care your welfare and we are there to help you."+'\n'+f"Kindly contact +91 7648234873 / +91 6725462543 if you think you need assistance."
        if 0 <= stress_value_temp <= 10 :
            stress_value = 'Low'
            msg = f"Your stress level is 'Low'" +'\n'+ f'Your Low visualization indicates that you can deal with stress well and maintain a healthy work/life balance.'
            dispatcher.utter_message(text=f"Your stress level is 'Low'")
            # dispatcher.utter_message(text=f"Your Low visualization indicates that you can deal with stress well and maintain a healthy work/life balance.")
        if 15 <= stress_value_temp <= 30 :
            stress_value = 'Moderate'
            msg =f"Your stress level is 'Moderate'"+'\n'+f"Your visualization suggests you’re under pressure and that you may be experiencing symptoms typical of moderate stress."+'\n'+f"The good news is moderate stress can be addressed quite easily by making small changes that have a lasting impact."
            dispatcher.utter_message(text=f"Your stress level is 'Moderate'")
            # dispatcher.utter_message(text=f"Your visualization suggests you’re under pressure and that you may be experiencing symptoms typical of moderate stress.")
            # dispatcher.utter_message(text=f"The good news is moderate stress can be addressed quite easily by making small changes that have a lasting impact.")
        if 30 <= stress_value_temp <= 40 :
            stress_value = 'High' 
            dispatcher.utter_message(text=f"Your stress level is 'High'")
            msg = f"Your stress level is 'High'"+'\n'+f"Your visualization suggests you’re feeling overly pressured and Feeling out of control is typical of higher stress but, once you know what to do, it’s easy to regain control."+'\n'+f"The key is to recognize stress as soon as you can and make small changes that have a lasting impact."
            # dispatcher.utter_message(text=f"Your visualization suggests you’re feeling overly pressured and Feeling out of control is typical of higher stress but, once you know what to do, it’s easy to regain control.")
            # dispatcher.utter_message(text=f'The key is to recognize stress as soon as you can and make small changes that have a lasting impact.')
            #dispatcher.utter_message(text=f"Please contact us if you need to consult a company-provided Doctor")
        dispatcher.utter_message(text=f"We have emailed you the stress test results and few suggestions that may help you.")
        msg_tnk= f'Thank you, '+'\n'+'Tyrion, Chatbot powered by RASA'
        #df_emp = pd.read_csv('/content/drive/MyDrive/employee_details.csv')
        empid =  tracker.get_slot("employeeId")
        empid = int(empid)
        output_emp =[row for row in df_emp.iterrows() if row[1][0] == empid]
        email=output_emp[0][1][4]
        email_msg = msg_intro+'\n'+msg  + '\n' + message_email + '\n' + message_email_1+'\n'+'\n'+msg_tnk
        subject="Stress Test Evaluation"
        SendEmail(email,subject,email_msg)
        return [SlotSet('stressValue',stress_value)]

def evaluate_stress(question_ans,question_count,stress_value):
    if stress_value == None or isinstance(stress_value, str):
        stress_value = 0
    question_count= int(question_count)
    if question_count in [1,2,3,6,9]:
        for key in positive:
            if key == question_ans.lower():
               stress_value = stress_value + positive[key]
    else:
        for key in negative:
            if key == question_ans.lower():
               stress_value = stress_value + negative[key]       
    return stress_value

def SendEmail(toaddr,subject,message):
    fromaddr = "kr.taway@gmail.com"
    msg = MIMEMultipart()       # instance of MIMEMultipart
    msg['From'] = fromaddr      # storing the senders email address
    msg['To'] = toaddr          # storing the receivers email address
    msg['Subject'] = subject    # storing the subject
    body = message              # string to store the body of the mail
    msg.attach(MIMEText(body, 'plain'))      # attach the body with the msg instance

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()   # start TLS for security
    try:
        s.login(fromaddr, "throwaway9389")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
    except:
        print("An Error occured while sending email.")
    finally:
        s.quit()