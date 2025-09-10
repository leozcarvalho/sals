<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import PinSelect from "../../components/PinSelect.vue";

// API Kitchens
const kitchensApi = new ApiClient("/kitchens");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Agitador", field: "shaker_pin_id", sort: "" },
  { name: "Bomba", field: "pump_pin_id", sort: "" },
  { name: "Balança", field: "scale_pin_id", sort: "" },
]);

const filter = reactive({
  name: null,
});

const kitchenSelected = ref(null);

const onKitchenSaved = () => {
  baseList.value.refresh();
  kitchenSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="kitchenSelected"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'shaker_pin_id', label: 'Agitador', component: PinSelect, rules: 'required' },
      { name: 'pump_pin_id', label: 'Bomba', component: PinSelect, rules: 'required' },
      { name: 'scale_pin_id', label: 'Balança', component: PinSelect, rules: 'required' },
    ]"
    :api="kitchensApi"
    @saved="onKitchenSaved"
    @close="kitchenSelected = null"
  />

  <BaseList
    ref="baseList"
    :title="'Cozinhas'"
    :api="kitchensApi"
    :cols="cols"
    :can-create="false"
    :can-edit="false"
    :filter="filter"
    v-model:filter="filter"
  >
    <!-- Ações Extras -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="modalForm.openModal(true)">
        <mdicon name="plus" />
      </button>
    </template>
    <template #cell-shaker_pin_id="{ row, col }">
      <span>
        {{ row.shaker_pin ? row.shaker_pin.name : 'N/A' }}
      </span>
    </template>
    <template #cell-pump_pin_id="{ row, col }">
      <span>
        {{ row.pump_pin ? row.pump_pin.name : 'N/A' }}
      </span>
    </template>
    <template #cell-scale_pin_id="{ row, col }">
      <span>
        {{ row.scale_pin ? row.scale_pin.name : 'N/A' }}
      </span>
    </template>
    <template #row-actions="{ row }">
      <button class="btn btn-sm btn-warning text-white" @click="kitchenSelected = row; modalForm.openModal()">
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>
