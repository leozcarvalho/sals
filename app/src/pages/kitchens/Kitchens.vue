<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";

const kitchensApi = new ApiClient("/kitchens");
const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Agitador", field: "shaker_pin_id", formatter: (value, row) => row.shaker_pin ? row.shaker_pin.name : 'N/A' },
  { name: "Bomba", field: "pump_pin_id", formatter: (value, row) => row.pump_pin ? row.pump_pin.name : 'N/A' },
  { name: "Balança", field: "scale_pin_id", formatter: (value, row) => row.scale_pin ? row.scale_pin.name : 'N/A' },
]);
</script>

<template>
  <BaseList ref="baseList" :title="'Cozinhas'" :api="kitchensApi" :cols="cols" :can-edit="false" :can-create="false">
  <template #extra-actions>
    <button class="btn btn-lg btn-success" @click="$router.push({ name: 'kitchen-form'})" title="Adicionar cozinha">
      <i class="fa fa-plus"></i>
    </button>
  </template>
  <template #row-actions="{ row }">
    <button  class="btn btn-lg btn-warning" @click="$router.push({ name: 'kitchen-form', params: { id: row.id } })">
      <i class="fa fa-pencil"></i>
    </button>
  </template>
</BaseList>
</template>
