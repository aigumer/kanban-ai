<script setup lang="ts">
import { computed } from 'vue'
import type { Card } from '../types'

const props = defineProps<{ card: Card }>()
const emit = defineEmits<{
  edit: [card: Card]
  delete: [id: number]
  startTimer: [id: number]
  stopTimer: [id: number]
}>()

function formatTime(seconds: number): string {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  return [h, m, s].map((v) => String(v).padStart(2, '0')).join(':')
}

const liveSeconds = computed(() => {
  if (!props.card.timer_running || !props.card.timer_started_at) {
    return props.card.timer_seconds
  }
  const elapsed = Math.floor(
    (Date.now() - new Date(props.card.timer_started_at).getTime()) / 1000,
  )
  return props.card.timer_seconds + elapsed
})
</script>

<template>
  <div class="kanban-card" :class="{ 'timer-active': card.timer_running }">
    <div class="card-header">
      <h4 class="card-title">{{ card.title }}</h4>
      <div class="card-actions">
        <button class="btn-icon" @click="emit('edit', card)" title="Edit">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
          </svg>
        </button>
        <button class="btn-icon btn-danger" @click="emit('delete', card.id)" title="Delete">
          <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>
    </div>
    <p v-if="card.description" class="card-description">{{ card.description }}</p>
    <div class="card-footer">
      <span class="timer" :class="{ running: card.timer_running }">
        <svg viewBox="0 0 20 20" fill="currentColor" width="12" height="12">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
        </svg>
        {{ formatTime(liveSeconds) }}
      </span>
      <button
        class="btn-timer"
        :class="card.timer_running ? 'stop' : 'start'"
        @click="card.timer_running ? emit('stopTimer', card.id) : emit('startTimer', card.id)"
      >
        {{ card.timer_running ? 'Stop' : 'Start' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.kanban-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  cursor: grab;
  transition: box-shadow 0.15s, border-color 0.15s;
}

.kanban-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

.kanban-card:active {
  cursor: grabbing;
}

.kanban-card.timer-active {
  border-color: #3b82f6;
  background: #f0f7ff;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.card-title {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
  flex: 1;
}

.card-actions {
  display: flex;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.15s;
}

.kanban-card:hover .card-actions {
  opacity: 1;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background: #f1f5f9;
  color: #334155;
}

.btn-icon.btn-danger:hover {
  background: #fef2f2;
  color: #dc2626;
}

.card-description {
  margin: 8px 0 0;
  font-size: 12px;
  color: #64748b;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #f1f5f9;
}

.timer {
  font-size: 12px;
  font-family: 'SF Mono', 'Fira Code', monospace;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 4px;
}

.timer.running {
  color: #3b82f6;
  font-weight: 600;
}

.btn-timer {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-timer.start {
  background: #dcfce7;
  color: #16a34a;
}

.btn-timer.start:hover {
  background: #bbf7d0;
}

.btn-timer.stop {
  background: #fee2e2;
  color: #dc2626;
}

.btn-timer.stop:hover {
  background: #fecaca;
}
</style>
