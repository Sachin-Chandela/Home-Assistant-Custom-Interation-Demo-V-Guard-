import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)



async def fan_control(host,port,session,state,speed):
    url=f"http://{host}:{port}/api/fan/control"


    _LOGGER.debug("the data is state=%s speed=%s", state, speed)


    # if the data is in json format which i think it will be so pass it as it is
    data_dict={"state":state,"speed":speed}
    
    response=await session.post(url,json=data_dict)

    data=await response.json()
    if(data["success"]==True):
        _LOGGER.debug("api is woring correctly")

    else:
        _LOGGER.debug("api is not working correctly")


    return data


async def fan_status(host,port,session):

    url=f"http://{host}:{port}/api/fan/status"


    response=await session.get(url)
    data=await response.json()

    # returns the data which is the json

    return data





