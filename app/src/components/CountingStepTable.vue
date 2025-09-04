<script setup>
import { ref, watch } from 'vue'
import { counterApi } from '@/services/counterApi'
import { formatDateBrl } from '@/helpers/formatters'

const props = defineProps({
  visible: Boolean,
  counterId: {
    type: [String, Number],
    required: true
  }
})

const steps = ref([])
const loading = ref(false)

const fetchSteps = async () => {
  if (!props.counterId) return
  loading.value = true
  try {
    const res = await counterApi.get(props.counterId)
    if (res.status === 200) {
      steps.value = res.data.counting_steps || []
    }
  } catch (err) {
    console.error('Erro ao buscar passos da contagem:', err)
  } finally {
    loading.value = false
  }
}

watch(() => props.visible, (val) => {
  if (val) fetchSteps()
})
</script>

<template>
  <div
    class="modal fade"
    tabindex="-1"
    :class="{ show: visible }"
    :style="{ display: visible ? 'block' : 'none' }"
    role="dialog"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">Parciais da Contagem</h5>
          <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <div v-if="loading" class="text-center text-muted">Carregando...</div>
          <div v-else-if="steps.length">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Início</th>
                  <th>Fim</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="step in steps" :key="step.id">
                  <td>{{ formatDateBrl(step.start_time).split(' ')[1] }}</td>
                  <td >{{ step.end_time ? formatDateBrl(step.end_time).split(' ')[1] : '' }}</td>
                  <td>{{ step.count }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="text-center text-muted">Nenhuma parcial registrada.</div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Fechar</button>
        </div>

      </div>
    </div>
  </div>
</template>
