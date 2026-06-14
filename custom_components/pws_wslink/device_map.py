"""Device mapping helpers for hub/module topology."""

import re

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    BARO_PRESSURE,
    CO,
    CO2,
    DOMAIN,
    HCHO,
    INDOOR_BATTERY,
    INDOOR_HUMIDITY,
    INDOOR_TEMP,
    LIGHTNING_DISTANCE,
    LIGHTNING_STRIKE_COUNT_DURING_1_DAY,
    LIGHTNING_STRIKE_COUNT_DURING_1_HOUR,
    LIGHTNING_STRIKE_COUNT_DURING_5_MINUTES,
    LIGHTNING_STRIKE_COUNT_DURING_30_MINUTES,
    LIGHTNING_STRIKE_COUNT_LAST_HOUR,
    LIGHTNING_STRIKE_TIME,
    MANUFACTURER,
    PM10,
    PM10_AQI,
    PM25,
    PM25_AQI,
    T5_BATTERY,
    T8_BATTERY,
    T9_BATTERY,
    T10_BATTERY,
    T11_BATTERY,
    VOC,
)

_TYPE234_CHANNEL_RE = re.compile(r"^ch([1-7])_")
_TYPE5_KEYS = {
    LIGHTNING_STRIKE_TIME,
    LIGHTNING_DISTANCE,
    LIGHTNING_STRIKE_COUNT_LAST_HOUR,
    LIGHTNING_STRIKE_COUNT_DURING_5_MINUTES,
    LIGHTNING_STRIKE_COUNT_DURING_30_MINUTES,
    LIGHTNING_STRIKE_COUNT_DURING_1_HOUR,
    LIGHTNING_STRIKE_COUNT_DURING_1_DAY,
    T5_BATTERY,
}
_TYPE6_CHANNEL_RE = re.compile(r"^t6_c([1-7])_")
_TYPE8_KEYS = {PM25, PM10, PM25_AQI, PM10_AQI, T8_BATTERY}
_TYPE9_KEYS = {HCHO, VOC, T9_BATTERY}
_TYPE10_KEYS = {CO2, T10_BATTERY}
_TYPE11_KEYS = {CO, T11_BATTERY}
_HUB_KEYS = {INDOOR_TEMP, INDOOR_HUMIDITY, INDOOR_BATTERY, BARO_PRESSURE}


def module_for_key(key: str) -> str:
    """Return logical module id for a sensor/binary_sensor key."""
    if key in _HUB_KEYS:
        return "hub"
    t234_match = _TYPE234_CHANNEL_RE.match(key)
    if t234_match:
        return f"t234c{t234_match.group(1)}"
    if key in _TYPE5_KEYS:
        return "type5"
    t6_match = _TYPE6_CHANNEL_RE.match(key)
    if t6_match:
        return f"t6c{t6_match.group(1)}"
    if key in _TYPE8_KEYS:
        return "type8"
    if key in _TYPE9_KEYS:
        return "type9"
    if key in _TYPE10_KEYS:
        return "type10"
    if key in _TYPE11_KEYS:
        return "type11"
    return "type1"


def _device_model_for_module(module: str) -> str:
    """Return model string shown in HA device page."""
    if module == "hub":
        return "Base station"
    if module.startswith("t234c"):
        return "Type 2/3/4"
    if module == "type5":
        return "Type 5"
    if module.startswith("t6c"):
        return "Type 6"
    if module == "type8":
        return "Type 8"
    if module == "type9":
        return "Type 9"
    if module == "type10":
        return "Type 10"
    if module == "type11":
        return "Type 11"
    return "Type 1"


def _device_translation_for_module(module: str) -> tuple[str, dict[str, str] | None]:
    """Return strings.json device translation key + placeholders."""
    if module == "hub":
        return "hub", None
    if module.startswith("t234c"):
        return "type234", {"channel": module[5:]}
    if module == "type5":
        return "type5", None
    if module.startswith("t6c"):
        return "type6", {"channel": module[3:]}
    if module == "type8":
        return "type8", None
    if module == "type9":
        return "type9", None
    if module == "type10":
        return "type10", None
    if module == "type11":
        return "type11", None
    return "type1", None


def device_info_for_key(config_entry: ConfigEntry, key: str) -> DeviceInfo:
    """Build DeviceInfo and localize device labels via strings.json only."""
    module = module_for_key(key)
    hub_identifier = (DOMAIN, f"{config_entry.entry_id}_hub")
    translation_key, placeholders = _device_translation_for_module(module)
    model = _device_model_for_module(module)

    if module == "hub":
        return DeviceInfo(
            identifiers={hub_identifier},
            manufacturer=MANUFACTURER,
            model=model,
            entry_type=DeviceEntryType.SERVICE,
            translation_key=translation_key,
            translation_placeholders=placeholders,
        )

    module_identifier = (DOMAIN, f"{config_entry.entry_id}_{module}")
    return DeviceInfo(
        identifiers={module_identifier},
        via_device=hub_identifier,
        manufacturer=MANUFACTURER,
        model=model,
        translation_key=translation_key,
        translation_placeholders=placeholders,
    )
