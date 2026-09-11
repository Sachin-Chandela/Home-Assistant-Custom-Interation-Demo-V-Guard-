# make the light UI

import logging
from homeassistant.components.light import (LightEntity,ColorMode,)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


_LOGGER = logging.getLogger(__name__)

from .light_api import light_control

from .const import DOMAIN

async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities: AddEntitiesCallback):
    # try to get the coordinator  and it is in the hass

    data=hass.data[DOMAIN][entry.entry_id]
    device_coordinator = data["device_coordinator"]

    light_coordinator=data["light_coordinator"]  #get only the light coordinator

    lights=[
        ESP32Light(light_coordinator,entry,device)
        for device in device_coordinator.data
        if device['product']== "light"
    ]

    async_add_entities(lights)

    # async_add_entities(ESP32Light(coordinator,entry))


class ESP32Light(CoordinatorEntity,LightEntity):

    def __init__(self,coordinator,entry,device):
        super().__init__(coordinator)

        self.coordinator=coordinator
        self._attr_name = device['name']
        self._attr_unique_id = f"esp32_fake_light_{device['uuid']}"

        self._attr_supported_color_modes = {ColorMode.ONOFF}
        self._attr_color_mode = ColorMode.ONOFF



    @property
    def is_on(self)->bool:
        return self.coordinator.data.get("state")

    async def async_turn_on(self, **kwargs) -> None:
        await light_control(
            self.coordinator.host,
            self.coordinator.port,
            self.coordinator.session,
            True
        )
        self.coordinator.data['state']=True
        await self.coordinator.async_request_refresh()


    async def async_turn_off(self,**kwargs)->None:

        await light_control(
                    self.coordinator.host,
                    self.coordinator.port,
                    self.coordinator.session,
                    False
                )
        # this is just the post so to check the backend status we need to call the light status and which is in the corrrdinator
        # that's why we calls hte async_request_refresh()

        self.coordinator.data['state']=False
        # its too not required as the coordinator will update the state
        await self.coordinator.async_request_refresh()


    


