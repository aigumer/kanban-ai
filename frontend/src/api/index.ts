import type { Board, Column, Card } from '../types'
import { mockBoard, mockColumns, mockCards, getNextCardId } from './mockData'

const delay = (ms = 80) => new Promise((r) => setTimeout(r, ms))

function findCardsByColumn(columnId: number): Card[] {
  return mockCards
    .filter((c) => c.column_id === columnId)
    .sort((a, b) => a.position - b.position)
}

export const api = {
  async getBoard(): Promise<Board> {
    await delay()
    return { ...mockBoard }
  },

  async getColumns(): Promise<Column[]> {
    await delay()
    return mockColumns.map((c) => ({ ...c }))
  },

  async getCards(columnId?: number): Promise<Card[]> {
    await delay()
    const cards = columnId !== undefined ? findCardsByColumn(columnId) : [...mockCards]
    return cards.map((c) => ({ ...c }))
  },

  async createCard(data: {
    column_id: number
    title: string
    description?: string | null
  }): Promise<Card> {
    await delay()
    const colCards = findCardsByColumn(data.column_id)
    const card: Card = {
      id: getNextCardId(),
      column_id: data.column_id,
      title: data.title,
      description: data.description ?? null,
      position: colCards.length,
      timer_seconds: 0,
      timer_running: false,
      timer_started_at: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    mockCards.push(card)
    return { ...card }
  },

  async updateCard(
    id: number,
    data: Partial<Pick<Card, 'title' | 'description' | 'position' | 'column_id'>>,
  ): Promise<Card> {
    await delay()
    const card = mockCards.find((c) => c.id === id)
    if (!card) throw new Error(`Card ${id} not found`)
    Object.assign(card, data, { updated_at: new Date().toISOString() })
    return { ...card }
  },

  async deleteCard(id: number): Promise<void> {
    await delay()
    const idx = mockCards.findIndex((c) => c.id === id)
    if (idx === -1) throw new Error(`Card ${id} not found`)
    mockCards.splice(idx, 1)
  },

  async startTimer(id: number): Promise<Card> {
    await delay()
    const card = mockCards.find((c) => c.id === id)
    if (!card) throw new Error(`Card ${id} not found`)
    card.timer_running = true
    card.timer_started_at = new Date().toISOString()
    card.updated_at = new Date().toISOString()
    return { ...card }
  },

  async stopTimer(id: number): Promise<Card> {
    await delay()
    const card = mockCards.find((c) => c.id === id)
    if (!card) throw new Error(`Card ${id} not found`)
    if (card.timer_running && card.timer_started_at) {
      const elapsed = Math.floor(
        (Date.now() - new Date(card.timer_started_at).getTime()) / 1000,
      )
      card.timer_seconds += elapsed
    }
    card.timer_running = false
    card.timer_started_at = null
    card.updated_at = new Date().toISOString()
    return { ...card }
  },

  async moveCard(
    cardId: number,
    toColumnId: number,
    newPosition: number,
  ): Promise<Card> {
    await delay()
    const card = mockCards.find((c) => c.id === cardId)
    if (!card) throw new Error(`Card ${cardId} not found`)

    const oldColumnCards = findCardsByColumn(card.column_id).filter(
      (c) => c.id !== cardId,
    )
    oldColumnCards.forEach((c, i) => (c.position = i))

    card.column_id = toColumnId
    card.position = newPosition
    card.updated_at = new Date().toISOString()

    const newColumnCards = findCardsByColumn(toColumnId).filter(
      (c) => c.id !== cardId,
    )
    newColumnCards.splice(newPosition, 0, card)
    newColumnCards.forEach((c, i) => (c.position = i))

    return { ...card }
  },
}
