import requests
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
zip_path = os.path.join(parent_dir, 'output.zip')

url = os.environ['DEPLOY_URL']
token = os.environ.get('DEPLOY_TOKEN', '')
mirror_url = os.environ['MIRROR_DEPLOY_URL']
mirror_token = os.environ.get('MIRROR_DEPLOY_TOKEN', '')

with open(zip_path, 'rb') as f:
    r = requests.post(
        url,
        files={'file': f},
        headers={'Authorization': f'Bearer {token}'}
    )

with open(zip_path, 'rb') as f:
    r = requests.post(
        mirror_url,
        files={'file': f},
        headers={'Authorization': f'Bearer {mirror_token}'}
    )

print(f"Server responded with status: {r.status_code}")
print(r.text)

print(f"Mirror server responded with status: {r.status_code}")
print(r.text)
