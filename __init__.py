import logging


import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


from .coordinator import FanCoordinator

from .coordinator import LightCoordinator

from .coordinator import DeviceCoordinator

from .const import DOMAIN

PLATFORMS=["fan","light"]

_LOGGER = logging.getLogger(__name__)

from .const import DEFAULT_HOST,DEFAULT_PORT

async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry):
    host=DEFAULT_HOST

    port=DEFAULT_PORT

    session=aiohttp.ClientSession()


    device_coordinator=DeviceCoordinator(hass,host,port,session)
    await device_coordinator.async_config_entry_first_refresh()
    # store all these into the hass so that in the fan.py light.py and other i can excess them

    fan_coordinator=FanCoordinator(hass,host,port,session)
    await fan_coordinator.async_config_entry_first_refresh()  #fetch the data once before setup 

    # so i think this is where if the device is off then we can't access entity

    light_coordinator=LightCoordinator(hass,host,port,session)
    await light_coordinator.async_config_entry_first_refresh()

    


    

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "device_coordinator":device_coordinator,
        "fan_coordinator": fan_coordinator,
        "light_coordinator":light_coordinator,
        "session": session,
    }


    # now in the deivce coordinator what all the devices is there i want to make its entity only
    # so where to write this logic:-  ANS   we write in the fan.py and light.py only   

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass:HomeAssistant,entry:ConfigEntry):
    # remove that platform

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["session"].close()   # <- actually closes the socket

    return unload_ok




# currently all fans talks to one api  like fan/control

# and same for the lights


# to make each separate then in backend also accepts the uuid and try to hadle each uuid state 
# differnetly



