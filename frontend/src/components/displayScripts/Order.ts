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

/** Set when a deliverer claims an order; used on the landing page for status updates. */
export const delivererCurrentOrder = ref<Order | null>(null)
export const delivererCurrentOrderLoading = ref(false)
export const delivererCurrentOrderError = ref<string | null>(null)

const API_BASE = 'http://localhost:8000'
const DELIVERER_CURRENT_ORDER_KEY = 'delivererCurrentOrder'

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

type OrderResponse = {
  order?: RawOrder
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

export function isActiveDelivererOrder(order: Order): boolean {
  return order.status === 'claimed' || order.status === 'on the way'
}

function readStoredCurrentOrder(): Order | null {
  const storedOrder = window.localStorage.getItem(DELIVERER_CURRENT_ORDER_KEY)
  if (!storedOrder) {
    return null
  }

  try {
    return convertOrder(JSON.parse(storedOrder) as RawOrder)
  } catch {
    window.localStorage.removeItem(DELIVERER_CURRENT_ORDER_KEY)
    return null
  }
}

export function setDelivererCurrentOrder(order: Order | null): void {
  delivererCurrentOrder.value = order

  if (order) {
    window.localStorage.setItem(DELIVERER_CURRENT_ORDER_KEY, JSON.stringify(order))
  } else {
    window.localStorage.removeItem(DELIVERER_CURRENT_ORDER_KEY)
  }
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

export async function fetchDelivererCurrentOrder(): Promise<void> {
  delivererCurrentOrderLoading.value = true
  delivererCurrentOrderError.value = null

  try {
    const response = await fetch(`${API_BASE}/api/orders`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = (await response.json()) as { orders?: RawOrder[] }
    const activeOrder = (data.orders ?? [])
      .map((order) => convertOrder(order))
      .find(isActiveDelivererOrder) ?? null

    setDelivererCurrentOrder(activeOrder)
  } catch (error) {
    const storedOrder = readStoredCurrentOrder()
    if (storedOrder && isActiveDelivererOrder(storedOrder)) {
      delivererCurrentOrder.value = storedOrder
    } else {
      setDelivererCurrentOrder(null)
    }
    delivererCurrentOrderError.value =
      error instanceof Error ? error.message : 'Failed to fetch active order.'
  } finally {
    delivererCurrentOrderLoading.value = false
  }
}

export async function claimOrder(orderId: number): Promise<Order> {
  const response = await fetch(`${API_BASE}/api/orders/claim/${orderId}`, {
    method: 'POST',
  })

  if (!response.ok) {
    const data = await response.json().catch(() => null)
    throw new Error(data?.detail ?? `Failed to claim order: ${response.status}`)
  }

  const data = (await response.json()) as OrderResponse
  if (!data.order) {
    throw new Error('Claim response did not include an order.')
  }

  const claimedOrder = convertOrder(data.order)
  setDelivererCurrentOrder(claimedOrder)
  return claimedOrder
}

export async function updateOrderStatus(orderId: number, status: string): Promise<Order> {
  const response = await fetch(`${API_BASE}/api/orders/${orderId}/status`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(status),
  })

  if (!response.ok) {
    const data = await response.json().catch(() => null)
    throw new Error(data?.detail ?? `Failed to update order status: ${response.status}`)
  }

  const data = (await response.json()) as OrderResponse
  if (!data.order) {
    throw new Error('Status response did not include an order.')
  }

  const updatedOrder = convertOrder(data.order)
  setDelivererCurrentOrder(isActiveDelivererOrder(updatedOrder) ? updatedOrder : null)
  return updatedOrder
}


export const pastOrders = ref<Order[]>([])
export const pastOrdersLoading = ref(false)
export async function fetchPastOrders(): Promise<void> {
  pastOrdersLoading.value = true
  try {
    const response = await fetch(`${API_BASE}/api/orders`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = (await response.json()) as { orders?: RawOrder[] }
    pastOrders.value = (data.orders ?? []).map((order) => convertOrder(order))
    .filter((order) => order.status === 'delivered')
  } catch (error) {
    pastOrders.value = []
  }finally {
    pastOrdersLoading.value = false
  }
}