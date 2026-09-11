# ok so if i have used the FanENtity  in class then i need to have to decalre the feature 
# with the same name and also   use the same fxn name to turn on or off

# and how the fxn looks like i can see that in the docs of HA components fan


# and if i don't want to use any FanENtity then i class just use the Entity only



import logging
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item,
)


_LOGGER = logging.getLogger(__name__)
from .fan_api import fan_control
from .const import DOMAIN

SPEED_LIST = ["1", "2", "3", "4"]

# first set it up

async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities: AddEntitiesCallback):
    data=hass.data[DOMAIN][entry.entry_id]
    device_coordinator = data["device_coordinator"]
    fan_coordinator=data["fan_coordinator"]  #get only the fan coordinator only

    fans = [
        ESP32Fan(fan_coordinator, entry, device)
        for device in device_coordinator.data
        if device['product'] == "smartfan"
    ]

    async_add_entities(fans)


    # async_add_entities([ESP32Fan(coordinator, entry)])

# its inherting from teh CoordinatorENtity class and the FanEntity class 
# and that's why we called the super to intialize their init
class ESP32Fan(CoordinatorEntity, FanEntity):
    def __init__(self,coordinator,entry,device):
        super().__init__(coordinator)

        self.coordinator=coordinator
        self._attr_name = device["name"]
        self._attr_unique_id = f"esp32_fake_fan_{device['uuid']}"

        self._attr_supported_features=(
            FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
            | FanEntityFeature.SET_SPEED
        )


    @property
    def is_on(self)->bool:
        return bool(self.coordinator.data.get("state"))


    # we need to convert into the percentage as in the FAn entity this is only there for the speed
    @property
    def percentage(self)->int | None:
        speed=self.coordinator.data.get("speed")
        if not speed or speed not in SPEED_LIST:
            return 0

        return ordered_list_item_to_percentage(SPEED_LIST,speed)


    # this below function will only works when we have like FanEntityFeature.TURN_ON  in the supported features

    async def async_turn_on(self, percentage: int | None = None, preset_mode: str | None = None, **kwargs) -> None:
            # Use requested percentage if the user set one while turning on,
            # otherwise fall back to whatever speed was last known
            if percentage:
                speed = percentage_to_ordered_list_item(SPEED_LIST, percentage)
            else:
                speed = self.coordinator.data.get("speed", SPEED_LIST[0])
            await fan_control(self.coordinator.host, self.coordinator.port, self.coordinator.session, True, speed)
            self.coordinator.data["state"] = True
            self.coordinator.data["speed"] = speed
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
            # Keep the last known speed, just flip state off
            speed = self.coordinator.data.get("speed", SPEED_LIST[0])
            await fan_control(self.coordinator.host, self.coordinator.port, self.coordinator.session, False, speed)
            self.coordinator.data["state"] = False
            await self.coordinator.async_request_refresh()

    async def async_set_percentage(self, percentage: int) -> None:

            if not self.coordinator.data.get("state"):
                 _LOGGER.debug("Device is OFF can't set the speed")
                 return
            if percentage == 0:
                await self.async_turn_off()
                return
            speed = percentage_to_ordered_list_item(SPEED_LIST, percentage)
            # Keep current on/off state, just change speed
            state = self.coordinator.data.get("state", True)
            await fan_control(self.coordinator.host, self.coordinator.port, self.coordinator.session, state, speed)
            self.coordinator.data["state"] = state
            self.coordinator.data["speed"] = speed
            await self.coordinator.async_request_refresh()


