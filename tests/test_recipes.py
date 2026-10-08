SAMPLE = {
    "title": "김치찌개",
    "description": "얼큰한 찌개",
    "ingredients": ["김치", "돼지고기", "두부"],
    "steps": ["김치와 고기를 볶는다", "물을 붓고 끓인다", "두부를 넣는다"],
    "cook_time_minutes": 30,
}


def create(client, **overrides):
    resp = client.post("/recipes", json={**SAMPLE, **overrides})
    assert resp.status_code == 201
    return resp.json()


def test_create_recipe(client):
    resp = client.post("/recipes", json=SAMPLE)
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] == 1
    assert {k: body[k] for k in SAMPLE} == SAMPLE


def test_create_recipe_missing_title(client):
    payload = {k: v for k, v in SAMPLE.items() if k != "title"}
    assert client.post("/recipes", json=payload).status_code == 422


def test_create_recipe_empty_title(client):
    assert client.post("/recipes", json={**SAMPLE, "title": ""}).status_code == 422


def test_create_recipe_negative_cook_time(client):
    resp = client.post("/recipes", json={**SAMPLE, "cook_time_minutes": -1})
    assert resp.status_code == 422


def test_create_assigns_unique_ids(client):
    first = create(client)
    second = create(client, title="된장찌개")
    assert first["id"] != second["id"]


def test_list_recipes_empty(client):
    resp = client.get("/recipes")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_recipes(client):
    create(client)
    create(client, title="된장찌개")
    resp = client.get("/recipes")
    assert resp.status_code == 200
    assert [r["title"] for r in resp.json()] == ["김치찌개", "된장찌개"]


def test_get_recipe(client):
    created = create(client)
    resp = client.get(f"/recipes/{created['id']}")
    assert resp.status_code == 200
    assert resp.json() == created


def test_get_recipe_not_found(client):
    assert client.get("/recipes/999").status_code == 404


def test_update_recipe_partial(client):
    created = create(client)
    resp = client.put(f"/recipes/{created['id']}", json={"title": "참치김치찌개"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "참치김치찌개"
    assert body["ingredients"] == SAMPLE["ingredients"]
    assert client.get(f"/recipes/{created['id']}").json() == body


def test_update_recipe_invalid(client):
    created = create(client)
    resp = client.put(f"/recipes/{created['id']}", json={"cook_time_minutes": -5})
    assert resp.status_code == 422


def test_update_recipe_not_found(client):
    assert client.put("/recipes/999", json={"title": "x"}).status_code == 404


def test_delete_recipe(client):
    created = create(client)
    resp = client.delete(f"/recipes/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/recipes/{created['id']}").status_code == 404


def test_delete_recipe_not_found(client):
    assert client.delete("/recipes/999").status_code == 404
