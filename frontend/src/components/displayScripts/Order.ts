import { ref } from 'vue'

export type OrderItem = {
  menu_item_id: number
  quantity: number
}

export class Order {
  id: number
  user_id: number
  dining_hall_id: number
  dining_hall: string
  delivery_address: string
  total_price: number
  status: string
  created_at: string
  items: OrderItem[]

  constructor(
    id: number,
    user_id: number,
    dining_hall_id: number,
    dining_hall: string,
    delivery_address: string,
    total_price: number,
    status: string,
    created_at: string,
    items: OrderItem[]
  ) {
    this.id = id
    this.user_id = user_id
    this.dining_hall_id = dining_hall_id
    this.dining_hall = dining_hall
    this.delivery_address = delivery_address
    this.total_price = total_price
    this.status = status
    this.created_at = created_at
    this.items = items
  }
}

export type OrdersResponse = {
  orders: Order[]
}

export const orders = ref<Order[]>([])
export const ordersLoading = ref(true)
export const ordersError = ref<string | null>(null)

const API_BASE = 'http://localhost:8000'

type RawOrderItem = {
  menu_item_id: number
  quantity: number
}

type RawOrder = {
  id: number
  user_id: number
  dining_hall_id: number
  dining_hall: string
  delivery_address: string
  total_price: number
  status: string
  created_at: string
  items?: RawOrderItem[]
}

export function convertOrder(data: RawOrder): Order {
  return new Order(
    data.id,
    data.user_id,
    data.dining_hall_id,
    data.dining_hall,
    data.delivery_address,
    data.total_price,
    data.status,
    data.created_at,
    (data.items ?? []).map((item: RawOrderItem) => ({
      menu_item_id: item.menu_item_id,
      quantity: item.quantity,
    }))
  )
}

export function onlyUnclaimed (order: Order): boolean {
  return (order.status === "unclaimed")
}

export async function fetchOrders(): Promise<void> {
  ordersLoading.value = true
  ordersError.value = null
  try {
    const response = await fetch(`${API_BASE}/api/orders`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = (await response.json()) as { orders?: RawOrder[] }
    orders.value = (data.orders ?? []).map((order) => convertOrder(order)).filter(onlyUnclaimed)
  } catch (error) {
    ordersError.value = error instanceof Error ? error.message : 'Failed to fetch orders.'
    orders.value = []
  } finally {
    ordersLoading.value = false
  }
}

export async function claimOrder(orderId: number): Promise<void> {
  const response = await fetch(`${API_BASE}/api/orders/claim/${orderId}`, {
    method: 'POST',
  })

  if (!response.ok) {
    const data = await response.json().catch(() => null)
    throw new Error(data?.detail ?? `Failed to claim order: ${response.status}`)
  }
}