import anthropic

from lib.describe import build_describe_prompt


def describe_via_anthropic(image_base64, api_key, model, base_url, location, view_description, current_temperature, temperature_unit, last_description_s):
    client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
    message = client.messages.create(
        model=model,
        max_tokens=200,
        temperature=0,
        timeout=60,
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
                        "text": build_describe_prompt(location, view_description, current_temperature, temperature_unit, last_description_s)
                    }
                ],
            }
        ],
    )

    description = message.content[0].text
    return description
