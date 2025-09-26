<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import PinSelect from "../../components/PinSelect.vue";

const productTanksApi = new ApiClient("/product-tanks");
const baseList = ref(null);
const tankSelected = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Produto", field: "product_id", formatter: (value, row) => row.product ? row.product.name : 'N/A' },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
  { name: "Pino", field: "pin_id", formatter: (value, row) => row.device_pin ? row.device_pin.name : 'N/A' },
]);

const onTankSaved = () => {
  baseList.value.refresh();
  tankSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="tankSelected" :fields="[
    { name: 'product_id', label: 'Produto', type: 'async-select', rules: 'required', entity: 'products' },
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'description', label: 'Descrição', type: 'text' },
    { name: 'pin_id', label: 'Pino', component: PinSelect, rules: 'required' }
  ]" :api="productTanksApi" @saved="onTankSaved" @close="tankSelected = null"/>
  <BaseList ref="baseList" :title="'Tanques de Produto'" :api="productTanksApi" :cols="cols"
    @create="modalForm.openModal(true)" @edit="tankSelected = $event; modalForm.openModal()" />
</template>