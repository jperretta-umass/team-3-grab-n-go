

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

// Mock data for fallback/testing when API is unavailable
const MOCK_ITEMS: MenuItem[] = [
  {
    id: 1,
    name: 'Grilled Chicken Bowl',
    mealType: ['lunch', 'dinner'],
    diets: ['gluten-free'],
    category: 'entree',
    diningHall: 'Hampshire',
    price: 13.25,
  },
  {
    id: 2,
    name: 'Vegetarian Pasta',
    mealType: ['lunch', 'dinner'],
    diets: ['vegetarian', 'vegan'],
    category: 'entree',
    diningHall: 'Berkshire',
    price: 12.50,
  },
  {
    id: 3,
    name: 'Caesar Salad',
    mealType: ['lunch'],
    diets: ['vegetarian', 'gluten-free'],
    category: 'entree',
    diningHall: 'Franklin',
    price: 11.00,
  },
  {
    id: 101,
    name: 'Fruit Cup',
    mealType: ['breakfast', 'lunch'],
    diets: ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
    category: 'snack',
    diningHall: 'Hampshire',
    price: 3.00,
  },
  {
    id: 102,
    name: 'Greek Yogurt',
    mealType: ['breakfast'],
    diets: ['vegetarian', 'gluten-free'],
    category: 'snack',
    diningHall: 'Berkshire',
    price: 2.50,
  },
  {
    id: 103,
    name: 'Lemonade',
    mealType: ['breakfast'],
    diets: ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
    category: 'drink',
    diningHall: 'Hampshire',
    price: 2.00,
  },
  {
    id: 104,
    name: 'Iced Tea',
    mealType: ['lunch', 'dinner'],
    diets: ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
    category: 'drink',
    diningHall: 'Berkshire',
    price: 2.00,
  },
  {
    id: 105,
    name: 'Yogurt Cup',
    mealType: ['breakfast', 'lunch'],
    diets: ['vegetarian', 'gluten-free'],
    category: 'snack',
    diningHall: 'Hampshire',
    price: 2.50,
  },
  {
    id: 106,
    name: 'Trail Mix',
    mealType: ['lunch', 'dinner'],
    diets: ['vegetarian'],
    category: 'snack',
    diningHall: 'Hampshire',
    price: 4.00,
  },
  {
    id: 107,
    name: 'Sparkling Water',
    mealType: ['breakfast', 'lunch', 'dinner'],
    diets: ['vegan', 'gluten-free', 'vegetarian', 'no-peanuts'],
    category: 'drink',
    diningHall: 'Hampshire',
    price: 2.50,
  },
]

export const cart = ref<CartItem[]>([])
let nextCartId = 0

function convert(data: Record<string, unknown>): MenuItem {
  return {
    id: data.id as number,
    name: data.name as string,
    mealType: (data.mealType as MealType[] | undefined) ?? [],
    diets: (data.diets as DietType[] | undefined) ?? [],
    category: data.category as 'entree' | 'snack' | 'drink',
    diningHall: data.dining_hall as DiningHall,
    price: data.price as number
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
      items.value = list.map((item: Record<string, unknown>) => convert(item))
    } catch (err: unknown) {
      const typedErr = err as Error
      error.value = typedErr.message || 'Failed to fetch menu items. Using mock data.'
      items.value = MOCK_ITEMS
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
  return cart.value.reduce((total: number, item: { price: number }) => total + item.price, 0).toFixed(2)
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