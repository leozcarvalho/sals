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

const loadAll = async () => {
  const roomsResponse = await roomsApi.getList({ shed_id: shedId });
  const roomsData = roomsResponse.data.items || [];

  await Promise.all(
    roomsData.map(async (room) => {
      const stallsResponse = await stallsApi.getList({ shed_room_id: room.id });
      room.stalls = stallsResponse.data.items || [];

      await Promise.all(
        room.stalls.map(async (stall) => {
          const feedersResponse = await feedersApi.getList({ room_stall_id: stall.id });
          stall.feeders = feedersResponse.data.items || [];
        })
      );
    })
  );

  rooms.value = roomsData;
};

onMounted(async () => {
  await loadAll();
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

const formConfig = ref({
  room: {
    api: roomsApi,
    fields: [
      { name: "name", label: "Nome", type: "text", rules: "required" },
      { name: "entrance_pin_id", label: "Pino de Entrada", component: PinSelect },
    ],
    extraPayload: () => ({ shed_id: modalData.parentId }),
  },
  stall: {
    api: stallsApi,
    fields: [
      { name: "name", label: "Nome", type: "text", rules: "required" },
    ],
    extraPayload: () => ({ shed_room_id: modalData.parentId }),
  },
  feeder: {
    api: feedersApi,
    fields: [
      { name: "name", label: "Nome", type: "text", rules: "required" },
      {
        name: "max_weight",
        label: "Peso máximo (kg)",
        type: "number",
        rules: "required|numeric|min:0",
      },
    ],
    extraPayload: () => ({ room_stall_id: modalData.parentId }),
  },
  valve: {
    api: valvesApi,
    fields: [
      { name: "device_pin_id", label: "Pino do Dispositivo", component: PinSelect, rules: "required" },
    ],
    extraPayload: () => ({ stall_feeder_id: modalData.parentId }),
  },
});
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
          <button class="btn btn-lg btn-info me-1" type="button" data-bs-toggle="collapse"
            :data-bs-target="'#room-' + room.id" aria-expanded="false" :aria-controls="'room-' + room.id">
            <i class="fa fa-chevron-down"></i>
          </button>
          <button class="btn btn-lg btn-warning" @click="openModal('room', room, shedId)">
            <i class="fa fa-pencil"></i>
          </button>
          <button class="btn btn-lg btn-danger ms-1" @click="openConfirm('room', room)">
            <i class="fa fa-trash"></i>
          </button>
          <button class="btn btn-lg btn-success ms-1" @click="openModal('stall', null, room.id)">
            + Baia
          </button>
        </div>
      </div>

      <!-- Conteúdo colapsável -->
      <div class="collapse" :id="'room-' + room.id">
        <div v-for="stall in room.stalls" :key="stall.id" class="card mb-2 ms-3 p-2 shadow-sm stall-card">
          <div class="d-flex justify-content-between align-items-center">
            <strong>{{ stall.name }}</strong>
            <div>
              <button class="btn btn-lg btn-warning" @click="openModal('stall', stall, room.id)">
                <i class="fa fa-pencil"></i>
              </button>
              <button class="btn btn-lg btn-danger ms-1" @click="openConfirm('stall', stall)">
                <i class="fa fa-trash"></i>
              </button>
              <button class="btn btn-lg btn-success ms-1" @click="openModal('feeder', null, stall.id)">
                + Comedouro
              </button>
            </div>
          </div>

          <div v-for="feeder in stall.feeders" :key="feeder.id" class="card mt-2 ms-3 p-2 feeder-card">
            <div class="d-flex justify-content-between align-items-center">
              <span>{{ feeder.name }}</span>
              <div>
                <button class="btn btn-lg btn-warning" @click="openModal('feeder', feeder, stall.id)">
                  <i class="fa fa-pencil"></i>
                </button>
                <button class="btn btn-lg btn-danger ms-1" @click="openConfirm('feeder', feeder)">
                  <i class="fa fa-trash"></i>
                </button>
                <button class="btn btn-lg btn-success ms-1" @click="openModal('valve', null, feeder.id)">
                  + Válvula
                </button>
              </div>
            </div>

            <!-- Lista de válvulas -->
            <div class="mt-2 ms-3 row">
              <div v-for="valve in feeder.device_pins" :key="valve.id" class="d-flex align-items-center mb-1 col-auto">
                <button class="btn btn-lg btn-primary disabled me-2">{{ valve.pin.name }}</button>
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
