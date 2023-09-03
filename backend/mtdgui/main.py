from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union

from routers import sim
from controllers import * 

app = FastAPI()

app.include_router(sim.router)

app.add_middleware(
    CORSMiddleware,    
    allow_origins= "http://localhost:5173",    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

class Item(BaseModel):
    name: str
    age: float
    is_TrueMan: Union[bool, None]=None

@app.post("/update_item/")
def update_item(item: Item):
    item.age += 10
    print(item)
    return {'item':item}