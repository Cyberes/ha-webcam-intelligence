# ha-webcam-intelligence

_Use AI vision to summarize current weather conditions from a webcam._

This uses a webcam to generate a current weather conditions summary via AI. Supports OpenAI and Anthropic.

The entity's state is the generated summary compressed via Brotli and encoded in Base91 in order to keep the length of
the state under the maximum of 255 characters.

### Install

1. `pip install -r requirementst.txt`
2. Configure your environment variables at `/etc/secrets/webcam-intelligence`. Here's an example:
   ```
   HLS_STREAM="http://192.168.10.106:8888/webcam/index.m3u8"
   AI_MODEL="claude-3-7-sonnet-latest"
   AI_API_KEY="xxx"
   WEBCAM_LOCATION="Anytown, Texas"
   WEBCAM_VIEW_DESCRIPTION="Webcam is above a small meadow and scrub oak trees. View is southerly and looks out to the Whatever Range. On a clear day, the mountains are visible all the way to Bob Joe Mountain."
   HA_ACCESS_TOKEN="xxx"
   HA_BASE_URL="home.example.com"
   HA_TEMPERATURE_SENSOR="sensor.weather_station_temperature"
   MQTT_BROKER_HOST="192.168.10.103"
   MQTT_USERNAME="user"
   MQTT_PASSWORD="xxx"
   ```
3. Install the systemd services.
4. Add this to your Home Assistant MQTT config:
   ```yaml
   - name: "Webcam Intelligent Summary"
     state_topic: "webcam-intelligence/webcam-intelligent-summary"
     unique_id: webcam_intelligent_summary
     json_attributes_topic: "webcam-intelligence/webcam-intelligent-summary/attributes"
   ```
5. Restart Home Assistant

The correct provider is chosen based on the model name. OpenAI's `o1` and `o3-mini` produce very dry and brief
reports. Claude writes slightly longer, more detailed, and "creative" reports. Choose the style you want.

### Dashboard Card

```yaml
type: markdown
content: |-
  ### Anytown Conditions
  {{ state_attr('sensor.webcam_intelligent_summary', 'summary') }}
```

### Example Summary

#### Claude 3.7 Sonnet

> Twilight conditions with a prominent stratocumulus cloud deck visible across the sky.<br>
> Cloud formation appears to be developing with some vertical structure, particularly over the mountain range.<br>
> Visibility is good with the Whatever Range clearly defined against the darkening sky.<br>
> City lights are becoming visible in the valley below.<br>
> No active precipitation observed in the immediate area.

#### o3-mini

> Twilight persists over Anytown with a broad stratocumulus layer and moderate vertical cloud development above the
> mountains.<br>
> The Whatever Range stands clearly against the darkening horizon while city lights emerge in the valley below.<br>
> No active precipitation or significant snow accumulation is evident.

#### o1

> Twilight conditions remain with a broad stratocumulus layer stretching across the sky.<br>
> Cloud formation exhibits moderate vertical development over the mountains, and the Whatever Range is clearly visible
> against the darkening horizon.<br>
> City lights are discernible in the valley below, with no new precipitation or snow accumulation evident.