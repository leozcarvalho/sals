<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { required } from "@vuelidate/validators";

const pinsApi = new ApiClient("/hardware-point-types");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Tipo", field: "kind", sort: "" },
  { name: "Qnt", field: "points_quantity", sort: "" },
]);

const filter = reactive(
  {
    kind: null,
  }
);

const pinSelected = ref(null);

const onPinSaved = (pin) => {
  baseList.value.refresh();
  pinSelected.value = null;
};

const modalForm = ref(null);
const openModal = () => {
  modalForm.value.openModal();
};
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="pinSelected" :fields="[
    { name: 'points_quantity', label: 'Pontos', type: 'number', rules: 'required' },
    { name: 'kind', label: 'Tipo', type: 'select', options: [{ label: 'Bit', value: 'bit' }, { label: 'Dword', value: 'dword' }], rules: 'required' },
  ]" :api="pinsApi" @saved="onPinSaved" @close="pinSelected = null" />
  <BaseList ref="baseList" :title="'Pontos'" :api="pinsApi" :cols="cols" :exportable="false" :can-create="false"
    :can-edit="false" :filter="filter" v-model:filter="filter">
    <!-- Filtros -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="openModal">
        <mdicon name="plus" />
      </button>
    </template>
    <template #filter>
      <div class="row px-5 py-5">
        <div class="col-md-4">
          <label class="form-label">Código</label>
          <input v-model="filter.kind" class="form-control" />
        </div>
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success" @click="baseList.refresh()">FILTRAR</button>
        </div>
      </div>
    </template>
    <template #row-actions="{ row }">
      <button class="btn btn-sm btn-warning text-white" @click="pinSelected = row; openModal()">
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
