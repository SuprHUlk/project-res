from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from pypdf import PdfReader
import io
import re
from google import genai
import json

from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_3xdSex_Pw3ktxhPmBfdQWeiakqTaQRhuwenvnFR3CBKJwiqecNDRLsyccceAqoU7GZewM6")
client = genai.Client(api_key="AIzaSyBnoXU_RhSg7l1-mFc7qLMyAwGNnId3q8U")
index_name = "developer-quickstart-py"

if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        dimension=2048,
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )

app = FastAPI()
host = "https://developer-quickstart-py-nb1cii0.svc.aped-4627-b74a.pinecone.io"

index = pc.Index(host=host)
user_id = '32'

@app.post("/createEmbedding")
async def create_embedding(file: UploadFile):
    contents = await file.read()
    pdf_stream = io.BytesIO(contents)
    try:
        reader = PdfReader(pdf_stream)
    except Exception as e:
        return {"error": f"Failed to read PDF: {str(e)}"}
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    
    sentences = re.split(r'(?<=[.!?]) +', extracted_text)

    pre_prompt = '''
            You will be provided with the text extracted from a resume in the following format
            INPUT_FORMAT:
            {
                [
                    "sentence 1",
                    "sentence 2"
                ]
            }

            add some keyword around every sentence for better embedding in an vector database
            
            NOTE: 
                you can even split the sentences further

            EXAMPLE:
                GIVEN:
                    "computelib May2025 Noida"
                RESULT:
                    "company computelib May2025 location Noida"

            Give response in following json format only
            OUTPUT_FORMAT:
            {
                [
                    "Modified sentence 1",
                    "Modified sentence 2",
                ]
            }

    '''

    post_prompt = f'''
        {pre_prompt}
        INPUT 
        {json.dumps(sentences, ensure_ascii=False)}
    '''
    # print(post_prompt)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents= post_prompt
    )

    # records = []

    # for idx, c in enumerate(response):
    #     if len(text) > 350:
    #         records.append(
    #             {
    #                 "_id": f"u{user_id}:c{idx}",
    #                 "chunk_text": text,
    #                 "user_id": user_id
    #             }
    #         )
    #         text = ""
    #     text += c
    
    # records.append(
    #     {
    #         "_id": f"u{user_id}:c{len(words)}",
    #         "chunk_text": text,
    #         "user_id": user_id
    #     }
    # )
    
    # index.upsert_records("res", records)

    try:
        text_response = response.text.strip()
        text_response = re.sub(r"^```(json)?", "", text_response.strip())
        text_response = re.sub(r"```$", "", text_response.strip())
        print(text_response)
        modified = json.loads(text_response)

        records = []

        for idx, sen in enumerate(modified):
            records.append(
                {
                    "_id": f"u{user_id}:c{idx}",
                    "chunk_text": sen,
                    "user_id": user_id
                }
            )
        
        index.upsert_records("res", records)
    except Exception as e:
        return {"error": f"Failed to parse Gemini response: {str(e)}"}

    # return extracted_text
    return { "len": modified }

@app.get("/test")
async def get_res():
    
    res = index.search(
        namespace="res",
        query={
            "inputs": {"text": "what's the name of the company?"},
            "top_k": 3,
            "filter": {
                "user_id": user_id,
            }
        },
        fields=["chunk_text"]
    )

    print(res)

    return { "res": "hi" }

@app.get("/health")
async def read_root():
    return {"Hello": "World"}