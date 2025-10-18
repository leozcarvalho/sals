<script setup>
import { ref, onMounted } from "vue";
import { ApiClient } from "../../services/genericApi";
const dashboardApi = new ApiClient("/dashboard/svg-data");

const data = ref([]);
const selectedData = ref({});

onMounted(async () => {
  try {
    const res = await dashboardApi.getList();
    data.value = res.data || [];
    selectedData.value = data.value[0] || {};
  } catch (err) {
    console.error("Erro ao carregar dados do dashboard:", err);
  }
});
</script>

<template>
  <BaseBackground>
    <div class="content content-full">
      <div class="button-group mb-4">
        <button
          v-for="item in data"
          :key="item.id"
          class="btn btn-primary btn-lg me-2"
          :class="{ 'btn-success': selectedData === item }"
          @click="selectedData = item"
        >
          {{ item.name }}
        </button>
      <div>
        {{ selectedData }}
      </div>
    </div>
  </div>

  </BaseBackground>
</template>
