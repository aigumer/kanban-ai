<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import draggable from 'vuedraggable'
import KanbanCard from './KanbanCard.vue'
import type { Column, Card } from '../types'
import { api } from '../api'

const props = defineProps<{ column: Column }>()
const emit = defineEmits<{
  'card-updated': []
}>()

const cards = ref<Card[]>([])
const showModal = ref(false)
const editingCard = ref<Card | null>(null)
const drag = ref(false)

async function loadCards() {
  cards.value = await api.getCards(props.column.id)
}

onMounted(loadCards)

let timerInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  timerInterval = setInterval(() => {
    cards.value = [...cards.value]
  }, 1000)
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

async function handleDragEnd() {
  drag.value = false
  for (let i = 0; i < cards.value.length; i++) {
    const card = cards.value[i]
    if (card.position !== i || card.column_id !== props.column.id) {
      await api.moveCard(card.id, props.column.id, i)
    }
  }
  emit('card-updated')
}

function openCreateModal() {
  editingCard.value = null
  showModal.value = true
}

function openEditModal(card: Card) {
  editingCard.value = card
  showModal.value = true
}

async function handleSave(data: { title: string; description: string }) {
  if (editingCard.value) {
    await api.updateCard(editingCard.value.id, data)
  } else {
    await api.createCard({ column_id: props.column.id, ...data })
  }
  showModal.value = false
  await loadCards()
  emit('card-updated')
}

async function handleDelete(id: number) {
  await api.deleteCard(id)
  await loadCards()
  emit('card-updated')
}

async function handleStartTimer(id: number) {
  await api.startTimer(id)
  await loadCards()
}

async function handleStopTimer(id: number) {
  await api.stopTimer(id)
  await loadCards()
}

defineExpose({ loadCards })
</script>

<template>
  <div class="kanban-column">
    <div class="column-header">
      <h3>{{ column.name }}</h3>
      <span class="card-count">{{ cards.length }}</span>
    </div>
    <draggable
      v-model="cards"
      group="cards"
      item-key="id"
      ghost-class="ghost"
      drag-class="dragging"
      :animation="200"
      @start="drag = true"
      @end="handleDragEnd"
    >
      <template #item="{ element }">
        <KanbanCard
          :card="element"
          @edit="openEditModal"
          @delete="handleDelete"
          @start-timer="handleStartTimer"
          @stop-timer="handleStopTimer"
        />
      </template>
    </draggable>
    <button class="add-card-btn" @click="openCreateModal">
      <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
      </svg>
      Add card
    </button>
    <CardModal
      :card="editingCard"
      :visible="showModal"
      @save="handleSave"
      @close="showModal = false"
    />
  </div>
</template>

<style scoped>
.kanban-column {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  min-width: 300px;
  max-width: 340px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 0 4px;
}

.column-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-count {
  background: #e2e8f0;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 10px;
}

.add-card-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 10px;
  margin-top: 4px;
  background: none;
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.add-card-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

:deep(.ghost) {
  opacity: 0.4;
  background: #e2e8f0;
  border-radius: 8px;
}

:deep(.dragging) {
  opacity: 0.9;
  transform: rotate(2deg);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
</style>
