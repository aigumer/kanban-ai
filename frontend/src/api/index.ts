import type { Board, Column, Card } from '../types'

const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText)
    throw new Error(`${res.status} ${text}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  getBoard: () => request<Board>('/board'),

  getColumns: () => request<Column[]>('/columns'),

  getCards: (columnId?: number) => {
    const qs = columnId !== undefined ? `?column_id=${columnId}` : ''
    return request<Card[]>(`/cards${qs}`)
  },

  createCard: (data: { column_id: number; title: string; description?: string | null }) =>
    request<Card>('/cards', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateCard: (
    id: number,
    data: Partial<Pick<Card, 'title' | 'description' | 'position' | 'column_id'>>,
  ) =>
    request<Card>(`/cards/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  deleteCard: (id: number) =>
    request<void>(`/cards/${id}`, { method: 'DELETE' }),

  startTimer: (id: number) =>
    request<Card>(`/cards/${id}/timer/start`, { method: 'POST' }),

  stopTimer: (id: number) =>
    request<Card>(`/cards/${id}/timer/stop`, { method: 'POST' }),

  moveCard: (cardId: number, toColumnId: number, newPosition: number) =>
    request<Card>(`/cards/${cardId}`, {
      method: 'PATCH',
      body: JSON.stringify({ column_id: toColumnId, position: newPosition }),
    }),
}
