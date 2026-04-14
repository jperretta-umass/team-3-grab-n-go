# def test_get_dining_halls(client):
#     """
#     Example integration test for a DB-backed GET endpoint.

#Verifies that dining halls seeded during test setup are returned correctly.

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     If the endpoint path, response format, or seed data changes,
#     update this test.
#     """
#     response = client.get("/customer/dininghalls")
#     assert response.status_code == 200

#     data = response.json()
#     assert len(data) == 2

#     names = [hall["name"] for hall in data]
#     assert "Worcester" in names
#     assert "Franklin" in names


# def test_get_items_for_dining_hall(client):
#     """
#     Example integration test for retrieving items from a dining hall.

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     This test currently assumes dining hall ID 1 exists in seed data.
#     If IDs become dynamic or seed data changes, update this test.
#     """
#     response = client.get("/customer/dininghalls/items/1")
#     assert response.status_code == 200

#     data = response.json()
#     assert len(data) >= 1


# def test_add_item_to_cart(client):
#     """
#     Example integration test for a DB-backed write operation.

#     Verifies that adding an item to a cart persists and can be read back.

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     This test currently assumes:
#     - cart 1 exists
#     - item 1 exists
#     - POST behavior remains the same
#     """
#     response = client.post("/customer/cart/1/item/1")
#     assert response.status_code == 200

#     cart_response = client.get("/customer/cart/1")
#     assert cart_response.status_code == 200
#     cart_data = cart_response.json()
#     assert len(cart_data) >= 1


# def test_update_cart_item_quantity(client):
#     """
#     Example integration test for a DB-backed update operation.

#     Verifies that PATCH updates quantity correctly.

#     IMPORTANT FOR FUTURE DATABASE IMPLEMENTATION:
#     This test currently assumes the same cart/item IDs as the seed data.
#     Update if cart schema or endpoint behavior changes.
#     """
#     client.post("/customer/cart/1/item/1")

#     response = client.patch(
#         "/customer/cart/1/item/1",
#         json={"quantity": 3},
#     )
#     assert response.status_code == 200
#     assert response.json()["quantity"] == 3
