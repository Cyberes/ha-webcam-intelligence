from datetime import datetime

import anthropic


def describe_image_via_ai(image_base64, api_key, model, base_url, location, view_description, current_temperature, temperature_unit):
    text = f'''
You are a NOAA automated weather service that analyzes a webcam to write a current weather conditions report.
Write a short summary in professional meteorology language and formatting. Length should be 1 short paragraph. You should only return 1 paragraph and do not include any headers or other formatting. Please begin the summary immediately and do not include any openers like "Current conditions:". 
Describe only the most important information, do not speculate, and do not forcast.
Do not describe wind, vegetation, or residual snow from past storms. Don't summarize your summary (ie. "Conditions appear typical of"). We don't really care about the ground besides snow accumulation and rain puddles.
Describe any precipitiation. We're only concerned about significant snow accumulation so ignore any residual snow that appears to be from past storms.
Your summary will be shown along with the image and other current weather data. The consumers of your summary are professional meteorologists (although you should avoid overly technical terms or measurements). It is not nessesary to describe the temperature as they will have access to the current data as well.
Please add newlines to improve readability. 
Location: {location}. {view_description}
Timestamp: {datetime.now().strftime("%H:%M %b %d, %Y")}
Temperature: {current_temperature} {temperature_unit}'''

    client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
    message = client.messages.create(
        model=model,
        max_tokens=200,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": text
                    }
                ],
            }
        ],
    )

    description = message.content[0].text
    return description
