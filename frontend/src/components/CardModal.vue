<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Card } from '../types'

const props = defineProps<{
  card: Card | null
  visible: boolean
}>()

const emit = defineEmits<{
  save: [data: { title: string; description: string }]
  close: []
}>()

const title = ref('')
const description = ref('')

watch(
  () => props.card,
  (c) => {
    title.value = c?.title ?? ''
    description.value = c?.description ?? ''
  },
  { immediate: true },
)

function handleSubmit() {
  if (!title.value.trim()) return
  emit('save', {
    title: title.value.trim(),
    description: description.value.trim(),
  })
}
</script>

<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click.self="emit('close')">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ card ? 'Edit Card' : 'New Card' }}</h3>
          <button class="btn-close" @click="emit('close')">&times;</button>
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="card-title">Title</label>
            <input
              id="card-title"
              v-model="title"
              type="text"
              placeholder="Enter card title..."
              autofocus
            />
          </div>
          <div class="form-group">
            <label for="card-desc">Description (optional)</label>
            <textarea
              id="card-desc"
              v-model="description"
              rows="3"
              placeholder="Add a description..."
            ></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="emit('close')">Cancel</button>
            <button type="submit" class="btn-primary" :disabled="!title.trim()">
              {{ card ? 'Save' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 440px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #1e293b;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #94a3b8;
  padding: 0;
  line-height: 1;
}

.btn-close:hover {
  color: #475569;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 6px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  color: #1e293b;
  box-sizing: border-box;
  transition: border-color 0.15s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 20px;
}

.btn-secondary {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #f8fafc;
}

.btn-primary {
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  background: #3b82f6;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
