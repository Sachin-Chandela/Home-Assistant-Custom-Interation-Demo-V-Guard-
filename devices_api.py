
import aiohttp

from .const import TOKEN

async def get_all_devices(session):
    url="your url to get the get the user all devices"

    headers={
        "Authorization":f"{TOKEN}",
        "platform":"3",
        "Content-Type":"application/json",
        "Accept-Encoding":"*"
    }


    try:
        response=await session.get(url,headers=headers)

        json_data = await response.json()
            
            # 2. Extract strictly the products array (using .get() to prevent crashes)
        products = json_data.get("data", {}).get("nous", {}).get("products", [])
            
        return products

    except aiohttp.ClientError as e:
        print(f"Network error: {e}")
        return []


    





