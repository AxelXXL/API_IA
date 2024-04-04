import google.generativeai as genai
from fastapi import FastAPI, Request, Response
from fastapi import status
from PIL import Image
import uvicorn
import urllib.request
from fastapi import FastAPI, File, UploadFile, Form, Body
from typing import Annotated
from typing import Any
from config import API_KEY
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
) -> Any:
    model = genai.GenerativeModel("gemini-pro-vision")

    prompt = prompts[TypePrompt]
    
    if int(TypePrompt) == 2:
        urllib.request.urlretrieve("https://imgs.search.brave.com/_DZXu-fk-_puRV2O6fcQI1zwszKXQdoghTshRVoAECk/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTgz/NDA3MTY1L2VzL2Zv/dG8vZm9uZG8tZGUt/cGFwZWwtZGUtY29s/b3ItYmxhbmNvLmpw/Zz9zPTYxMng2MTIm/dz0wJms9MjAmYz1r/T1NYZzB2bFZiTVRX/YkxzbmdyX0ZYUlhk/TnNGVGJocEdoVkhI/UDlodnRNPQ", "Prueba.png")
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)