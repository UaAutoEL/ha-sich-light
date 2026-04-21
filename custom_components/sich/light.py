import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    LightEntity, ATTR_BRIGHTNESS, COLOR_MODE_BRIGHTNESS
)
from homeassistant.const import CONF_HOST, CONF_NAME

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME, default="Лампа Sich"): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    host = config[CONF_HOST]
    name = config[CONF_NAME]
    add_entities([SichLight(name, host)], True)

class SichLight(LightEntity):
    def __init__(self, name, host):
        self._name = name
        self._host = host
        self._state = False
        self._brightness = 255

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def brightness(self):
        return self._brightness

    @property
    def supported_color_modes(self):
        return {COLOR_MODE_BRIGHTNESS}

    @property
    def color_mode(self):
        return COLOR_MODE_BRIGHTNESS

    def turn_on(self, **kwargs):
        self._state = True
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            
        # Команда на увімкнення (T=1), яскравість (A=...) та теплий білий колір (R=255&G=214&B=170)
        url = f"http://{self._host}/win&T=1&A={self._brightness}&R=255&G=214&B=170"
        try:
            requests.get(url, timeout=3)
        except Exception as e:
            _LOGGER.error("Помилка підключення до Sich: %s", e)

    def turn_off(self, **kwargs):
        self._state = False
        url = f"http://{self._host}/win&T=0"
        try:
            requests.get(url, timeout=3)
        except Exception as e:
            _LOGGER.error("Помилка вимкнення Sich: %s", e)

    def update(self):
        pass