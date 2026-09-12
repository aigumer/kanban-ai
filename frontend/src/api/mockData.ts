import type { Board, Column, Card } from '../types'

let nextCardId = 1

export const mockBoard: Board = {
  id: 1,
  name: 'My Board',
  created_at: new Date().toISOString(),
}

export const mockColumns: Column[] = [
  { id: 1, board_id: 1, name: 'To Do', position: 0 },
  { id: 2, board_id: 1, name: 'In Progress', position: 1 },
  { id: 3, board_id: 1, name: 'Done', position: 2 },
]

export const mockCards: Card[] = [
  {
    id: nextCardId++,
    column_id: 1,
    title: 'Design homepage layout',
    description: 'Create wireframes for the main landing page',
    position: 0,
    timer_seconds: 0,
    timer_running: false,
    timer_started_at: null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: nextCardId++,
    column_id: 1,
    title: 'Set up CI/CD pipeline',
    description: null,
    position: 1,
    timer_seconds: 300,
    timer_running: false,
    timer_started_at: null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: nextCardId++,
    column_id: 2,
    title: 'Implement authentication',
    description: 'OAuth2 with Google and GitHub',
    position: 0,
    timer_seconds: 1250,
    timer_running: true,
    timer_started_at: new Date(Date.now() - 60000).toISOString(),
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: nextCardId++,
    column_id: 3,
    title: 'Project scaffolding',
    description: null,
    position: 0,
    timer_seconds: 450,
    timer_running: false,
    timer_started_at: null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
]

export function getNextCardId(): number {
  return nextCardId++
}
