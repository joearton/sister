# Sister
Simple Sister API client (Dikti/Kemdikbudristek) using Python.

## Sister Credential Preparation
1. Get your developer credential from **akses.ristekdikti.go.id**.
2. In there, create new user with role "Developer".
3. Open your sister, and syncronize to get new "developer user".
4. Login to your sister using developer credential.
5. Copy username, password, and id_pengguna, and put it on "config.json".

## Config Preparation
1. Copy/rename "config.template.json" to "config.json" in config folder.
2. Set your Sister URL with schema, example: https://sister.umko.ac.id.
3. Set credential username, password, and id_pengguna of your account.

## Official API Guide
https://sister.kemdikbud.go.id

## Basic Use
```
from sister import SisterAPI 

api = SisterAPI()
res = api.get_data('/referensi/sdm')
print(res)
```
