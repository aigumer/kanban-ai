export interface Board {
  id: number
  name: string
  created_at: string
}

export interface Column {
  id: number
  board_id: number
  name: string
  position: number
}

export interface Card {
  id: number
  column_id: number
  title: string
  description: string | null
  position: number
  timer_seconds: number
  timer_running: boolean
  timer_started_at: string | null
  created_at: string
  updated_at: string
}
