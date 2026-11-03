# Tuya Smoke Detector Cloud

A HACS custom integration that reads Tuya Wi-Fi smoke detectors through the Tuya IoT Cloud **Query Properties** API. It is a separate integration, not an extension of Xtend Tuya and not a replacement for the built-in Tuya integration.

## Confirmed devices

| Location | Tuya device ID |
|---|---|
| Kitchen | `bfd594ab265a617489nqsn` |
| Factory | `bf6b8165e386e79696stm` |

## Entities

The integration reads the seven confirmed cloud properties:

| Property | DP | Entity behavior |
|---|---:|---|
| `smoke_sensor_state` | 1 | Smoke sensor status, raw enum (for example `normal`) |
| `battery_percentage` | 15 | Battery percent |
| `muffling` | 16 | Muffling value |
| `temp_current` | 23 | Temperature °C; raw value divided by 10 |
| `humidity_value` | 24 | Humidity percent; raw value retained |
| `temp_alarm` | 101 | Temperature alarm enum; `cancel` is displayed as `None` |
| `self_test` | 102 | Self-test On/Off |

The primary entities match the five shown in the provided Xtend Tuya screenshot: Humidity, Self test, Smoke sensor status, Temperature, and Temperature alarm. Battery and Muffling are additional confirmed properties. This integration reads the same cloud property values; it does not attach entities to Xtend Tuya's device.

## Tuya project setup

Use the existing Tuya IoT Cloud Development project linked to the Smart Life/Tuya account containing the detectors. Ensure the project uses the **Central Europe Data Center** and is authorized for Query Properties (`GET /v2.0/cloud/thing/{device_id}/shadow/properties`). The integration uses `https://openapi.tuyaeu.com`.

Enter the project's Access ID and Access Secret in Home Assistant's setup form. Credentials are stored in the config entry and are not included in the source files.

## HACS installation

1. In HACS, open **Integrations** → menu → **Custom repositories**.
2. Add `https://github.com/manieschutte/tuya-smoke-detector-cloud` as type **Integration**.
3. Download **Tuya Smoke Detector Cloud** and restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration** and select **Tuya Smoke Detector Cloud**.
5. Add each detector as a separate entry using the same project credentials and its device ID.

For manual installation, copy `custom_components/tuya_smoke_detector_cloud` into the Home Assistant configuration directory's `custom_components` folder, restart, and add the integration in the UI.

## Polling

The integration polls Query Properties once per minute. It is read-only. It does not send control commands or change existing Tuya/Xtend Tuya integrations.

## Release status

Version `0.2.0` corrects the API endpoint and response parsing to use the Tuya Query Properties result shape. It has not yet been authenticated against the user's live Home Assistant install. Compare the values using the same detector ID; the supplied Xtend screenshot and API response may refer to different detectors.
