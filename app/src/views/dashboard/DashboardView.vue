<script setup>
import { ref, onMounted, nextTick } from "vue";
import { ApiClient } from "../../services/genericApi";
import SVGPanel from "../../components/SVGPanel.vue";

const dashboardApi = new ApiClient("/dashboard/svg-data");

const data = ref([]);
const selectedData = ref({});
const refresh = async () => {
  try {
    const res = await dashboardApi.getList();
    data.value = res.data || [];
    if (data.value.length > 0) {
      changeData(data.value[0]);
    }
  } catch (err) {
    console.error("Erro ao carregar dados do dashboard:", err);
  }
}

const SVGPanelRef = ref(null);
const changeData = async (item) => {
  selectedData.value = item;
  await nextTick();
  if (SVGPanelRef.value) {
    await SVGPanelRef.value.refresh();
  }
};
onMounted(async () => {
  await refresh();
});
</script>

<template>
  <BaseBackground>
    <div class="content content-full">
      <div class="button-group mb-3">
        <button
          v-for="item in data"
          :key="item.id"
          class="btn btn-primary btn-lg me-2"
          :class="{ 'btn-success': selectedData === item }"
          @click="changeData(item)"
        >
          {{ item.name }}
        </button>
    </div>
    <div v-if="selectedData.svg_id">
        <SVGPanel
          ref="SVGPanelRef"
          :svgId="selectedData.svg_id"
        />
      </div>
  </div>

  </BaseBackground>
</template>
