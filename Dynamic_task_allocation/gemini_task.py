from langchain_core.output_parsers import JsonOutputParser, format_instructions
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv
import os
from dummy_data import training_data_gemini
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")


class ClassificationModel(BaseModel):
    text: str = Field(description="The input given by the user")
    classification: str = Field(description="The classification of the log, should follow the rules given")

parser = JsonOutputParser(pydantic_object=ClassificationModel)

prompt = PromptTemplate(
    template='''The shift log of each worker working in a coal mine is given. You need to classify the shift log based on the examples given as training_data = {training_data}. The response should either tell an issue, or tell there was No issue/Irrelevant depending on the context. Here is the Log data: {log_data}. {format_instruction}''',
    input_variables=["training_data", "log_data"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)


llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
classification_model = prompt | llm | parser

log_data_arr = [
    # Equipment Issue
    "The drill bit broke during operation, needs replacement.",
    
    # Delay Issue
    "Work delayed due to heavy fog in the morning.",
    
    # Safety Issue
    "A worker slipped on wet ground, no major injury.",
    
    # Operational Issue
    "Power outage affected all operations for 20 minutes.",
    
    # Resource Issue
    "Running low on drilling fluids, need resupply soon.",
    
    # Human Error
    "A worker accidentally damaged the equipment during handling.",
    
    # Positive Log
    "All machines are operating smoothly, no issues reported."
]

for log_data in log_data_arr:
    res = classification_model.invoke(
        {
            "log_data": log_data,
            "training_data": training_data_gemini
        }
    )

    print(res)