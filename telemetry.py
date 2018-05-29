import requests
import json
import players
import matches

global url
url = "https://cdn.gamelockerapp.com/stunlock-studios-battlerite/global/2018/05/02/17/07/55dea46c-4e2b-11e8-a3c8-0a586460b906-telemetry.json"

global header
header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3NzMxMGZjMC0yYjc1LTAxMzYtYjIyYi0wYTU4NjQ2MGI5M2QiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0NzQzMjI1LCJwdWIiOiJzdHVubG9jay1zdHVkaW9zIiwidGl0bGUiOiJiYXR0bGVyaXRlIiwiYXBwIjoiYmF0dGxlcml0ZS1jb21wYW5pb24tY2EzZmRmMTItODYxOS00ZDIzLWI3YWYtN2MyMWYzOGRkMjdlIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.hILjtng403GUUZN8cLqdsCp8R6qnESkoZOeLgRcvvx4",
    "Accept": "application/vnd.api+json"
}

def getTelemetryInfo():
    query = {
        "page[limit]": "3000"
    }

    request = requests.get(url, headers=header, params=query)
    request = request.json()
    return request

def getTelemetryJson():
    query = {
        "page[limit]": "3000"
    }

    r = requests.get(url, headers=header, params=query)
    f = r.json()
    return json.dumps(f)