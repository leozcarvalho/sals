<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { required } from "@vuelidate/validators";

const hardwareKindsApi = new ApiClient("/hardware-kinds");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Tipo", field: "kind", sort: "" },
]);

const filter = reactive({
  kind: null,
});

const hardwareKindSelected = ref(null);

const onHardwareKindSaved = () => {
  baseList.value.refresh();
  hardwareKindSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="hardwareKindSelected" 
    :fields="[
      { name: 'kind', label: 'Tipo', type: 'text', rules: 'required' }
    ]" 
    :api="hardwareKindsApi" 
    @saved="onHardwareKindSaved" 
    @close="hardwareKindSelected = null" 
  />

  <BaseList 
    ref="baseList" 
    :title="'Tipos de Hardware'" 
    :api="hardwareKindsApi" 
    :cols="cols" 
    :exportable="false" 
    :can-create="false"
    :can-edit="false" 
    :filter="filter" 
    v-model:filter="filter"
  >
    <!-- Botão Criar -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="modalForm.openModal(true)">
        <mdicon name="plus" />
      </button>
    </template>

    <!-- Filtros -->
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

    <!-- Ações de linha -->
    <template #row-actions="{ row }">
      <button 
        class="btn btn-sm btn-warning text-white" 
        @click="hardwareKindSelected = row; modalForm.openModal()"
      >
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>
