def test_api_search(client):
    response = client.get("/api/spells", query_string = {"kw":"","rpp":25,"page":1,"schoolMul":["塑能"],"levelMul":["3"],"classMul":["wizard"]})
    #post用data，get用query_string
    data = response.get_json()
    assert response.status_code == 200
    assert data["total"] >= 1
    assert "results" in data

def test_api_info(client):
    response = client.get("/api/spells/Fireball")
    assert response.status_code == 200

def test_api_info_wrong(client):
    response = client.get("/api/spells/Firedoll")
    assert response.status_code == 404