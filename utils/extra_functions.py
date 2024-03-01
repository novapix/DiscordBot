import httpx
from typing import Tuple

JOKE_ERROR = "Error Getting Joke"

async def get_jokes() ->Tuple[bool, str]:
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url,timeout=10.0)
        except httpx.TimeoutException:
            return False, JOKE_ERROR
    
    if response.status_code != 200:
        return False, JOKE_ERROR
    
    joke = response.json()['joke']
    return True, joke