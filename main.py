import google.generativeai as genai
from fastapi import FastAPI, Request, Response
from fastapi import status
from PIL import Image
import uvicorn
import urllib.request
from fastapi import FastAPI, File, UploadFile, Form, Body
from typing import Annotated, Optional
from typing import Any
from config import API_KEY, IMG_DEFAULT
import json 
with open('url.json') as f:
    data = json.load(f)
import json
with open('promts.json') as f:
    prompts = json.load(f)


app = FastAPI()
genai.configure(api_key=API_KEY)

@app.post("/API_IA")
async def post_method(
    ID_URL,
    TypePrompt,
    response_fastapi: Response,
    promptEspec: Optional[str] = None
) -> Any:
    model = genai.GenerativeModel("gemini-pro-vision")

    prompt = prompts[TypePrompt]
    
    if promptEspec is None:
        if int(TypePrompt) == 2:
            urllib.request.urlretrieve(IMG_DEFAULT, "Prueba.png")
            img = Image.open("Prueba.png")
            response = model.generate_content([prompt, img])
            response_fastapi.status_code = status.HTTP_200_OK
            print(response.text)
            return {"message": response.text}
        elif int(TypePrompt) == 1:        
            url = data[ID_URL]
            urllib.request.urlretrieve(url, "Prueba.png")
            img = Image.open("Prueba.png")
            response = model.generate_content([prompt, img])
            response_fastapi.status_code = status.HTTP_200_OK
            return {"message": response.text}
    else:
        urllib.request.urlretrieve(IMG_DEFAULT, "Prueba.png")
        img = Image.open("Prueba.png")
        response = model.generate_content([promptEspec, img])
        response_fastapi.status_code = status.HTTP_200_OK
        print(response.text)
        return {"message": response.text}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)