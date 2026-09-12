<script setup lang="ts">
import { ref, onMounted } from 'vue'
import KanbanColumn from './KanbanColumn.vue'
import type { Board, Column } from '../types'
import { api } from '../api'

const board = ref<Board | null>(null)
const columns = ref<Column[]>([])
const columnRefs = ref<InstanceType<typeof KanbanColumn>[]>([])

async function loadBoard() {
  board.value = await api.getBoard()
  columns.value = await api.getColumns()
}

onMounted(loadBoard)

function refreshColumns() {
  columnRefs.value.forEach((col) => col?.loadCards())
}
</script>

<template>
  <div class="board-wrapper">
    <header class="board-header">
      <h1>{{ board?.name ?? 'Loading...' }}</h1>
    </header>
    <div class="board-columns">
      <KanbanColumn
        v-for="col in columns"
        :key="col.id"
        :column="col"
        ref="columnRefs"
        @card-updated="refreshColumns"
      />
    </div>
  </div>
</template>

<style scoped>
.board-wrapper {
  min-height: 100vh;
  background: #f1f5f9;
  padding: 24px;
}

.board-header {
  margin-bottom: 24px;
}

.board-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.board-columns {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  overflow-x: auto;
  padding-bottom: 16px;
}

@media (max-width: 768px) {
  .board-wrapper {
    padding: 16px;
  }

  .board-columns {
    flex-direction: column;
    align-items: stretch;
  }

  .board-columns > :deep(.kanban-column) {
    max-width: none;
    min-width: 0;
  }
}
</style>
