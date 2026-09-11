import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

state=False

async def light_status(host,port,session):
    url=f"http://{host}:{port}/api/light/status"

    response=await session.get(url)

    data=await response.json()

    # data will look like  {state:true}

    return data


async def light_control(host,port,session,set_state):
    url=f"http://{host}:{port}/api/light/control"

    state=set_state

    # post should look like   {state:true}
    response=await session.post(url,json={"state":state})

    data=await response.json()

    if data.get("success"):
        _LOGGER.debug("light api working correctly")
    else:
        _LOGGER.debug("light api not working correctly")
    return data


