<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute } from "vue-router";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import PinSelect from "../../components/PinSelect.vue";

const route = useRoute();

const roomsApi = new ApiClient("/shed-rooms");
const stallsApi = new ApiClient("/room-stalls");
const feedersApi = new ApiClient("/stall-feeders");
const valvesApi = new ApiClient("/feeder-valves");

const shedId = route.query.id;
const rooms = ref([]);

const modalForm = ref(null);
const modalData = reactive({
  type: null,
  entity: null,
  parentId: null,
});

// Modal de exclusão
const deleteData = reactive({
  type: null,
  entity: null,
});

// Carrega toda a árvore de dados
const loadAll = async () => {
  const roomsResponse = await roomsApi.getList({ shed_id: shedId });
  rooms.value = roomsResponse.data.items || [];

  for (const room of rooms.value) {
    const stallsResponse = await stallsApi.getList({ shed_room_id: room.id });
    room.stalls = stallsResponse.data.items || [];

    for (const stall of room.stalls) {
      const feedersResponse = await feedersApi.getList({ room_stall_id: stall.id });
      stall.feeders = feedersResponse.data.items || [];
    }
  }
};

onMounted(async () => {
  await loadAll();
});

// Abre modal para criação/edição
const openModal = (type, entity = null, parentId = null) => {
  modalData.type = type;
  modalData.entity = entity || { name: "" };
  modalData.parentId = parentId;
  modalForm.value.openModal();
};

const onSaved = async () => {
  await loadAll();
};

const openConfirm = (type, entity) => {
  deleteData.type = type;
  deleteData.entity = entity;
  const modal = new bootstrap.Modal(document.getElementById("modal-delete"));
  modal.show();
};

const deleteItem = async () => {
  let api;
  if (deleteData.type === "room") api = roomsApi;
  else if (deleteData.type === "stall") api = stallsApi;
  else if (deleteData.type === "feeder") api = feedersApi;
  else api = valvesApi;

  const res = await api.delete(deleteData.entity.id);
  handleApiToast(res, "Item excluído com sucesso");
  if (res.success) {
    await loadAll();
    deleteData.type = null;
    deleteData.entity = null;
  }
};

// Adiciona uma nova válvula
const addValve = async (feederId, pinId) => {
  const res = await valvesApi.save({ stall_feeder_id: feederId, device_pin_id: pinId });
  handleApiToast(res, "Válvula adicionada");
  if (res.success) await loadAll();
};
</script>

<template>
  <div class="container py-4">
    <h3 class="mb-4">Galpão #{{ shedId }}</h3>
    <button class="btn btn-success mb-3" @click="openModal('room', null, shedId)">
      + Sala
    </button>

    <div v-for="room in rooms" :key="room.id" class="card mb-3 p-3 shadow-sm room-card">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0">{{ room.name }}</h5>
        <div>
          <button class="btn btn-sm btn-warning" @click="openModal('room', room, shedId)">
            <i class="fa fa-pencil"></i>
          </button>
          <button class="btn btn-sm btn-danger ms-1" @click="openConfirm('room', room)">
            <i class="fa fa-trash"></i>
          </button>
          <button class="btn btn-sm btn-success ms-1" @click="openModal('stall', null, room.id)">
            + Baia
          </button>
        </div>
      </div>

      <div v-for="stall in room.stalls" :key="stall.id" class="card mb-2 ms-3 p-2 shadow-sm stall-card">
        <div class="d-flex justify-content-between align-items-center">
          <strong>{{ stall.name }}</strong>
          <div>
            <button class="btn btn-sm btn-warning" @click="openModal('stall', stall, room.id)">
              <i class="fa fa-pencil"></i>
            </button>
            <button class="btn btn-sm btn-danger ms-1" @click="openConfirm('stall', stall)">
              <i class="fa fa-trash"></i>
            </button>
            <button class="btn btn-sm btn-success ms-1" @click="openModal('feeder', null, stall.id)">
              + Comedouro
            </button>
          </div>
        </div>

        <div v-for="feeder in stall.feeders" :key="feeder.id" class="card mt-2 ms-3 p-2 feeder-card">
          <div class="d-flex justify-content-between align-items-center">
            <span>{{ feeder.name }}</span>
            <div>
              <button class="btn btn-sm btn-warning" @click="openModal('feeder', feeder, stall.id)">
                <i class="fa fa-pencil"></i>
              </button>
              <button class="btn btn-sm btn-danger ms-1" @click="openConfirm('feeder', feeder)">
                <i class="fa fa-trash"></i>
              </button>
            </div>
          </div>

          <!-- Lista de válvulas -->
          <div class="mt-2 ms-3 row">
            <div v-for="valve in feeder.device_pins" :key="valve.id" class="d-flex align-items-center mb-1 col-auto">
              <span class="badge bg-primary me-2">{{ valve.pin.name }}</span>
              <button class="btn btn-sm btn-danger" @click="openConfirm('feeder-valves', valve)">
                <i class="fa fa-trash"></i>
              </button>
            </div>

            <div class="input-group mt-2">
              <PinSelect v-model="feeder.newValvePin" class="flex-grow-1" />
              <button :disabled="!feeder.newValvePin" class="btn btn-outline-success"
                @click="addValve(feeder.id, feeder.newValvePin)">
                + Válvula
              </button>
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

    <!-- Modal único -->
    <BaseModalForm ref="modalForm" v-model="modalData.entity"
      :fields="
          modalData.type === 'room'
            ? [
                { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
                { name: 'entrance_pin_id', label: 'Pino de Entrada', component: PinSelect }
              ]
            : [
                { name: 'name', label: 'Nome', type: 'text', rules: 'required' }
              ]
        "
      :api="modalData.type === 'room' ? roomsApi : modalData.type === 'stall' ? stallsApi : feedersApi" :extra-payload="modalData.type === 'room'
          ? { shed_id: modalData.parentId }
          : modalData.type === 'stall'
            ? { shed_room_id: modalData.parentId }
            : { room_stall_id: modalData.parentId }
        " @saved="onSaved" />
  </div>
</template>

<style scoped>
.room-card {
  color: #fff;
  border-radius: 10px;
}

.stall-card {
  border-radius: 8px;
}

.feeder-card {
  border-radius: 6px;
}

.badge {
  font-size: 0.85rem;
}
</style>
