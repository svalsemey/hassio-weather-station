"""Sensor entities for the Weather Station integration for old endpoint."""

from typing import cast

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    DEGREE,
    PERCENTAGE,
    UV_INDEX,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfVolumetricFlux,
)

from .const import (
    BARO_PRESSURE,
    CHILL_INDEX,
    DEW_POINT,
    HEAT_INDEX,
    HUMIDITY,
    INDOOR_HUMIDITY,
    INDOOR_TEMP,
    OUTSIDE_HUMIDITY,
    OUTSIDE_TEMP,
    RAIN_RATE,
    RAINFALL_DAILY,
    SOLAR_RADIATION,
    T234_HUMIDITY_KEYS,
    T234_TEMP_KEYS,
    TEMPERATURE,
    UV,
    WIND_AZIMUTH,
    WIND_DIR,
    WIND_GUST,
    WIND_SPEED,
    UnitOfDir,
)
from .helpers import wind_dir_to_text
from .sensors_common import WeatherSensorEntityDescription


def _temp_desc(
    key: str,
    unit: UnitOfTemperature,
    *,
    icon: str = "mdi:thermometer",
) -> WeatherSensorEntityDescription:
    return WeatherSensorEntityDescription(
        key=key,
        native_unit_of_measurement=unit,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon=icon,
        translation_key=TEMPERATURE,
        value_fn=lambda data: cast("float", data),
    )


def _humidity_desc(
    key: str,
    *,
    icon: str = "mdi:water-percent",
) -> WeatherSensorEntityDescription:
    return WeatherSensorEntityDescription(
        key=key,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.HUMIDITY,
        icon=icon,
        translation_key=HUMIDITY,
        value_fn=lambda data: cast("int", data),
    )


_CHANNELS_PWS = tuple(zip(T234_TEMP_KEYS, T234_HUMIDITY_KEYS, strict=False))


def _channel_descriptions_pws() -> tuple[WeatherSensorEntityDescription, ...]:
    out: list[WeatherSensorEntityDescription] = []
    for temp_key, humidity_key in _CHANNELS_PWS:
        out.append(_temp_desc(temp_key, UnitOfTemperature.FAHRENHEIT))
        out.append(_humidity_desc(humidity_key))
    return tuple(out)


SENSOR_TYPES_PWS: tuple[WeatherSensorEntityDescription, ...] = (
    _temp_desc(INDOOR_TEMP, UnitOfTemperature.FAHRENHEIT),
    _humidity_desc(INDOOR_HUMIDITY),
    _temp_desc(OUTSIDE_TEMP, UnitOfTemperature.FAHRENHEIT),
    _humidity_desc(OUTSIDE_HUMIDITY, icon="mdi:cloud-percent"),
    WeatherSensorEntityDescription(
        key=DEW_POINT,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-lines",
        device_class=SensorDeviceClass.TEMPERATURE,
        translation_key=DEW_POINT,
        value_fn=lambda data: cast("float", data),
    ),
    WeatherSensorEntityDescription(
        key=BARO_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.INHG,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        suggested_unit_of_measurement=UnitOfPressure.HPA,
        translation_key=BARO_PRESSURE,
        value_fn=lambda data: cast("float", data),
    ),
    WeatherSensorEntityDescription(
        key=WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.WIND_SPEED,
        suggested_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        icon="mdi:weather-windy",
        translation_key=WIND_SPEED,
        value_fn=lambda data: cast("int", data),
    ),
    WeatherSensorEntityDescription(
        key=WIND_GUST,
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.WIND_SPEED,
        suggested_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        icon="mdi:windsock",
        translation_key=WIND_GUST,
        value_fn=lambda data: cast("float", data),
    ),
    WeatherSensorEntityDescription(
        key=WIND_DIR,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT_ANGLE,
        device_class=SensorDeviceClass.WIND_DIRECTION,
        suggested_display_precision=None,
        icon="mdi:sign-direction",
        translation_key=WIND_DIR,
        value_fn=lambda data: cast("int", data),
    ),
    WeatherSensorEntityDescription(
        key=WIND_AZIMUTH,
        icon="mdi:sign-direction",
        value_fn=lambda data: cast("str", wind_dir_to_text(data)),
        device_class=SensorDeviceClass.ENUM,
        options=list(UnitOfDir),
        translation_key=WIND_AZIMUTH,
    ),
    WeatherSensorEntityDescription(
        key=RAIN_RATE,
        native_unit_of_measurement=UnitOfVolumetricFlux.INCHES_PER_HOUR,
        device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_unit_of_measurement=UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR,
        suggested_display_precision=2,
        icon="mdi:weather-pouring",
        translation_key=RAIN_RATE,
        value_fn=lambda data: cast("float", data),
    ),
    WeatherSensorEntityDescription(
        key=RAINFALL_DAILY,
        native_unit_of_measurement=UnitOfPrecipitationDepth.INCHES,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PRECIPITATION,
        suggested_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        suggested_display_precision=2,
        icon="mdi:weather-pouring",
        translation_key=RAINFALL_DAILY,
        value_fn=lambda data: cast("float", data),
    ),
    WeatherSensorEntityDescription(
        key=SOLAR_RADIATION,
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.IRRADIANCE,
        icon="mdi:weather-sunny",
        translation_key=SOLAR_RADIATION,
        value_fn=lambda data: cast("float", data),
    ),
    WeatherSensorEntityDescription(
        key=UV,
        name=UV,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UV_INDEX,
        icon="mdi:sunglasses",
        translation_key=UV,
        value_fn=lambda data: cast("float", data),
    ),
    *_channel_descriptions_pws(),
    WeatherSensorEntityDescription(
        key=HEAT_INDEX,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        icon="mdi:thermometer",
        translation_key=HEAT_INDEX,
        value_fn=lambda data: cast("int", data),
    ),
    WeatherSensorEntityDescription(
        key=CHILL_INDEX,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_unit_of_measurement=UnitOfTemperature.CELSIUS,
        suggested_display_precision=1,
        icon="mdi:thermometer",
        translation_key=CHILL_INDEX,
        value_fn=lambda data: cast("int", data),
    ),
)
