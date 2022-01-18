import requests


class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Accept: application/json"
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class SisterSession(requests.Session):

    def __init__(self):
        super().__init__()
        self.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
