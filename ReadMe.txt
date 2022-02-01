Code setup: 
	Download the code from Github repository(https://github.com/Rathi-Thiagu/Tyrion_2.0) and add to the Google drive account where the colab will be executed. 
Steps to set up the environment: 
 	Please refer to the Env_setup.pdf document 
Dataset Preparation : 
	All the data files are already present in /data folder.
	Please use any employeeID from /data/employee_details.csv for testing.Or add an entry with your correct email address details incase if you are testing chatbot's email sending feature.
Run code:
	Trained model is already present in /models. After the environmental setup we can start the chatbot by 
	
	rasa run actions & rasa shell 
conversation flow: 
	This can be referred in file Conversation flow.pdf
Email feature Demo: 
	Tyrion chatbot is capable of sending emails to users. 
	SendEmail function in actions.py does this job. However due to privacy issues from address and password were not given.
	It can be tested by giving input to 
		 fromaddr = "giveemail@gmail.com"
		 s.login(fromaddr, "givepassword")
	Also email address settings need to changed in this link https://accounts.google.com/DisplayUnlockCaptcha
	This will allow access to the code to login to the mail.
	So i have given the demo on the below video.
		https://www.youtube.com/watch?v=NaqOsrdlv0w
	Even if these details were not given the conversation flow can still be tested.Just that chat bot will give a response in the chat but will not send an email.
Notes: 
	1. The Questions for Stress test used here is taken from Cigna healthcare. 
	   The evaluation is not accurate. Developed just to showcase the feature of chatbot.
	2. Chatbot is capable of sending emails. But concerning to privacy the from mail address and password is not provided.
	   It can checked by giving those details. However this will not hinder the chatbot's conversation flow
	3. Separate actions are written for each question of stress evaluation as RASA 1.10.3 doesnot have the form filling features
	4. Chatbot was developed for company resource access and can be customized for any company.For now chatbot got developed for Infosys Ltd.
	5. Since this is company resource related, there is no open source APIs present to access data. Sample dataset was formed using csv and then accessed
	

