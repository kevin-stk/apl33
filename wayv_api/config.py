import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///instance/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    WAYV_TOKEN = os.getenv('WAYV_TOKEN', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55X2lkIjoiNjY5OGZkNGFkZTFiMmEwN2QwNGM0YTlmIiwiY3VycmVudF90aW1lIjoxNzQ0MzA1MTY4NzUzLCJleHAiOjIwNTk4Mzc5Njh9.ZU2yT2Ig5rYZ1VUt2N0ReBiB_0Ro-lADCUSXN-aoPjs')
    WAYV_TEMPLATE_ID = os.getenv('WAYV_TEMPLATE_ID', '679a0ab6c8825d82fe8273ff')
    WAYV_EXECUTION_COMPANY_ID = os.getenv('WAYV_EXECUTION_COMPANY_ID', '664274977fc8ba05332d2f0c')
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'desenvolvimento-wayv-api')