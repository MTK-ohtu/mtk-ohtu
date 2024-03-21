import pytest
from copy import deepcopy

def post_test(client, json):
    return client.post(
        "/api/postings",
        content_type="application/json; charset=utf-8",
        headers={"API-Key": "test_api_key"},
        json=json,
    )

CREATE_JSON={'posting_id': 100, 'entry_type': 'create', 'title': 'esm', 'description': 'kuv', 'category': 'Wood', 'sub_category': 'Treated wood', 'post_type': 'sell', 'delivery_method': 'pickup', 'demand': 'one time', 'batch_size': 200, 'batch_type': 'tn', 'expiry_date': 1712825393, 'price': 200, 'delivery_details': 'tx', 'address': { 'latitude' : 62.02740179999999, 'longitude' : 24.6354997, 'country' : 'Suomi', 'city' : 'Mänttä', 'state' : None, 'streetAddress' : 'Tehtaankatu 20, Mänttä, Suomi', 'postalCode' : None, 'apartment' : None }, 'date_created': 1712825393 }

UPDATE_JSON={'posting_id': 1, 'entry_type': 'update', 'price': 1234}

def test_db_api_missing_parameters(client):
    with client:
        response = post_test(client, json={"test_attribute": 123})
        assert response.content_type == "application/json"
        msg = response.json["message"]
        assert "test_attribute" in msg
        assert msg["test_attribute"] == ["Unknown field."]
        assert msg["posting_id"] == ["Missing data for required field."]

def test_db_create_missing_parameters(client):
    json = deepcopy(CREATE_JSON)
    json.pop('price')
    with client:
        response = post_test(client, json=json)
        assert response.content_type == "application/json"
        assert not response.json["success"]
        msg = response.json["message"]
        assert ["Missing required fields from create"] in msg.values()

def test_db_create_post_already_exists(client):
    json = deepcopy(CREATE_JSON)
    json["posting_id"] = 1
    with client:
        response = post_test(client, json=json)
        assert response.content_type == "application/json"
        assert not response.json["success"]
        assert response.json["message"] == "Post id 1 already exists. Did you mean to update?"
        assert response.status_code == 401

def test_db_create_post_correct_succeeds(client):
    json = deepcopy(CREATE_JSON)
    with client:
        response = post_test(client, json=json)
        assert response.content_type == "application/json"
        assert response.json["success"]
        assert client.get("en/listing/100").status_code == 200

def test_db_update_post_id_not_exists(client):
    json = deepcopy(UPDATE_JSON)
    json["posting_id"] = 100
    with client:
        response = post_test(client, json=json)
        assert response.content_type == "application/json"
        assert not response.json["success"]
        assert response.json["message"] == "No post with post_id 100"
        assert response.status_code == 404

def test_db_update_post_correct_succeeds(client):
    json = deepcopy(UPDATE_JSON)
    with client:
        assert "<h1>250 €</h1>".encode('utf8') in client.get("en/listing/1").data
        response = post_test(client, json=json)
        assert response.content_type == "application/json"
        assert response.json["success"]
        assert "<h1>1234 €</h1>".encode('utf8') in client.get("en/listing/1").data

def test_db_delete_post_not_exists(client):
    with client:
        response = post_test(client, json={'posting_id': 100, 'entry_type': 'delete'})
        assert response.content_type == "application/json"
        assert not response.json["success"]
        assert response.json["message"] == "No post with post_id 100"
        assert response.status_code == 404

def test_db_delete_post_correct_succeeds(client):
    with client:
        assert client.get("en/listing/1").status_code == 200
        response = post_test(client, json={'posting_id': 1, 'entry_type': 'delete'})
        assert response.content_type == "application/json"
        assert response.json["success"]
        assert client.get("en/listing/1").status_code == 404

def test_incorrect_api_key(client):
    with client:
        response = client.post(
            "/api/postings",
            content_type="application/json; charset=utf-8",
            headers={"API-Key": "incorrect key"},
            json={"posting_id": 3, "address": {"streetAddres": "Helsinki"}},
        )

        assert response.status_code == 401


def missing_api_key(client):
    with client:
        response = client.post(
            "/api/postings",
            content_type="application/json; charset=utf-8",
            json={"posting_id": 3, "address": {"streetAddres": "Helsinki"}},
        )

        assert response.status_code == 401
