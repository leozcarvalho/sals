<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const productsApi = new ApiClient("/products");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
  { name: "Porcentagem de Umidade", field: "moisture_percentage" },
  { name: "Tipo", field: "kind", formatter: (value) => value === 'solid' ? 'Sólido' : 'Líquido' },
  { name: "Densidade", field: "density" },
]);

const productSelected = ref(null);

const onProductSaved = () => {
  baseList.value.refresh();
  productSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="productSelected" :fields="[
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'description', label: 'Descrição', type: 'text', rules: 'required' },
    { name: 'moisture_percentage', label: 'Porcentagem de Umidade', type: 'number', rules: { required: true, maxValue: 100 } },
    { name: 'kind', label: 'Tipo', type: 'select', rules: 'required', options: [
      { label: 'Sólido', value: 'solid' },
      { label: 'Líquido', value: 'liquid' },
    ] },
    { name: 'density', label: 'Densidade Kg/m³', type: 'number', rules: 'required' },
    { name: 'is_active', label: 'Status', type: 'select', rules: 'required', options: [
      { label: 'Ativo', value: true },
      { label: 'Inativo', value: false },
    ] },
  ]" :api="productsApi" @saved="onProductSaved" @close="productSelected = null">
  </BaseModalForm>
  <BaseList ref="baseList" :title="'Produtos'" :api="productsApi" :cols="cols"
    @create="modalForm.openModal(true)" @edit="productSelected = $event; modalForm.openModal()" />
</template>