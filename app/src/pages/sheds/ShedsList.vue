<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import PinSelect from "../../components/PinSelect.vue";

// API Sheds
const shedsApi = new ApiClient("/sheds");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
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
