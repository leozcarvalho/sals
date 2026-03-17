<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import { ShedClient } from "../../services/shedApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { handleApiToast } from "../../components/toast";

// API Sheds
const shedsApi = new ShedClient();
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
  { name: "Cozinha", field: "kitchen", formatter: (value, row) => row.kitchen.name }
]);

const shedSelected = ref(null);

const onshedSaved = () => {
  baseList.value.refresh();
  shedSelected.value = null;
};

const modalForm = ref(null);

const shedToClone = ref(null);
const openCloneModal = (shed) => {
  shedToClone.value = shed;
  const modal = new bootstrap.Modal(document.getElementById("modal-clone"));
  modal.show();
};

const cloneShed = async () => {
  if (!shedToClone.value) return;
  const res = await shedsApi.clone(shedToClone.value.id);
  handleApiToast(res, "Galpão clonado com sucesso!");
  baseList.value.refresh();
  shedToClone.value = null;
};
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="shedSelected" :fields="[
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'kitchen_id', label: 'Cozinha', type: 'select', options: kitchenOptions, rules: 'required' },
  ]" :api="shedsApi" @saved="onshedSaved" @close="shedSelected = null" />
  <BaseList ref="baseList" :title="'Galpões'" :api="shedsApi" :cols="cols" @create="modalForm.openModal(true)"
    @edit="shedSelected = $event; modalForm.openModal()"
    delete-confirm-message="Tem certeza que deseja excluir este galpão (Também serão excluídos salas, baias, comedouros e lotes)?">
    <template #row-actions="{ row }">
      <button class="btn btn-lg btn-warning text-white" @click="openCloneModal(row)">
        <i class="fa fa-copy"></i>
      </button>
      <button class="btn btn-lg btn-primary text-white" @click="$router.push({ name: 'shed', query: { id: row.id } })">
        <i class="fa fa-eye"></i>
      </button>
    </template>
  </BaseList>
  <div class="modal fade" id="modal-clone" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">Clonar Galpão</div>
        <div class="modal-body" v-if="shedToClone">
          <p>Confirmar clonagem do galpão com {{ shedToClone.name }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">CANCELAR</button>
          <button class="btn btn-danger" data-bs-dismiss="modal" @click="cloneShed">CONFIRMAR</button>
        </div>
      </div>
    </div>
  </div>
</template>
