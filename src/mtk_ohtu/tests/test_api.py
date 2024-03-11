import pytest

def test_api_missing_parameters(client):
    with client:
        response = client.post("/api/logistics_info", content_type="application/json; charset=utf-8", json={
            "test_attribute": 123
        })
        assert response.content_type == "application/json"
        msg = response.json["message"]
        assert "test_attribute" in msg
        assert msg["test_attribute"] == ["Unknown field."]
        assert msg["address"] == ["Missing data for required field."]
        assert msg["posting_id"] == ["Missing data for required field."]

def test_api_incorrect_url(client):
    with client:
        response = client.post("/api/test", json={
            "address": {"streetAddress": "Helsinki"},
            "posting_id": 6
        })
        assert response.status_code == 404

def test_api_incorrect_parameter_types(client):
    with client:
        response = client.post("/api/logistics_info", json={
            "address": {"streetAddress": "Turku"},
            "posting_id": "test_str"
        })
        assert response.content_type == "application/json"
        msg = response.json["message"]
        assert msg["posting_id"] == ["Invalid posting_id (int expected)"]

def test_api_invalid_listing_id(client):
    with client:
        response = client.post("/api/logistics_info", json={
            "address": {"streetAddress": "Helsinki"},
            "posting_id": -512
        })
        assert response.status_code == 400

def test_api_invalid_address(client):
    with client:
        response = client.post("/api/logistics_info", json={
            "posting_id": 6,
            "address": {"streetAddress": "-612361236123"}
        })
        msg = response.json["message"]
        assert response.status_code == 400
        assert msg["address"]["streetAddress"] == ["Invalid address: -612361236123"]

def test_api_correct_response(client):
    with client:
        response = client.post("/api/logistics_info", json={
            "posting_id": 3,
            "address": {"streetAddress": "Helsinki"}
        })

        # These values need to be updated with the mock data
        assert response.json["provider_count"] == 4
        assert round(response.json["distance"], -1) == 530
        assert response.json["logistics_url"] == "http://localhost/listing/3"

def test_api_incomplete_address(client):
    with client:
        response = client.post("/api/logistics_info", json={
            "posting_id": 3,
            "address": {"latitude": 61.7123, "city": "Helsinki"}
        })

        assert response.status_code == 400