import requests
import json

class ApiClient:
    def __init__(self):
        self.base_url = "https://okisun.xyz/api/user/enter-call?token="

    def enter_call(self, token, rawDeviceId, sId, link):
        url = f"{self.base_url}{token}"

        data = {
            "rawDeviceId": rawDeviceId,
            "sId": sId,
            "link": link 
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            try:
                response_json = response.json()
                return response_json
            except json.JSONDecodeError:
                raise Exception("Resposta inválida.")
        else:
            raise Exception(f"Falha ao requisitar: - {response.status_code}")

# Usage
if __name__ == "__main__":
    token = input("Enter token: ")
    rawDeviceId = input("Enter rawDeviceId: ")
    sId = input("Enter sId: ")
    link = input("Enter link (can be empty): ")

    api_client = ApiClient()
    result = api_client.enter_call(token, rawDeviceId, sId, link)
    
    print("Response:")
    print(result)
