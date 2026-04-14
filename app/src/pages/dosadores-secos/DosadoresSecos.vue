<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { ApiClient } from "../../services/genericApi";
import PinSelect from "../../components/PinSelect.vue";

const api = new ApiClient("/dosadores-secos");
const kitchensApi = new ApiClient("/kitchens");

const baseList = ref(null);
const modalForm = ref(null);

const dosadorSelecionado = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Pino Saída", field: "output_pin_id", sort: "", formatter: (value, row) => row.output_pin ? row.output_pin.name : 'N/A' },
  { name: "Pino Balança", field: "scale_pin_id", sort: "", formatter: (value, row) => row.scale_pin ? row.scale_pin.name : 'N/A' },
  { name: "Cozinha Destino", field: "destiny_kitchen_id", sort: "", formatter: (value, row) => row.destiny_kitchen ? row.destiny_kitchen.name : 'N/A' },
  { name: "Ignorar Peso", field: "ignore_kitchen_weight", sort: "", formatter: (value) => value ? 'Sim' : 'Não' },
]);

const onSaved = () => {
  baseList.value.refresh();
  dosadorSelecionado.value = null;
};

const kitchensOptions = ref([]);
const loadKitchenOptions = async () => {
  const res = await kitchensApi.getList();
  kitchensOptions.value = (res.data.items || []).map(k => ({ label: k.name, value: k.id }));
};

onMounted(loadKitchenOptions);
</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="dosadorSelecionado"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'output_pin_id', label: 'Pino de Saída', component: PinSelect },
      { name: 'scale_pin_id', label: 'Pino da Balança', component: PinSelect },
      { name: 'volume_misturador', label: 'Volume do Misturador (kg)', type: 'number', rules: 'required' },
      { name: 'fracao_volume_misturador', label: 'Fração do Volume', type: 'number', rules: 'required' },
      { name: 'destiny_kitchen_id', label: 'Cozinha Destino', type: 'select', options: kitchensOptions },
      { name: 'ignore_kitchen_weight', label: 'Ignorar Peso na Cozinha', type: 'checkbox' }
    ]"
    :api="api"
    @saved="onSaved"
    @close="dosadorSelecionado = null"
  />

  <BaseList
    ref="baseList"
    :title="'Dosadores Secos'"
    :api="api"
    :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="dosadorSelecionado = $event; modalForm.openModal()"
  />
</template>
