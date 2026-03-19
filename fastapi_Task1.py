from fastapi import FastAPI
from enum import Enum 
app = FastAPI()
 
class AvailableCuisines(str,Enum):
    indian = "indian"
    american = "american"
    italian = "italian"
food_Items = {
    'indian': ['Samosa','Dosa'],
    'american':['Hot dog','Burger'],
    'italian':['Pasta','pizza']
}

@app.get("/get_items/{cuisine}")
async def get_items(cuisine: AvailableCuisines):
    return food_Items.get(cuisine)