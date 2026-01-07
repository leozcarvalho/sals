<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute } from "vue-router";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import PinSelect from "../../components/PinSelect.vue";
import NumericInput from "../../components/NumericInput.vue";

const route = useRoute();

const shedsApi = new ApiClient("/sheds");
const salasApi = new ApiClient("/salas");
const baiasApi = new ApiClient("/baias");
const comedourosApi = new ApiClient("/comedouros");
const valvesApi = new ApiClient("/feeder-valves");

const shedId = route.query.id;
const shed = ref({});

const modalForm = ref(null);
const modalData = reactive({
  type: null,
  entity: null,
  parentId: null,
});

const deleteData = reactive({
  type: null,
  entity: null,
});


const fetchValvulas = async (comedouroId) => {
  const res = await valvesApi.getList({ comedouro_id: comedouroId });
  return res.data.items || [];
};

const refresh = async () => {
  const res = await shedsApi.get(shedId);
  shed.value = res.data || {};
  shed.value.salas?.forEach((sala) => {
    sala.baias?.forEach((baia) => {
      baia.comedouros?.forEach(async (comedouro) => {
        comedouro.device_pins = await fetchValvulas(comedouro.id);
      });
    });
  });
};

onMounted(async () => {
  await refresh();
});

const openModal = (type, entity = null, parentId = null) => {
  Object.assign(modalData, {
    type,
    entity: entity ?? {},
    parentId,
  });
  modalForm.value.openModal();
};

const onSaved = async () => {
  await refresh();
};

const openConfirm = (type, entity) => {
  deleteData.type = type;
  deleteData.entity = entity;
  const modal = new bootstrap.Modal(document.getElementById("modal-delete"));
  modal.show();
};

const deleteItem = async () => {
  let api;
  if (deleteData.type === "sala") api = salasApi;
  else if (deleteData.type === "baia") api = baiasApi;
  else if (deleteData.type === "comedouro") api = comedourosApi;
  else api = valvesApi;

  const res = await api.delete(deleteData.entity.id);
  handleApiToast(res, "Item excluído com sucesso");
  if (res.success) {
    await refresh();
    deleteData.type = null;
    deleteData.entity = null;
  }
};

const numericProps = {
  type: 'decimal',
  step: '0.01',
  max: '100'
}

const formConfig = ref({
  sala: {
    api: salasApi,
    fields: [
      { name: "name", label: "Nome", type: "text", rules: "required" },
      { name: "entrance_pin_id", label: "Pino de Entrada", component: PinSelect },
    ],
    extraPayload: () => ({ shed_id: modalData.parentId }),
  },
  baia: {
    api: baiasApi,
    fields: [
      { name: "name", label: "Nome", type: "text", rules: "required" },
      { name: "t1", label: "T1", component: NumericInput, props: numericProps, rules: "required" },
      { name: "t2", label: "T2", component: NumericInput, props: numericProps, rules: "required" },
      { name: "t3", label: "T3", component: NumericInput, props: numericProps, rules: "required" },
      { name: "t4", label: "T4", component: NumericInput, props: numericProps, rules: "required" },
      { name: "t5", label: "T5", component: NumericInput, props: numericProps, rules: "required" },
      { name: "t6", label: "T6", component: NumericInput, props: numericProps, rules: "required" },
    ],
    extraPayload: () => ({ sala_id: modalData.parentId }),
  },
  comedouro: {
    api: comedourosApi,
    fields: [
      { name: "name", label: "Nome", type: "text", rules: "required" },
      {
        name: "max_weight",
        label: "Peso máximo (kg)",
        type: "number",
        rules: "required|numeric|min:0",
      },
    ],
    extraPayload: () => ({ baia_id: modalData.parentId }),
  },
  valve: {
    api: valvesApi,
    fields: [
      { name: "device_pin_id", label: "Pino do Dispositivo", component: PinSelect, rules: "required" },
    ],
    extraPayload: () => ({ comedouro_id: modalData.parentId }),
  },
});
</script>

