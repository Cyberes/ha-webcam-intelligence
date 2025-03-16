from openai import OpenAI

from lib.describe import build_describe_prompt


def describe_via_openai(image_base64, api_key, model, base_url, location, view_description, current_temperature, temperature_unit, last_description_s):
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": build_describe_prompt(location, view_description, current_temperature, temperature_unit, last_description_s)
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ],
            }
        ],
    )

    description = response.output_text
    return description
