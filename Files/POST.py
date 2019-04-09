import requests
import os
import base64


def get_image(testName, image):
    with open(image, "rb") as imageFile:
        name = base64.urlsafe_b64encode(imageFile.read())

    base64_string = name.decode('utf-8')
    # defining the api-endpoint
    API_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate?key=YOUR_API_KEY"
    # your source code here
    source_code = {
        "requests": [
            {
                "image": {
                    "content": base64_string
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION",
                        "maxResults": 1
                    }
                ]
            }
        ]
    }

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, json=source_code)

    # extracting response text
    text = r.text

    path = r"C:\Users\YASH\PycharmProjects\ValueExtractor\Json"
    os.chdir(path)
    complete_name = testName + ".json"
    with open(complete_name, 'w', encoding='utf-8') as f:
        f.write(text)
