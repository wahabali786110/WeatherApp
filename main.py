from fastapi import FastAPI,Request,Form
import os
from dotenv import load_dotenv
import httpx
from fastapi.templating import Jinja2Templates

load_dotenv()

API_KEY=os.getenv("WEATHER_API_KEY")

templates=Jinja2Templates(directory="templates")

app=FastAPI()

@app.get('/')
async def home(request:Request):
    return templates.TemplateResponse(request=request,name="index.html",context={"weather_data":None})

@app.post("/weather/")
async def get_api( request:Request ,city:str=Form(...)):
    base_url="http://api.weatherapi.com/v1/current.json"
    params={
        "key":API_KEY,
        "q":city
    }

    async with httpx.AsyncClient() as client:
        response=await client.get(base_url,params=params)

        if response.status_code==200:
            data=response.json()
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={"weather_data":data,"error":None}
            )
        else:
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={"weather_data":None,"error":"Error in fetching data"}
            )