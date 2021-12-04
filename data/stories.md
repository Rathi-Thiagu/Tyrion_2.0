## contact_emergency
* emergency
  - utter_emergency
* goodbye
  - utter_goodbye 

## company_news
* company_news
  - utter_company_news
* goodbye
  - utter_goodbye 

## raise_complaints
* raise_complaints
  - action_raise_complaints
* employeeId
  - slot{"employeeId":"661577"}
  - utter_ask_complaintType
* detect_complaintType
  - slot{"complaintType":"Individual Grievances"}
  - action_ask_complaint
* complaint_description
  - slot{"complaint_description":"Description: I have this problem"}
  - action_ask_register 
> check_raise_complaints 

## raise_complaints_affirm 1
> check_raise_complaints
* affirm 
  - action_register_complaint
  - utter_askhelp
* deny
  - utter_goodbye   

## raise_complaints_affirm 2
> check_raise_complaints
* affirm 
  - action_register_complaint
  - utter_askhelp
* affirm
  - utter_happy

## raise_complaints_deny 1
> check_raise_complaints
* deny
    - utter_askhelp
* affirm
  - utter_happy

## raise_complaints_deny 2
> check_raise_complaints
* deny
    - utter_askhelp
* deny
  - utter_goodbye

## company_products 1
* company_products
  - utter_company_products 
  - utter_askhelp
* goodbye
  - utter_goodbye 

## company_products 2
* company_products
  - utter_company_products 
  - utter_askhelp
* deny
  - utter_goodbye   

## company_products 3
* company_products
  - utter_company_products 
  - utter_askhelp
* affirm
  - utter_happy
  
## stress 1
* detect_stress_frustration_anxiety
  - action_stress_relief
> check_stress_level

## stress 1 deny 
> check_stress_level
* deny 
  - action_suggest_plans
  - utter_askhelp
* goodbye
  - utter_goodbye

## stress 1 deny 1
> check_stress_level
* deny 
  - action_suggest_plans
  - utter_askhelp
* deny
  - utter_goodbye

## stress 1 deny 2
> check_stress_level
* deny 
  - action_suggest_plans
  - utter_askhelp
* affirm
  - utter_happy

## stress 1 affirm 1
> check_stress_level
* affirm
  - action_raise_complaints
* employeeId
  - action_stress_test_Q1
* StressTestanswer
  - action_stress_test_Q2
* StressTestanswer
  - action_stress_test_Q3
* StressTestanswer
  - action_stress_test_Q4
* StressTestanswer
  - action_stress_test_Q5
* StressTestanswer
  - action_stress_test_Q6
* StressTestanswer
  - action_stress_test_Q7
* StressTestanswer
  - action_stress_test_Q8
* StressTestanswer
  - action_stress_test_Q9
* StressTestanswer
  - action_stress_test_Q10
* StressTestanswer
  - action_stress_test_results
  - utter_did_that_help
* goodbye
  - utter_goodbye 

## stress 1 affirm 2
> check_stress_level
* affirm
  - action_stress_test_Q1
* StressTestanswer
  - action_stress_test_Q2
* StressTestanswer
  - action_stress_test_Q3
* StressTestanswer
  - action_stress_test_Q4
* StressTestanswer
  - action_stress_test_Q5
* StressTestanswer
  - action_stress_test_Q6
* StressTestanswer
  - action_stress_test_Q7
* StressTestanswer
  - action_stress_test_Q8
* StressTestanswer
  - action_stress_test_Q9
* StressTestanswer
  - action_stress_test_Q10
* StressTestanswer
  - action_stress_test_results
  - utter_did_that_help
* affirm
  - utter_askhelp
* goodbye
  - utter_goodbye

## motivate 1
* detect_exhaustion_unproductive
  - action_motivate
  - utter_did_that_help
* goodbye
  - utter_goodbye

## motivate 2
* detect_exhaustion_unproductive
  - action_motivate
  - utter_did_that_help
* affirm
  - utter_askhelp
* goodbye
  - utter_goodbye

## motivate 3
* detect_exhaustion_unproductive
  - action_motivate
  - utter_did_that_help
* affirm
  - utter_askhelp
* deny
  - utter_goodbye

## motivate 4
* detect_exhaustion_unproductive
  - action_motivate
  - utter_did_that_help
* deny
  - utter_denybye
* goodbye
  - utter_goodbye

## food_court 1
* food_court 
  - utter_food_court
* food_court_timings
  - action_fc_timings
* eat_food
  - action_eat_food

## eat_food 1
* greet
  - utter_greet
* mood_great
  - utter_happy
* eat_food
  - action_eat_food

## food_court 2
* greet
  - utter_greet
* mood_great
  - utter_happy
* food_court 
  - utter_food_court
* food_court_timings
  - action_fc_timings
* affirm
  - utter_askhelp

## ergonomics 1
* ergonomics
  - utter_ergonomics
* ergonomics_assessment
  - utter_ergonomics_assessment
  - action_ergonomics_assessment
* affirm
  - utter_happy

## ergonomics 2
* ergonomics
  - utter_ergonomics
* ergonomics_selfhelp
  - utter_ergonomics_selfhelp
  - utter_askhelp
* affirm
  - utter_happy

## ergonomics_assessment 1
* ergonomics_assessment
  - utter_ergonomics_assessment
  - action_ergonomics_assessment
* affirm
  - utter_happy

## ergonomics_assessment 2
* ergonomics_assessment
  - utter_ergonomics_assessment
  - action_ergonomics_assessment
  - utter_askhelp
* affirm
  - utter_happy

## ergonomics_selfhelp 2
* ergonomics_selfhelp
  - utter_ergonomics_selfhelp
  - utter_askhelp
* goodbye
  - utter_goodbye

## ergonomics_reportissue 1
* ergonomics_issue
  - utter_ergonomics_issue
* affirm
  - utter_employeeId
* employeeId
  - slot{"employeeId":"661577"}
  - action_describe_issue
* describe_issue
  - slot{"issue":"I have backpain"}
  - action_date
* appdate
  - slot{"date":"Dec 25 , 2021"}
  - action_appdate
> check_feedback_details

## affirm path 1
> check_feedback_details
* affirm
  - action_book_app

## deny path 1
> check_feedback_details
*deny
  - utter_awareness

## ergonomics_reportissue 2
* greet
  - utter_greet
* mood_great
  - utter_happy
* ergonomics_issue
  - utter_ergonomics_issue
* affirm
  - utter_employeeId
* employeeId
  - slot{"employeeId":"661577"}
  - action_describe_issue
* describe_issue
  - slot{"issue":"I have backpain"}
  - action_date
* appdate
  - slot{"date":"Dec 25 , 2021"}
  - action_appdate
> check_feedback_details

## affirm path 1
> check_ergonomics_details
* affirm
  - action_book_app

## deny path 1
> check_ergonomics_details
*deny
  - utter_awareness

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_denybye
  - utter_askhelp

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## feedback happy 1
* greet
  - utter_greet
* mood_great
  - utter_happy
* feedbackWish
  - utter_feedbackWish
* goodbye
  - utter_goodbye

## feedback sad 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy
* feedbackWish
  - utter_feedbackWish
* deny
  - utter_denybye
  - utter_askhelp

## small talk sad 
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy
* smalltalk 
  - utter_smalltalk
  - utter_askhelp

## small talk happy 
* greet
  - utter_greet
* mood_great
  - utter_happy
* smalltalk 
  - utter_smalltalk
  - utter_askhelp
  
## cannot handle 
* greet 
  - utter_greet 
* out_of_scope
  - utter_out_of_scope
  - utter_askhelp