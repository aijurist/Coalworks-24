from langchain_core.output_parsers import JsonOutputParser, format_instructions
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAI
from worker_log import log_data

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
training_data_gemini = [
    # No Issue/Positive Logs
    ("No issues reported", "No Issue"),
    ("Routine inspection completed successfully", "No Issue"),
    ("All operations running smoothly", "No Issue"),
    ("Team meeting held, no concerns raised", "No Issue"),
    ("Completed the task ahead of schedule", "No Issue"),
    ("Shift change executed without issues", "No Issue"),
    ("Weekly safety drill conducted successfully", "No Issue"),
    ("Team morale is high; no problems to report", "No Issue"),
    ("All safety protocols followed during shift", "No Issue"),
    ("Production targets met without any issues", "No Issue"),

    # Delay Issues
    ("Minor delay in shovel operation due to soil conditions", "Delay"),
    ("Overburden removal delayed due to heavy rainfall", "Delay"),
    ("Material supply delayed by traffic congestion", "Delay"),
    ("Work delayed due to unforeseen circumstances", "Delay"),
    ("Operational delay in loading due to equipment issues", "Delay"),
    ("Shift start delayed due to foggy conditions", "Delay"),
    ("Waiting for replacement parts caused a delay in work", "Delay"),
    ("Delay in drilling operation due to hard rock formation", "Delay"),
    ("Power outage delayed the start of the operation", "Delay"),
    ("Loading operation delayed due to congestion at the site", "Delay"),

    # Equipment Issues
    ("Drill malfunction during operation", "Equipment Issue"),
    ("Blasting equipment failed to ignite, causing delays", "Equipment Issue"),
    ("Drill performance issue affecting work speed", "Equipment Issue"),
    ("Unexpected machinery breakdown during excavation", "Equipment Issue"),
    ("Faulty conveyor belt causing material flow stoppage", "Equipment Issue"),
    ("JCB making unusual noises, needs inspection", "Equipment Issue"),
    ("Water leaking from the roof of the JCB cabin", "Equipment Issue"),
    ("Truck brake is loose, requires immediate attention", "Equipment Issue"),
    ("Flat tire on truck causing transport delays", "Equipment Issue"),
    ("Bulldozer hydraulic system failure", "Equipment Issue"),
    ("Loader bucket malfunctioned during operation", "Equipment Issue"),
    ("Excavator arm stuck in mid-position", "Equipment Issue"),
    ("Fuel pump on generator malfunctioned", "Equipment Issue"),
    ("Conveyor belt motor overheated", "Equipment Issue"),
    ("Crane cable showing signs of wear, needs replacement", "Equipment Issue"),

    # Maintenance Issues
    ("Routine maintenance completed", "Maintenance"),
    ("Scheduling conflict in maintenance work", "Maintenance"),
    ("Delayed maintenance work due to resource unavailability", "Maintenance"),
    ("Maintenance team understaffed, causing delays", "Maintenance"),
    ("Emergency maintenance required for conveyor belt", "Maintenance"),
    ("Planned maintenance of drilling equipment postponed", "Maintenance"),
    ("Maintenance work on truck fleet started late", "Maintenance"),
    ("Maintenance team waiting for spare parts", "Maintenance"),
    ("Maintenance inspection revealed minor wear and tear", "Maintenance"),
    ("Shift maintenance completed with no major issues", "Maintenance"),

    # Operational Issues
    ("Power outage affecting all operations", "Operational Issue"),
    ("Supervisor is late by 12 hours", "Operational Issue"),
    ("Miscommunication between teams causing workflow issues", "Operational Issue"),
    ("System outage impacting operation tracking", "Operational Issue"),
    ("Unscheduled safety drill affecting productivity", "Operational Issue"),
    ("Change in shift schedule causing confusion", "Operational Issue"),
    ("Operational efficiency reduced due to lack of coordination", "Operational Issue"),
    ("Unexpected change in work orders caused delays", "Operational Issue"),
    ("Safety drill interrupted the ongoing work", "Operational Issue"),
    ("Data entry error led to incorrect production reporting", "Operational Issue"),

    # Resource Issues
    ("Inadequate stock of essential supplies", "Resource Issue"),
    ("Shortage of critical resources affecting operations", "Resource Issue"),
    ("Insufficient fuel for machinery", "Resource Issue"),
    ("Delay in receiving materials from supplier", "Resource Issue"),
    ("Water supply issues affecting cooling systems", "Resource Issue"),
    ("Low inventory of safety gear", "Resource Issue"),
    ("Fuel delivery delayed by weather conditions", "Resource Issue"),
    ("Lack of spare parts impacting maintenance schedule", "Resource Issue"),
    ("Shortage of lubricants for machinery", "Resource Issue"),
    ("Delay in arrival of explosives for blasting", "Resource Issue"),

    # Human Error Issues
    ("Employee absence causing delays", "Human Error"),
    ("Mistake in task execution leading to rework", "Human Error"),
    ("Improper handling of equipment leading to damage", "Human Error"),
    ("Mislabeling of materials causing operational confusion", "Human Error"),
    ("Failure to follow safety protocol during blasting", "Human Error"),
    ("Incorrect drill bit selection slowed progress", "Human Error"),
    ("Late arrival of workers impacted productivity", "Human Error"),
    ("Overfilling of dump truck caused spillage", "Human Error"),
    ("Incomplete documentation caused delays in task allocation", "Human Error"),
    ("Miscommunication led to improper tool usage", "Human Error"),

    # Safety Issues
    ("Safety protocol breach identified", "Safety Issue"),
    ("Safety hazard identified in the workplace", "Safety Issue"),
    ("Incident involving minor injury reported", "Safety Issue"),
    ("Unsafe working conditions due to poor lighting", "Safety Issue"),
    ("Overhead structure damage posing a safety risk", "Safety Issue"),
    ("Fire safety equipment not functional", "Safety Issue"),
    ("Blocked emergency exit found during inspection", "Safety Issue"),
    ("Hazardous materials not stored properly", "Safety Issue"),
    ("Safety inspection revealed potential risks", "Safety Issue"),
    ("Loose wiring identified as a safety hazard", "Safety Issue"),

    # Irrelevant/Unrelated Logs
    ("Discussion about weekend plans", "Irrelevant"),
    ("Weather is sunny, no issues expected", "Irrelevant"),
    ("Team discussing last night's football match", "Irrelevant"),
    ("Personal conversation about family matters", "Irrelevant"),
    ("Employee requesting a leave of absence", "Irrelevant"),
    ("Lunch break started late", "Irrelevant"),
    ("Request for additional chairs in the break room", "Irrelevant"),
    ("Talking about new office decorations", "Irrelevant"),
    ("Discussion about upcoming holidays", "Irrelevant"),
    ("Casual chat about new restaurant in town", "Irrelevant"),
    ("Team planning a social event after work", "Irrelevant"),
    ("Discussion about company-wide news", "Irrelevant"),
]


