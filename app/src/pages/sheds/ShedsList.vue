<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

// API Sheds
const shedsApi = new ApiClient("/sheds");
const kitchensApi = new ApiClient("/kitchens");

const baseList = ref(null);

const kitchenOptions = ref([]);
const fetchKitchens = async () => {
  const res = await kitchensApi.getList();
  kitchenOptions.value = res.data.items.map(kitchen => ({ label: kitchen.name, value: kitchen.id })) || [];
};

onMounted(() => {
  fetchKitchens();
});

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Cozinha", field: "kitchen", formatter: (value, row) => row.kitchen.name  }
]);

const shedSelected = ref(null);

const onshedSaved = () => {
  baseList.value.refresh();
  shedSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="shedSelected"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'kitchen_id', label: 'Cozinha', type: 'select', options: kitchenOptions, rules: 'required' },
    ]"
    :api="shedsApi"
    @saved="onshedSaved"
    @close="shedSelected = null"
  />
  <BaseList
    ref="baseList"
    :title="'Galpões'"
    :api="shedsApi"
    :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="shedSelected = $event; modalForm.openModal()"
  >
    <template #row-actions="{ row }">
      <button class="btn btn-lg btn-primary text-white" @click="$router.push({ name: 'shed', query: { id: row.id } })">
        <i class="fa fa-eye"></i>
      </button>
    </template>
  </BaseList>
</template>
