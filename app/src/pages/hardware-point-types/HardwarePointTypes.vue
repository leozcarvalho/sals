<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const pinsApi = new ApiClient("/hardware-point-types");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Tipo", field: "kind" },
  { name: "Qnt", field: "points_quantity" },
]);

const pinSelected = ref(null);

const onPinSaved = (pin) => {
  baseList.value.refresh();
  pinSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="pinSelected" :fields="[
    { name: 'points_quantity', label: 'Pontos', type: 'number', rules: 'required' },
    { name: 'kind', label: 'Tipo', type: 'select', options: [{ label: 'Bit', value: 'bit' }, { label: 'Dword', value: 'dword' }], rules: 'required' },
  ]" :api="pinsApi" @saved="onPinSaved" @close="pinSelected = null" />
  <BaseList ref="baseList" :title="'Pontos'" :api="pinsApi" :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="pinSelected = $event; modalForm.openModal()">
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
  </BaseList>
</template>
