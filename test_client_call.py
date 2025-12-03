from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

resp = client.get('/users/trainers/approved')
print('status', resp.status_code)
print(resp.json())
