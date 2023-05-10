

def test_create_article(client):
    response = client.post("http://nginx/api/articles", json={
        "title": "hello",
        "body": "hello hello hello"
    })
    assert response.status_code == 200
    assert response.json.get("title") == "hello"


def test_get_articles_list(client):
    response = client.get("http://nginx/api/articles")
    assert response.status_code == 200
    assert response.json[0].get("id") == 1


def test_get_article_first(client):
    response = client.get("http://nginx/api/articles/1")
    assert response.status_code == 200
    assert response.json.get("id") == 1


def test_article_put(client):
    response = client.put("http://nginx/api/articles/1", json={
        "title": "bye",
        "body": "hello hello] hello"
    })
    assert response.status_code == 200
    assert response.json.get("title") == "bye"


def test_dell_article(client):
    res = client.delete("http://nginx/api/articles/1")
    assert res.status_code == 204


