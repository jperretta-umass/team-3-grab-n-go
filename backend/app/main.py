from copy import deepcopy

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Grab & Go Mock API")


class CartItemUpdate(BaseModel):
    quantity: int = Field(default=1, ge=1, le=25)


def _mock_state() -> dict:
    return {
        "Users": [
            {
                "UserId": 101,
                "Username": "alice",
                "Email": "alice@umass.edu",
                "PhoneNum": "413-555-0101",
                "hasDelivererProfile": False,
                "DelieverId": None,
            },
            {
                "UserId": 103,
                "Username": "ben",
                "Email": "ben@umass.edu",
                "PhoneNum": "413-555-0103",
                "hasDelivererProfile": True,
                "DelieverId": 14,
            },
        ],
        "delivererProfile": [
            {"DelivererId": 14, "POrderId": 9001, "COrderId": 7002},
            {"DelivererId": 17, "POrderId": None, "COrderId": None},
        ],
        "Dininghalls": [
            {"DhId": 1, "DhName": "Hampshire", "isOpen": True},
            {"DhId": 2, "DhName": "Berkshire", "isOpen": True},
            {"DhId": 3, "DhName": "Franklin", "isOpen": False},
            {"DhId": 4, "DhName": "Worcester", "isOpen": True},
        ],
        "Items": [
            {
                "ItemId": 1,
                "ItemName": "Grilled Chicken Bowl",
                "Price": 13.25,
                "IsSnack": False,
                "Allergy": "dairy",
                "MealType": "lunch,dinner",
                "DietaryType": "gluten-free",
            },
            {
                "ItemId": 2,
                "ItemName": "Veggie Wrap",
                "Price": 10.50,
                "IsSnack": False,
                "Allergy": "none",
                "MealType": "lunch",
                "DietaryType": "vegetarian",
            },
            {
                "ItemId": 3,
                "ItemName": "Fruit Cup",
                "Price": 4.75,
                "IsSnack": True,
                "Allergy": "none",
                "MealType": "breakfast,lunch,dinner",
                "DietaryType": "vegan,gluten-free,vegetarian,no-peanuts",
            },
            {
                "ItemId": 4,
                "ItemName": "Sparkling Water",
                "Price": 2.50,
                "IsSnack": True,
                "Allergy": "none",
                "MealType": "breakfast,lunch,dinner",
                "DietaryType": "vegan,gluten-free,vegetarian,no-peanuts",
            },
        ],
        "DininghallsItems": [
            {"DhItemeId": 1, "DhId": 1, "ItemId": 1, "IsAvailable": True},
            {"DhItemeId": 2, "DhId": 2, "ItemId": 2, "IsAvailable": True},
            {"DhItemeId": 3, "DhId": 1, "ItemId": 3, "IsAvailable": True},
            {"DhItemeId": 4, "DhId": 1, "ItemId": 4, "IsAvailable": True},
        ],
        "Orders": [
            {
                "orderId": 5001,
                "userId": 101,
                "DhId": 1,
                "TotalPrice": 18.00,
                "OrderTime": "2026-03-31T10:15:00-04:00",
                "OrderStatus": "ready",
            },
            {
                "orderId": 5002,
                "userId": 103,
                "DhId": 2,
                "TotalPrice": 10.50,
                "OrderTime": "2026-03-31T10:25:00-04:00",
                "OrderStatus": "claimed",
            },
            {
                "orderId": 1,
                "userId": 101,
                "DhId": 1,
                "TotalPrice": 22.75,
                "OrderTime": "2026-03-31T10:35:00-04:00",
                "OrderStatus": "cart",
            },
        ],
        "OrderItems": [
            {
                "orderItems": 1,
                "OrderId": 5001,
                "ItemId": 1,
                "Quantity": 1.0,
                "SpecialInstruct": "No sauce",
                "DeliveryInstruct": "Leave at desk",
            },
            {
                "orderItems": 2,
                "OrderId": 5001,
                "ItemId": 3,
                "Quantity": 1.0,
                "SpecialInstruct": "",
                "DeliveryInstruct": "Leave at desk",
            },
            {
                "orderItems": 3,
                "OrderId": 5002,
                "ItemId": 2,
                "Quantity": 1.0,
                "SpecialInstruct": "Cut in half",
                "DeliveryInstruct": "Meet outside",
            },
            {
                "orderItems": 4,
                "OrderId": 1,
                "ItemId": 1,
                "Quantity": 1.0,
                "SpecialInstruct": "",
                "DeliveryInstruct": "",
            },
            {
                "orderItems": 5,
                "OrderId": 1,
                "ItemId": 3,
                "Quantity": 2.0,
                "SpecialInstruct": "",
                "DeliveryInstruct": "",
            },
        ],
        "CurrentOrder": [
            {"COrderId": 7001, "OrderId": 5001, "DelivererId": None},
            {"COrderId": 7002, "OrderId": 5002, "DelivererId": 14},
            {"COrderId": 7003, "OrderId": 1, "DelivererId": None},
        ],
        "PastOrders": [
            {"POrderId": 9001, "OrderId": 4001},
        ],
        "UnclaimedOrders": [
            {"UOrderId": 8001, "OrderId": 5001},
        ],
        "next_order_item_id": 6,
    }


