<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";

const feedingCurvesApi = new ApiClient("/feeding-curves");
const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
]);
</script>

<template>
  <BaseList ref="baseList" :title="'Curvas de Alimentação'" :api="feedingCurvesApi" :cols="cols" :can-create="false"
    :can-edit="false">
    <template #extra-actions>
      <button class="btn btn-lg btn-success" @click="$router.push({ name: 'feeding-curve-form' })" title="Adicionar fórmula">
        <i class="fa fa-plus"></i>
      </button>
    </template>
    <template #row-actions="{ row }">
      <button class="btn btn-lg btn-warning" @click="$router.push({ name: 'feeding-curve-form', params: { id: row.id } })">
        <i class="fa fa-pencil"></i>
      </button>
    </template>
  </BaseList>
</template>