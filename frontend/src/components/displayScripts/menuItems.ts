import { computed, ref } from 'vue'

export type MealType = 'breakfast' | 'lunch' | 'dinner'
export type DietType = 'no-peanuts' | 'vegan' | 'gluten-free' | 'vegetarian'
export type DiningHall = 'Hampshire' | 'Berkshire' | 'Franklin' | 'Worcester' 

export type MenuItem = {
  id: number
  name: string
  mealType: MealType[]
  diets: DietType[]
  category: 'entree' | 'snack' | 'drink'
  diningHall: DiningHall
  price: number
}

export type CartItem = {
  cartId: number
  id: number
  name: string
  price: number
}

export const items = ref<MenuItem[]>([])
export const loading = ref(true)
export const error = ref<string | null>(null)

export const selectedMeal = ref('')
export const selectedDiet = ref('')
export const selectedHall = ref('Hampshire')
const API_BASE = 'http://localhost:8000' // Change this to your backend URL if different

export const cart = ref<CartItem[]>([])
let nextCartId = 0

function convert(data: any): MenuItem {
  return {
    id: data.id,
    name: data.name,
    mealType: data.mealType ?? [],
    diets: data.diets ?? [],
    category: data.category,
    diningHall: data.dining_hall as DiningHall,
    price: data.price
  }
}

export async function fetchMenuItems(): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE}/api/menu-items`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      const list = data.menu_items ?? []
      items.value = list.map((item: any) => convert(item))
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch menu items.'
      items.value = []
    } finally {
      loading.value = false
    }
}

export const entrees = computed(() => items.value.filter((item => item.category === 'entree')))
export const snacksAndDrinks = computed(() => items.value.filter((item => item.category !== 'entree')))
export const diningHalls = computed(() => {
  const halls = new Set(items.value.map(item => item.diningHall))
  return Array.from(halls)
})


function matchesFilters(item: MenuItem): boolean {
  const mealMatches =
    !selectedMeal.value || item.mealType.includes(selectedMeal.value as MealType)

  const dietMatches =
    !selectedDiet.value || item.diets.includes(selectedDiet.value as DietType)

  const hallMatches = !selectedHall.value || item.diningHall === selectedHall.value
  return mealMatches && dietMatches && hallMatches
}

export const filteredEntrees = computed(() => {
  return entrees.value.filter(matchesFilters)
})

export const filteredSnacksAndDrinks = computed(() => {
  return snacksAndDrinks.value.filter(matchesFilters)
})

export const cartTotal = computed(() => {
  return cart.value.reduce((total: any, item: { price: any; }) => total + item.price, 0).toFixed(2)
})

export function addToCart(item: MenuItem): void {
  cart.value.push({
    cartId: nextCartId++,
    id: item.id,
    name: item.name,
    price: item.price
  })
}

export function removeFromCart(cartId: number): void {
  cart.value = cart.value.filter((item: { cartId: number; }) => item.cartId !== cartId)
}

export function formatTags(item: MenuItem): string {
  const meals = item.mealType.join(', ')
  const diets = item.diets.length ? item.diets.join(', ') : 'none'
  return `Meal: ${meals} | Diet: ${diets}`
}