MOCK_DB = _mock_state()


def reset_mock_db() -> None:
    global MOCK_DB
    MOCK_DB = _mock_state()


def _find_item(item_id: int) -> dict:
    for item in MOCK_DB["Items"]:
        if item["ItemId"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


def _find_order(order_id: int) -> dict:
    for order in MOCK_DB["Orders"]:
        if order["orderId"] == order_id:
            return order
    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")


def _find_dining_hall(dh_id: int) -> dict:
    for hall in MOCK_DB["Dininghalls"]:
        if hall["DhId"] == dh_id:
            return hall
    raise HTTPException(status_code=404, detail=f"Dining hall {dh_id} not found")


def _find_current_order(order_id: int) -> dict:
    for current_order in MOCK_DB["CurrentOrder"]:
        if current_order["OrderId"] == order_id:
            return current_order
    raise HTTPException(status_code=404, detail=f"Current order for {order_id} not found")


def _find_deliverer_profile(deliverer_id: int) -> dict:
    for profile in MOCK_DB["delivererProfile"]:
        if profile["DelivererId"] == deliverer_id:
            return profile
    raise HTTPException(status_code=404, detail=f"Deliverer {deliverer_id} not found")


def _cart_order(cart_id: int) -> dict:
    order = _find_order(cart_id)
    if order["OrderStatus"] != "cart":
        raise HTTPException(status_code=404, detail=f"Cart {cart_id} not found")
    return order


def _order_items(order_id: int) -> list[dict]:
    return [
        order_item
        for order_item in MOCK_DB["OrderItems"]
        if order_item["OrderId"] == order_id
    ]


def _recalculate_order_total(order_id: int) -> None:
    order = _find_order(order_id)
    total = 0.0
    for order_item in _order_items(order_id):
        item = _find_item(order_item["ItemId"])
        total += item["Price"] * order_item["Quantity"]
    order["TotalPrice"] = round(total, 2)


def _serialize_cart(order: dict) -> dict:
    items = []
    for order_item in _order_items(order["orderId"]):
        item = _find_item(order_item["ItemId"])
        subtotal = round(item["Price"] * order_item["Quantity"], 2)
        items.append(
            {
                "cartItemId": order_item["orderItems"],
                "itemId": item["ItemId"],
                "name": item["ItemName"],
                "quantity": int(order_item["Quantity"]),
                "price": item["Price"],
                "subtotal": subtotal,
                "specialInstructions": order_item["SpecialInstruct"],
                "deliveryInstructions": order_item["DeliveryInstruct"],
            }
        )

    return {
        "cartId": order["orderId"],
        "customerId": order["userId"],
        "diningHallId": order["DhId"],
        "items": items,
        "total": order["TotalPrice"],
        "schemaSource": {
            "orderTable": "Orders",
            "lineItemTable": "OrderItems",
            "currentOrderTable": "CurrentOrder",
        },
    }


def _serialize_order(order: dict) -> dict:
    current_order = _find_current_order(order["orderId"])
    hall = _find_dining_hall(order["DhId"])
    items = []

    for order_item in _order_items(order["orderId"]):
        item = _find_item(order_item["ItemId"])
        items.append(
            {
                "orderItems": order_item["orderItems"],
                "itemId": item["ItemId"],
                "itemName": item["ItemName"],
                "quantity": order_item["Quantity"],
                "specialInstructions": order_item["SpecialInstruct"],
                "deliveryInstructions": order_item["DeliveryInstruct"],
            }
        )

    return {
        "orderId": order["orderId"],
        "userId": order["userId"],
        "delivererId": current_order["DelivererId"],
        "diningHall": hall["DhName"],
        "status": order["OrderStatus"],
        "totalPrice": order["TotalPrice"],
        "orderTime": order["OrderTime"],
        "items": items,
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "backend": "healthy"}


@app.get("/")
def root() -> dict:
    return {
        "message": "Grab & Go API",
        "implementationOrder": [
            "Validate request and ids",
            "Run SQL query against schema tables or mock rows",
            "Return JSON payload for the Vue client",
        ],
        "mockSchemaTables": [
            "Users",
            "delivererProfile",
            "Dininghalls",
            "DininghallsItems",
            "Items",
            "Orders",
            "OrderItems",
            "CurrentOrder",
            "PastOrders",
            "UnclaimedOrders",
        ],
    }


@app.post("/customer/cart/{cartId}/item/{itemId}")
def add_item_cart(cartId: int, itemId: int) -> dict:
    order = _cart_order(cartId)
    _find_item(itemId)

    for order_item in _order_items(order["orderId"]):
        if order_item["ItemId"] == itemId:
            order_item["Quantity"] += 1.0
            _recalculate_order_total(order["orderId"])
            return {
                "message": "Item quantity increased",
                "cart": _serialize_cart(order),
            }

    MOCK_DB["OrderItems"].append(
        {
            "orderItems": MOCK_DB["next_order_item_id"],
            "OrderId": order["orderId"],
            "ItemId": itemId,
            "Quantity": 1.0,
            "SpecialInstruct": "",
            "DeliveryInstruct": "",
        }
    )
    MOCK_DB["next_order_item_id"] += 1
    _recalculate_order_total(order["orderId"])
    return {"message": "Item added to cart", "cart": _serialize_cart(order)}


@app.get("/customer/cart/{cartId}")
def get_item(cartId: int) -> dict:
    order = _cart_order(cartId)
    return _serialize_cart(order)


@app.delete("/customer/cart/{itemId}")
def delete_item(itemId: int) -> dict:
    for order_item in list(MOCK_DB["OrderItems"]):
        order = _find_order(order_item["OrderId"])
        if order_item["orderItems"] == itemId and order["OrderStatus"] == "cart":
            MOCK_DB["OrderItems"].remove(order_item)
            _recalculate_order_total(order["orderId"])
            return {
                "message": "Item removed from cart",
                "cart": _serialize_cart(order),
            }

    raise HTTPException(status_code=404, detail=f"Cart item {itemId} not found")


@app.patch("/customer/cart/{cartId}/item/{itemId}")
def update_cart(cartId: int, itemId: int, payload: CartItemUpdate) -> dict:
    order = _cart_order(cartId)

    for order_item in _order_items(order["orderId"]):
        if order_item["ItemId"] == itemId:
            order_item["Quantity"] = float(payload.quantity)
            _recalculate_order_total(order["orderId"])
            return {
                "message": "Cart item updated",
                "cart": _serialize_cart(order),
            }

    raise HTTPException(
        status_code=404,
        detail=f"Item {itemId} is not currently in cart {cartId}",
    )


@app.get("/customer/dininghalls")
def get_dininghalls() -> dict:
    return {"diningHalls": deepcopy(MOCK_DB["Dininghalls"])}


@app.get("/customer/dininghalls/items/{DhId}")
def get_dinninghall_items(DhId: int) -> dict:
    hall = _find_dining_hall(DhId)
    rows = [
        row
        for row in MOCK_DB["DininghallsItems"]
        if row["DhId"] == DhId and row["IsAvailable"]
    ]
    items = []
    for row in rows:
        item = _find_item(row["ItemId"])
        items.append(
            {
                "DhItemeId": row["DhItemeId"],
                "DhId": row["DhId"],
                "ItemId": item["ItemId"],
                "ItemName": item["ItemName"],
                "Price": item["Price"],
                "IsSnack": item["IsSnack"],
                "Allergy": item["Allergy"],
                "MealType": item["MealType"],
                "DietaryType": item["DietaryType"],
                "IsAvailable": row["IsAvailable"],
            }
        )

    return {"diningHall": deepcopy(hall), "items": items}


@app.get("/deliverer/orders")
def get_orders() -> dict:
    return {
        "orders": [
            _serialize_order(_find_order(row["OrderId"]))
            for row in MOCK_DB["UnclaimedOrders"]
        ]
    }


@app.put("/deliverer/claim/{delivererId}/order/{orderId}")
def update_delivever_order(delivererId: int, orderId: int) -> dict:
    _find_deliverer_profile(delivererId)
    order = _find_order(orderId)
    current_order = _find_current_order(orderId)

    if current_order["DelivererId"] is not None and current_order["DelivererId"] != delivererId:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Order {orderId} is already claimed by deliverer "
                f"{current_order['DelivererId']}"
            ),
        )

    current_order["DelivererId"] = delivererId
    order["OrderStatus"] = "claimed"

    MOCK_DB["UnclaimedOrders"] = [
        row for row in MOCK_DB["UnclaimedOrders"] if row["OrderId"] != orderId
    ]

    profile = _find_deliverer_profile(delivererId)
    profile["COrderId"] = current_order["COrderId"]

    return {"message": "Order claimed", "order": _serialize_order(order)}


@app.get("/deliverer/order/{orderId}")
def get_order(orderId: int) -> dict:
    order = _find_order(orderId)
    return _serialize_order(order)


@app.post("/deliverer/past-orders/{delivererId}/order/{orderId}")
def update_past_order(delivererId: int, orderId: int) -> dict:
    profile = _find_deliverer_profile(delivererId)
    order = _find_order(orderId)
    current_order = _find_current_order(orderId)

    if current_order["DelivererId"] != delivererId:
        raise HTTPException(
            status_code=403,
            detail=f"Deliverer {delivererId} cannot close order {orderId}",
        )

    order["OrderStatus"] = "delivered"
    next_past_order_id = (
        max((row["POrderId"] for row in MOCK_DB["PastOrders"]), default=9000) + 1
    )
    MOCK_DB["PastOrders"].append({"POrderId": next_past_order_id, "OrderId": orderId})
    profile["POrderId"] = next_past_order_id
    profile["COrderId"] = None

    return {"message": "Order archived", "order": _serialize_order(order)}
