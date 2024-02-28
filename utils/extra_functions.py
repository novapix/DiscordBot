import httpx


async def get_jokes() ->str:
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
    
    if response.status_code != 200:
        return "Welcome to the server"
    
    joke = response.json()['joke']
    message_to_user = f"Welcome to the server.\nHere is a Joke for you:\n{joke}"
    return message_to_user