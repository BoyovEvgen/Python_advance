
import pytest


@pytest.mark.parametrize('name, link',
                         [("Create Articles", "/article/create"),
                          ("Blog", "/"),
                          ("Create category", "/category/create")
                          ])
def test_create_menu(client, name, link):
    response = client.post("http://nginx/api/menu-items", json={
        "name": name,
        "link": link
    })
    assert response.status_code == 200
    assert response.json.get("link") == link


def test_get_menu(client):
    response = client.get("http://nginx/api/menu-items")
    assert response.status_code == 200
    assert response.json[0].get("name") == "Create Articles"
    assert response.json[1].get("name") == "Blog"
    assert response.json[2].get("name") == "Create category"
