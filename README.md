# Tuya Smoke Detector Cloud

A HACS custom integration for reading two Tuya Wi-Fi smoke detectors through Tuya IoT Cloud. It is a separate integration and does not replace or modify Home Assistant's built-in Tuya or Xtend Tuya integrations.

## Confirmed devices

| Location | Tuya device ID |
|---|---|
| Kitchen | `bfd594ab265a617489nqsn` |
| Factory | `bf6b8165e386e79696stm` |

## Exposed properties

| Property | DP | Home Assistant entity |
|---|---:|---|
| `smoke_sensor_state` | 1 | Raw value sensor and smoke alarm binary sensor |
| `battery_percentage` | 15 | Battery percentage |
| `muffling` | 16 | Raw value sensor (read only) |
| `temp_current` | 23 | Temperature in °C (raw value divided by 10) |
| `humidity_value` | 24 | Humidity in percent (raw value preserved) |
| `temp_alarm` | 101 | Raw value sensor and heat alarm binary sensor |
| `self_test` | 102 | Raw value sensor |

Every property sensor includes its Tuya DP and raw response value as attributes. The alarm binary sensors map common truthy values (`true`, `1`, `on`, `alarm`, `smoke`, `high`) to active. Since the device's enum mapping has not been confirmed, use the raw sensor values to verify alarm semantics before using the binary sensors in safety automations.

## Tuya project setup

Create a Tuya IoT Cloud Development project, link the Smart Life/Tuya app account containing the detectors, enable the relevant device status/query API permissions, and select the **Central Europe Data Center**. You will need the project's Access ID (Client ID) and Access Secret (Client Secret).

The integration asks for those credentials in Home Assistant's setup form and stores them in its config entry. No credentials are included in these files. The API endpoint is `https://openapi.tuyaeu.com`; access tokens are acquired and refreshed by the integration.

## HACS installation

This folder is laid out as the root of a HACS custom integration repository. To install it through HACS, publish the contents of this folder in a GitHub repository, then:

1. In HACS, open **Integrations** → menu → **Custom repositories**.
2. Add the repository URL and select **Integration**.
3. Download **Tuya Smoke Detector Cloud** and restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration** and choose **Tuya Smoke Detector Cloud**.
5. Enter the Client ID, Client Secret, and one device ID. Add the second device as another integration entry with the same project credentials.

For manual installation, copy `custom_components/tuya_smoke_detector_cloud` into your Home Assistant configuration directory's `custom_components` folder, restart, and add the integration in the UI.

## Polling and scope

The integration queries the Tuya device status endpoint once per minute. It is read-only: `muffling` is exposed as a sensor because the confirmed details establish property reads, not a supported write command. Existing Tuya integrations remain untouched.

## Troubleshooting

- **Cannot connect:** check Client ID/Secret, Central Europe region, app-account linkage, API permissions, and device ID.
- **No properties returned:** verify the cloud project is authorized to query status for the linked device.
- **Alarm meaning is unexpected:** inspect the raw state value. Device enum mappings may differ; the binary entities use only a conservative common-value mapping.

## Release status

Initial package version `0.1.0`. It has not yet been authenticated against the user's live Tuya project or devices. A public repository URL must be created before HACS can add this as a custom repository.