<template>
  <div class="container py-4">
    <h3 class="mb-4">{{ shed.name }}</h3>
    <button class="btn btn-success mb-3" @click="openModal('sala', null, shedId)">
      + Sala
    </button>

    <div v-for="sala in shed.salas" :key="sala.id" class="card mb-3 p-3 shadow-sm sala-card">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0">{{ sala.name }}</h5>
        <div>
          <button class="btn btn-lg btn-info me-1" type="button" data-bs-toggle="collapse"
            :data-bs-target="'#sala-' + sala.id" aria-expanded="true" :aria-controls="'sala-' + sala.id">
            <i class="fa fa-chevron-down"></i>
          </button>
          <button class="btn btn-lg btn-warning" @click="openModal('sala', sala, shedId)">
            <i class="fa fa-pencil"></i>
          </button>
          <button class="btn btn-lg btn-danger ms-1" @click="openConfirm('sala', sala)">
            <i class="fa fa-trash"></i>
          </button>
          <button class="btn btn-lg btn-success ms-1" @click="openModal('baia', null, sala.id)">
            + Baia
          </button>
        </div>
      </div>
      <!-- Conteúdo colapsável -->
      <div class="collapse" :id="'sala-' + sala.id">
        <div v-for="baia in sala.baias" :key="baia.id" class="card mb-2 ms-3 p-2 shadow-sm baia-card">
          <div class="d-flex justify-content-between align-items-center">
            <strong>{{ baia.name }}</strong>
            <div>
              <button class="btn btn-lg btn-warning" @click="openModal('baia', baia, sala.id)">
                <i class="fa fa-pencil"></i>
              </button>
              <button class="btn btn-lg btn-danger ms-1" @click="openConfirm('baia', baia)">
                <i class="fa fa-trash"></i>
              </button>
              <button class="btn btn-lg btn-success ms-1" @click="openModal('comedouro', null, baia.id)">
                + Comedouro
              </button>
            </div>
          </div>

          <div v-for="comedouro in baia.comedouros" :key="comedouro.id" class="card mt-2 ms-3 p-2 comedouro-card">
            <div class="d-flex justify-content-between align-items-center">
              <span>{{ comedouro.name }}</span>
              <div>
                <button class="btn btn-lg btn-warning" @click="openModal('comedouro', comedouro, baia.id)">
                  <i class="fa fa-pencil"></i>
                </button>
                <button class="btn btn-lg btn-danger ms-1" @click="openConfirm('comedouro', comedouro)">
                  <i class="fa fa-trash"></i>
                </button>
                <button class="btn btn-lg btn-success ms-1" @click="openModal('valve', null, comedouro.id)">
                  + Válvula
                </button>
              </div>
            </div>

            <!-- Lista de válvulas -->
            <div class="mt-2 ms-3 row">
              <div v-for="valve in comedouro.device_pins" :key="valve.id" class="d-flex align-items-center mb-1 col-auto">
                <button class="btn btn-lg btn-primary disabled me-2">{{ valve.device_pin.name }}</button>
                <button class="btn btn-lg btn-danger" @click="openConfirm('feeder-valves', valve)">
                  <i class="fa fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal de exclusão -->
    <div class="modal fade" id="modal-delete" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmar Ação</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            Deseja realmente excluir <strong>{{ deleteData.entity?.name || 'este item' }}</strong>?
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-danger" data-bs-dismiss="modal" @click="deleteItem">Confirmar</button>
          </div>
        </div>
      </div>
    </div>
    <BaseModalForm ref="modalForm" v-model="modalData.entity" :fields="formConfig[modalData.type]?.fields || []"
      :api="formConfig[modalData.type]?.api || {}" :extra-payload="formConfig[modalData.type]?.extraPayload()"
      @saved="onSaved" />
  </div>
</template>

<style scoped>
.sala-card {
  color: #fff;
  border-radius: 10px;
}

.baia-card {
  border-radius: 8px;
}

.feeder-card {
  border-radius: 6px;
}

.badge {
  font-size: 0.85rem;
}
</style>
