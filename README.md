# ha-webcam-intelligence

_Use AI vision to summarize current weather conditions from a webcam._

This uses a webcam to generate a current weather conditions summary via the Anthropic API.

### Install

1. `pip install -r requirementst.txt`
2. Configure your environment variables at `/etc/secrets/webcam-intelligence`. Here's an example:
   ```
   HLS_STREAM="http://192.168.10.106:8888/webcam/index.m3u8"
   ANTHROPIC_MODEL="claude-3-7-sonnet-latest"
   ANTHROPIC_API_KEY="xxx"
   WEBCAM_LOCATION="Anytown, Texas"
   WEBCAM_VIEW_DESCRIPTION="Webcam is above a small meadow and scrub oak trees. View is southerly and looks out to the Whatever Range. On a clear day, the mountains are visible all the way to Bob Joe Mountain."
   HA_ACCESS_TOKEN="xxx"
   HA_BASE_URL="home.example.com"
   HA_TEMPERATURE_SENSOR="sensor.weather_station_temperature"
   MQTT_BROKER_HOST="192.168.10.103"
   MQTT_USERNAME="user"
   MQTT_PASSWORD="xxx"
   ```
4. Install the systemd services.
5. Add this to your Home Assistant MQTT config:
   ```yaml
   - name: "Webcam Intelligent Summary"
     state_topic: "webcam-intelligence/webcam-intelligent-summary"
     unique_id: webcam_intelligent_summary
     json_attributes_topic: "webcam-intelligence/webcam-intelligent-summary/attributes"
   ```
6. Restart Home Assistant

### Dashboard Card

```yaml
type: markdown
content: |-
  ### Anytown Conditions
  {{ state_attr('sensor.webcam_intelligent_summary', 'summary') }}
```

### Example Summary

> Overcast conditions prevail with a low, uniform cloud deck obscuring the Whatever Range and distant mountain
> views.<br>Visibility is significantly reduced with a gray, hazy appearance suggesting possible light precipitation or
> fog in the area.<br>No active precipitation is currently visible in the immediate foreground, though patches of
> melting
> snow remain visible in scattered areas of the landscape.<br>The cloud ceiling appears quite low, with complete stratus
> coverage creating diffuse lighting across the scene.