class ClassificationModel(BaseModel):
    text: str = Field(description="The input given by the user")
    classification: str = Field(description="The classification of the log, should follow the rules given")

parser = JsonOutputParser(pydantic_object=ClassificationModel)

prompt = PromptTemplate(
    template='''The shift log of each worker working in a coal mine is given. You need to classify the 
    shift log based on the examples given as training_data = {training_data}. The response should either tell an issue, 
    or tell there was No issue/Irrelevant depending on the context. Here is the Log data: {log_data}. {format_instruction}''',
    input_variables=["training_data", "log_data"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)


llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
classification_model = prompt | llm | parser

# log_data_arr = [
#     # Equipment Issue
#     "The drill bit broke during operation, needs replacement.",

#     # Delay Issue
#     "Work delayed due to heavy fog in the morning.",
    
#     # Safety Issue
#     "A worker slipped on wet ground, no major injury.",
    
#     # Operational Issue
#     "Power outage affected all operations for 20 minutes.",
    
#     # Resource Issue
#     "Running low on drilling fluids, need resupply soon.",
    
#     # Human Error
#     "A worker accidentally damaged the equipment during handling.",
    
#     # Positive Log
#     "All machines are operating smoothly, no issues reported."
# ]
# for log_id, log_info in log_data.items():
#     log_details = log_info["log_details"]
#     res = classification_model.invoke(
#         {
#             "log_data": log_details,
#             "training_data": training_data_gemini
#         }
#     )

#     print(res)