import requests


class DataManager:
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.bearer_token = f"Bearer {token}"
        self.header = {
            "Content-Type": "application/json",
            "Authorization": self.bearer_token
        }
        self.data = []

    def get_flight_data(self):
        response = requests.get(url=f"{self.endpoint}/prices", headers=self.header)
        result = response.json()
        self.data = result['prices']
        return result['prices']

    def update_flight_data(self, row_id, payload):
        url = f"{self.endpoint}/prices/{row_id}"
        body = {
            "price": {key: payload[key] for key in payload}
        }
        response = requests.put(url=url, json=body, headers=self.header)
        result = response.json()
        print(result)

    def add_user(self, user):
        url = f"{self.endpoint}/users"
        body = {
            "user": {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email
            }
        }
        response = requests.post(url=url, json=body, headers=self.header)
        result = response.json()
        print(result)

    def get_users(self):
        response = requests.get(url=f"{self.endpoint}/users", headers=self.header)
        result = response.json()
        self.data = result['users']
        return result['users']