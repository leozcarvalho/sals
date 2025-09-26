<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const feedingCurvesApi = new ApiClient("/feeding-curves");
const baseList = ref(null);
const curveSelected = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
]);

const onCurveSaved = () => {
  baseList.value.refresh();
  curveSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="curveSelected" :fields="[
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'description', label: 'Descrição', type: 'text' }
  ]" :api="feedingCurvesApi" @saved="onCurveSaved" @close="curveSelected = null" />
  <BaseList ref="baseList" :title="'Curvas de Alimentação'" :api="feedingCurvesApi" :cols="cols"
    @create="modalForm.openModal(true)" @edit="curveSelected = $event; modalForm.openModal()" />
</template>