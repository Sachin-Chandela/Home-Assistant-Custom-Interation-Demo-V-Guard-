import logging

from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

from .fan_api import fan_status
from .light_api import light_status

from .devices_api import get_all_devices



class DeviceCoordinator(DataUpdateCoordinator):
    def __init__(self,hass,host,port,session):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=15),   #fetches the state in every 15 seconds it call the fxn update_data
    
        )
    
        self.host=host
        self.port=port
        self.session=session
    
    async def _async_update_data(self):

        # state is in the form  of 

        # products=[
        #     {"product": "fan",
        #     "model": "301B",
        #     "uuid": "301B/5168185317888857",
        #     "unit": "0",
        #     "name": "FAN_1",
        #     "deviceId": "5168185317888857",
        #     "boardSerial": "5168185317888857"
        #     },
        #     {"product": "light",
        #         "model": "6001", 
        #         "uuid": "6001/3025645269080997",
        #         "unit": "0",
        #         "name": "LIGHT_1",
        #         "deviceId": "3025645269080997",
        #         "boardSerial": "3025645269080997"
        #     }
        # ]


        devices = await get_all_devices(self.session)
        return devices

class FanCoordinator(DataUpdateCoordinator):
    def __init__(self,hass,host,port,session):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=15),   #fetches the state in every 15 seconds it call the fxn update_data

        )

        self.host=host
        self.port=port
        self.session=session

    async def _async_update_data(self):
        state = await fan_status(self.host, self.port, self.session)
        return state


class LightCoordinator(DataUpdateCoordinator):
    def __init__(self,hass,host,port,session):

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=15),   #fetches the state in every 15 seconds it call the fxn update_data
        
        )
        
        self.host=host
        self.port=port
        self.session=session
        
    async def _async_update_data(self):
        state = await light_status(self.host, self.port, self.session)
        return state



