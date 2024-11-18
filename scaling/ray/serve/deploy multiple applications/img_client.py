import requests

bear_url = "https://cdn.britannica.com/41/156441-050-A4424AEC/Grizzly-bear-Jasper-National-Park-Canada-Alberta.jpg"  # noqa
resp = requests.post("http://localhost:8000/classify", json={"image_url": bear_url})

print(resp.text)
# 'brown bear, bruin, Ursus arctos'