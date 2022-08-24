import requests
import os

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

BASE_URL = f"https://{AUTH0_DOMAIN}"
API_USERS = "/api/v2/users"
API_INFO = "/api/private/info"
API_OAUTH_TOKEN = "/oauth/token"


class AuthError(Exception):
    pass


class Auth0Utils:
    def __init__(self) -> None:
        self.bearer: str = None
        self.user_cache: dict = {}

        self._get_bearer_token()

    @property
    def headers(self):
        return {"authorization": f"Bearer {self.bearer}"}

    def _get_bearer_token(self) -> None:
        """Gets the Auth0 bearer token and store it in the class.
        Only need to call this once.
        """
        print("Auth0Utils._get_bearer_token(), Getting access token from Auth0...")

        if self.bearer:
            return self.bearer

        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "audience": f"{BASE_URL}/api/v2/",
            "grant_type": "client_credentials",
        }

        try:
            response = requests.post(f"{BASE_URL}{API_OAUTH_TOKEN}", json=data)
        except Exception as e:
            print("Could not call the API :(", str(e))

        if response.status_code != 200:
            print("There was an error :(", response.content)

        resp_json = response.json()
        if "access_token" not in resp_json:
            print("Could not find access token in response!! :(")
            raise AuthError("Could not find access token in response!! :(")

        self.bearer = resp_json["access_token"]

    def get_user_id(self, user_info):
        print("Auth0Utils.get_user_id(), Getting user id for", user_info.get("email"))
        user_email = user_info.get("email")
        user_id = self.user_cache.get(user_email)
        if user_id:
            return user_id

        api_url = f"{BASE_URL}{API_USERS}"

        resp = requests.get(api_url, headers=self.headers)
        res_json = resp.json()

        user_id = list(filter(lambda x: x["email"] == user_email, res_json))[0][
            "user_id"
        ]
        self.user_cache[user_email] = user_id
        return user_id

    def update_user(
        self, user_info, _class: str = None, key: str = None, secret: str = None
    ):
        print("Auth0Utils.update_user(), Getting user id for", user_info.get("email"))
        user_id = self.get_user_id(user_info)
        metadata = {}
        if _class:
            metadata["classes"] = _class
        if key:
            metadata["key"] = key
        if secret:
            metadata["secret"] = secret
        data = {"user_metadata": metadata}

        api_url = f"{BASE_URL}{API_USERS}/{user_id}"

        try:
            response = requests.patch(api_url, headers=self.headers, json=data)
        except Exception as e:
            print("Could not call the API :(", str(e))

        if response.status_code != 200:
            print("There was an error :(", response.content)

        print("Updated user successfully.")

    def get_user_creds(self, user_info):
        print(
            "Auth0Utils.get_user_creds(), Getting user credentials for",
            user_info.get("email"),
        )
        user_id = self.get_user_id(user_info)

        api_url = f"{BASE_URL}{API_USERS}/{user_id}"
        resp = requests.get(api_url, headers=self.headers)
        res_json: dict = resp.json()

        metadata = res_json.get("user_metadata", {})
        creds = [metadata.get("key"), metadata.get("secret")]
        if None not in creds:
            return creds

        print("Resetting creds for user")
        self.update_user(
            user_info=user_info, _class="default", key="default", secret="default"
        )
        return []

    def get_user_classes(self, user_info):
        print(
            "Auth0Utils.get_user_classes(), Getting user classes for",
            user_info.get("email"),
        )
        user_id = self.get_user_id(user_info)

        api_url = f"{BASE_URL}{API_USERS}/{user_id}"
        resp = requests.get(api_url, headers=self.headers)
        res_json: dict = resp.json()

        classes = res_json.get("user_metadata", {}).get("classes")
        if classes:
            return classes

        print("RESETTING METADATA CLASS")
        self.update_user(
            user_info=user_info, _class="default", key="default", secret="default"
        )
        return ""
