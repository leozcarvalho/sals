<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

// API Kitchens
const kitchensApi = new ApiClient("/kitchens");
const pinsApi = new ApiClient("/device-pins");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Agitador", field: "shaker_pin_id", sort: "" },
  { name: "Bomba", field: "pump_pin_id", sort: "" },
  { name: "Balança", field: "scale_pin_id", sort: "" },
  { name: "Produto", field: "product_pin_id", sort: "" },
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
const openModal = () => {
  modalForm.value.openModal();
};

const pinsOptions = ref([]);
onMounted(async () => {
  const res = await pinsApi.getList({ limit: 1000, in_use: false });
  pinsOptions.value = res.data.items.map(p => ({
    label: `${p.name}`,
    value: p.id,
  }));
});
</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="kitchenSelected"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'account_id', label: 'Conta', type: 'async-select', entity: 'accounts' },
      { name: 'shaker_pin_id', label: 'Agitador', type: 'select', rules: 'required', options: pinsOptions },
      { name: 'pump_pin_id', label: 'Bomba', type: 'select', rules: 'required', options: pinsOptions },
      { name: 'scale_pin_id', label: 'Balança', type: 'select', rules: 'required', options: pinsOptions },
      { name: 'product_pin_id', label: 'Produto', type: 'select', rules: 'required', options: pinsOptions },
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
    :exportable="false"
    :can-create="false"
    :can-edit="false"
    :filter="filter"
    v-model:filter="filter"
  >
    <!-- Ações Extras -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="openModal">
        <mdicon name="plus" />
      </button>
    </template>

    <!-- Filtro -->
    <template #filter>
      <div class="row px-5 py-5">
        <div class="col-md-4">
          <label class="form-label">Nome</label>
          <input v-model="filter.name" class="form-control" />
        </div>
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success" @click="baseList.refresh()">FILTRAR</button>
        </div>
      </div>
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
    <template #cell-product_pin_id="{ row, col }">
      <span>
        {{ row.product_pin ? row.product_pin.name : 'N/A' }}
      </span>
    </template>

    <!-- Ações de Linha -->
    <template #row-actions="{ row }">
      <button class="btn btn-sm btn-warning text-white" @click="kitchenSelected = row; openModal()">
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>

<style lang="scss" scoped>
@import url('../../assets/scss/custom/_tablestyle.scss');

.last-read {
  cursor: pointer;
}
</style>
