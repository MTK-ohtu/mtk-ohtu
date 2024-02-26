import pytest

def test_api_missing_parameters(client):
    with client:
        response = client.get("/api/logistics_info", content_type="application/json; charset=utf-8", json={
            "test_attribute": 123
        })
        assert response.content_type == "application/json"
        assert "test_attribute" in response.json
        assert response.json["test_attribute"] == ["Unknown field."]
        assert response.json["location"] == ["Missing data for required field."]
        assert response.json["listing"] == ["Missing data for required field."]

def test_api_incorrect_url(client):
    with client:
        response = client.get("/api/test", json={
            "location": "Helsinki",
            "listing": 6
        })
        assert response.status_code == 404

def test_api_incorrect_parameter_types(client):
    with client:
        response = client.get("/api/logistics_info", json={
            "location": 12673,
            "listing": "test_str"
        })
        assert response.content_type == "application/json"
        assert response.json["location"] == ["Invalid location input"]
        assert response.json["listing"] == ["Invalid listing id (int expected)"]

def test_api_invalid_listing_id(client):
    with client:
        response = client.get("/api/logistics_info", json={
            "location": "Helsinki",
            "listing": -512
        })
        assert response.json["listing"] == ["Invalid listing id (no listing found with id -512)"]

def test_api_invalid_address(client):
    with client:
        response = client.get("/api/logistics_info", json={
            "listing": 6,
            "location": "-612361236123"
        })
        assert response.json["location"] == ["Invalid address: -612361236123"]

def test_api_correct_response(client):
    with client:
        response = client.get("/api/logistics_info", json={
            "listing": 9,
            "location": "Helsinki"
        })

        # These values need to be updated with the mock data
        assert response.json["num_providers"] == 7
        assert round(response.json["distance"], -1) == 60
        assert response.json["link"] == "http://localhost/listing/9"