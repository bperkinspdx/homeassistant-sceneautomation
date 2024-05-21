import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class SceneAutomationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Scene Automation", data=user_input)

        on_scene_schema = vol.Schema({
            vol.Required("tod_sensor"): cv.entity_id,
            vol.Required("scene"): cv.entity_id,
        })

        data_schema = vol.Schema({
            vol.Required("on_scenes"): vol.All(cv.ensure_list, [on_scene_schema]),
            vol.Required("off_scene"): cv.entity_id,
            vol.Required("binary_sensor"): cv.entity_id,
            vol.Optional("disable_sensor"): cv.entity_id,
            vol.Optional("enable_event"): cv.string,
            vol.Optional("disable_event"): cv.string,
            vol.Optional("rgb_light"): cv.entity_id,
            vol.Optional("enable_color", default=[0, 255, 0]): vol.All(cv.ensure_list, [cv.positive_int]),
            vol.Optional("disable_color", default=[255, 0, 0]): vol.All(cv.ensure_list, [cv.positive_int]),
            vol.Optional("already_color", default=[0, 0, 255]): vol.All(cv.ensure_list, [cv.positive_int]),
            vol.Optional("color_duration", default=5): cv.positive_int,
            vol.Optional("scene_order", default=[]): vol.All(cv.ensure_list, [cv.entity_id]),
            vol.Optional("off_delay", default=0): cv.positive_int,
            vol.Optional("brighter_event"): cv.string,
            vol.Optional("dimmer_event"): cv.string,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SceneAutomationOptionsFlowHandler(config_entry)


class SceneAutomationOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        on_scene_schema = vol.Schema({
            vol.Required("tod_sensor"): cv.entity_id,
            vol.Required("scene"): cv.entity_id,
        })

        data_schema = vol.Schema({
            vol.Required("on_scenes", default=self.config_entry.data.get("on_scenes")): vol.All(cv.ensure_list, [on_scene_schema]),
            vol.Required("off_scene", default=self.config_entry.data.get("off_scene")): cv.entity_id,
            vol.Required("binary_sensor", default=self.config_entry.data.get("binary_sensor")): cv.entity_id,
            vol.Optional("disable_sensor", default=self.config_entry.data.get("disable_sensor")): cv.entity_id,
            vol.Optional("enable_event", default=self.config_entry.data.get("enable_event")): cv.string,
            vol.Optional("disable_event", default=self.config_entry.data.get("disable_event")): cv.string,
            vol.Optional("rgb_light", default=self.config_entry.data.get("rgb_light")): cv.entity_id,
            vol.Optional("enable_color", default=self.config_entry.data.get("enable_color", [0, 255, 0])): vol.All(cv.ensure_list, [cv.positive_int]),
            vol.Optional("disable_color", default=self.config_entry.data.get("disable_color", [255, 0, 0])): vol.All(cv.ensure_list, [cv.positive_int]),
            vol.Optional("already_color", default=self.config_entry.data.get("already_color", [0, 0, 255])): vol.All(cv.ensure_list, [cv.positive_int]),
            vol.Optional("color_duration", default=self.config_entry.data.get("color_duration", 5)): cv.positive_int,
            vol.Optional("scene_order", default=self.config_entry.data.get("scene_order", [])): vol.All(cv.ensure_list, [cv.entity_id]),
            vol.Optional("off_delay", default=self.config_entry.data.get("off_delay", 0)): cv.positive_int,
            vol.Optional("brighter_event", default=self.config_entry.data.get("brighter_event")): cv.string,
            vol.Optional("dimmer_event", default=self.config_entry.data.get("dimmer_event")): cv.string,
        })

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)
