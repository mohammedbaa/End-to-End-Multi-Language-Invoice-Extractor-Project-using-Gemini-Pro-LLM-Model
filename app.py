from dotenv import load_dotenv
load_dotenv() ## Load all the enviroment variables from .env


import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini pro vision 
model=genai.GenerativeModel("models/gemini-2.5-flash")


def get_gemini_response(system_prompt, image_parts, user_prompt):
    response = model.generate_content([system_prompt, image_parts, user_prompt])
    return response.text

# def get_gemini_response(input,image,prompt):
#     response=model.generate_content([input,image[0],prompt])
#     return response.text

def input_image_details(uploded_file):
    if uploded_file is not None:
        ## Read the file into bytes
        bytes_data=uploded_file.getvalue()

        image_parts={
            "mime_type":uploded_file.type,
            "data":bytes_data
        }

        return image_parts
    else:
        raise FileNotFoundError("No file uploded")




## initialize our streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input Prompt: ",key="input")
uploded_file=st.file_uploader("Choose an image of the invoice......",type=["jpg","jpeg","png"])


image=""
if uploded_file is not None:
    image=Image.open(uploded_file)
    st.image(image,caption="Uploded Image.",use_container_width =True)



submit=st.button("Tell me about the invoice")

input_prompt="""
you are an expert in understanding invoices . we will upload a a image as invoice 
and you will have to answer any qustions based on the uploded invoice image
"""

# if submit button is clicked 
if submit:
    image_data=input_image_details(uploded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)