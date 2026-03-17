<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { FeedingCurveClient } from "../../services/feedingCurve";
import { handleApiToast } from "../../components/toast";

const feedingCurvesApi = new FeedingCurveClient();
const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
]);

const feedingCurveToClone = ref(null);
const openCloneModal = (feedingCurve) => {
  feedingCurveToClone.value = feedingCurve;
  const modal = new bootstrap.Modal(document.getElementById("modal-clone"));
  modal.show();
};

const cloneFeedingCurve = async () => {
  if (!feedingCurveToClone.value) return;
  const res = await feedingCurvesApi.clone(feedingCurveToClone.value.id);
  handleApiToast(res, "Curva de Alimentação clonada com sucesso!");
  baseList.value.refresh();
  feedingCurveToClone.value = null;
};
</script>

<template>
  <BaseList ref="baseList" :title="'Curvas de Alimentação'" :api="feedingCurvesApi" :cols="cols" :can-create="false"
    :can-edit="false">
    <template #extra-actions>
      <button class="btn btn-lg btn-success" @click="$router.push({ name: 'feeding-curve-form' })" title="Adicionar fórmula">
        <i class="fa fa-plus"></i>
      </button>
    </template>
    <template #row-actions="{ row }">
      <button class="btn btn-lg btn-primary text-white" @click="openCloneModal(row)">
        <i class="fa fa-copy"></i>
      </button>
      <button class="btn btn-lg btn-warning" @click="$router.push({ name: 'feeding-curve-form', params: { id: row.id } })">
        <i class="fa fa-pencil"></i>
      </button>
    </template>
  </BaseList>
  <div class="modal fade" id="modal-clone" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">Clonar Curva de Alimentação</div>
        <div class="modal-body" v-if="feedingCurveToClone">
          <p>Confirmar clonagem da curva de alimentação com {{ feedingCurveToClone.name }}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">CANCELAR</button>
          <button class="btn btn-danger" data-bs-dismiss="modal" @click="cloneFeedingCurve">CONFIRMAR</button>
        </div>
      </div>
    </div>
  </div>
</template>