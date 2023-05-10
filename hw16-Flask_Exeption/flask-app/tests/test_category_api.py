
def test_get_categories(client):
    response = client.get("http://nginx/api/categories")
    assert response.status_code == 200
    assert response.json[0].get("name") == "Test1"
    assert response.json[1].get("name") == "Test2"
