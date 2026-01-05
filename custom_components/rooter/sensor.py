"""Sensor entities for ROOTer."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    SIGNAL_STRENGTH_DECIBELS,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RooterDataUpdateCoordinator

@dataclass
class RooterSensorEntityDescription(SensorEntityDescription):
    """Class describing ROOTer sensor entities."""
    key: str

SENSOR_TYPES: tuple[RooterSensorEntityDescription, ...] = (
    RooterSensorEntityDescription(
        key="signal_strength",
        name="Signal Strength",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:signal",
    ),
    RooterSensorEntityDescription(
        key="csq",
        name="CSQ",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:signal-cellular-outline",
    ),
    RooterSensorEntityDescription(
        key="rssi",
        name="RSSI",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    RooterSensorEntityDescription(
        key="rsrp",
        name="RSRP",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    RooterSensorEntityDescription(
        key="rsrq",
        name="RSRQ",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    RooterSensorEntityDescription(
        key="sinr",
        name="SINR",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    RooterSensorEntityDescription(
        key="band",
        name="Band",
        icon="mdi:radio-tower",
    ),
    RooterSensorEntityDescription(
        key="mode",
        name="Mode",
        icon="mdi:access-point-network",
    ),
    RooterSensorEntityDescription(
        key="cell_id",
        name="Cell ID",
        icon="mdi:transmission-tower",
    ),
    RooterSensorEntityDescription(
        key="mcc",
        name="MCC",
        icon="mdi:sim",
    ),
    RooterSensorEntityDescription(
        key="mnc",
        name="MNC",
        icon="mdi:sim",
    ),
    RooterSensorEntityDescription(
        key="router_model",
        name="Router Model",
        icon="mdi:router",
    ),
    RooterSensorEntityDescription(
        key="modem_model",
        name="Modem Model",
        icon="mdi:chip",
    ),
    RooterSensorEntityDescription(
        key="provider",
        name="Provider",
        icon="mdi:network",
    ),
    RooterSensorEntityDescription(
        key="temperature",
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    RooterSensorEntityDescription(
        key="bands",
        name="Bands Detail",
        icon="mdi:radio-tower",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up ROOTer sensors based on a config entry."""
    coordinator: RooterDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for description in SENSOR_TYPES:
        if description.key in coordinator.data:
            entities.append(RooterSensor(coordinator, description))
            
    async_add_entities(entities)

class RooterSensor(CoordinatorEntity, SensorEntity):
    """Defines a ROOTer sensor."""

    entity_description: RooterSensorEntityDescription

    def __init__(
        self,
        coordinator: RooterDataUpdateCoordinator,
        description: RooterSensorEntityDescription,
    ) -> None:
        """Initialize ROOTer sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.client._host}_{description.key}"
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.client._host)},
            "name": f"ROOTer {coordinator.client._host}",
            "manufacturer": "ROOTer",
            "model": coordinator.data.get("router_model", "Unknown"),
            "sw_version": coordinator.data.get("modem_model", "Unknown"),
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)
