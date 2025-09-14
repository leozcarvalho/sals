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
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
]);

const filter = reactive({
  name: null,
});

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
    :exportable="false"
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
    <!-- Ações de Linha -->
    <template #row-actions="{ row }">
      <button class="btn btn-sm btn-primary text-white" @click="$router.push({ name: 'shed', query: { id: row.id } })">
        <mdicon name="eye" />
      </button>
      <button class="btn btn-sm btn-warning text-white" @click="shedSelected = row; modalForm.openModal()">
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>
