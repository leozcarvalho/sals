<script setup>
import { reactive, ref } from "vue";
import { useRoute } from "vue-router";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

// API Sheds
const shedsApi = new ApiClient("/sheds");

const baseList = ref(null);
const route = useRoute();

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
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

</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="kitchenSelected"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'account_id', label: 'Conta', type: 'async-select', entity: 'accounts' },
    ]"
    :api="shedsApi"
    @saved="onKitchenSaved"
    @close="kitchenSelected = null"
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

    <!-- Ações de Linha -->
    <template #row-actions="{ row }">
      <button class="btn btn-sm btn-primary text-white" @click="$router.push({ name: 'shed', query: { id: row.id } })">
        <mdicon name="eye" />
      </button>
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
