import httpx
from typing import Tuple

JOKE_ERROR = "Error Getting Joke! Please try again Later"


async def get_jokes() -> Tuple[bool, str]:
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, timeout=10.0)
        except httpx.TimeoutException:
            return False, JOKE_ERROR

    if response.status_code != 200:
        return False, JOKE_ERROR
    try:
        joke = response.json()['joke']
    except KeyError:
        return False, JOKE_ERROR

    return True, joke
