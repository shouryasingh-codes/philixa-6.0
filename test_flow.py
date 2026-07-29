import httpx

def test_flow():
    headers = {"X-API-Key": "philixa-demo-secret-123"}
    base_url = "http://127.0.0.1:8000"
    
    with httpx.Client(base_url=base_url) as client:
        # 1. Check health
        r = client.get("/health", headers=headers)
        print("Health:", r.status_code, r.text)
        
        # 2. Process a meeting note
        r = client.post("/api/v1/meeting-notes/process", headers=headers, json={
            "raw_notes": "Met Rajesh Sharma today. Interested in business loan. Promised documents by Friday.",
            "meeting_date": "2026-06-19"
        })
        print("Process note response:", r.status_code, r.json())
        data = r.json()
        
        client_id = data.get("client_id")
        meeting_id = data.get("meeting_id")
        
        if data.get("requires_client_confirmation"):
            print("Requires confirmation, confirming as new client...")
            r = client.post(f"/api/v1/meeting-notes/{meeting_id}/confirm-client", headers=headers, json={
                "new_client_name": "Rajesh Sharma"
            })
            print("Confirm client response:", r.status_code, r.json())
            data = r.json()
            client_id = data.get("client_id")
        
        print("Client ID:", client_id)
        
        # 3. Get client memory
        r = client.get(f"/api/v1/clients/{client_id}/memory", headers=headers)
        print("Memory response:", r.status_code, r.json())

        # 4. List commitments
        r = client.get("/api/v1/commitments", headers=headers)
        print("Commitments response:", r.status_code, r.json())

        # 5. Clean up
        r = client.delete(f"/api/v1/clients/{client_id}", headers=headers)
        print("Delete response:", r.status_code)

if __name__ == "__main__":
    test_flow()
