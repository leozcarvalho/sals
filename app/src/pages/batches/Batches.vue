<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";

// Endpoint /batches
const batchesApi = new ApiClient("/batches");
const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Dia Inicial", field: "initial_day" },
  { name: "Curva", field: "feeding_curve_id", formatter: (value, row) => row.feeding_curve.name  },
  { name: "Galpão", field: "shed_id", formatter: (value, row) => row.shed.name  },
  { name: "Sala", field: "shed_room_id", formatter: (value, row) => row.shed_room.name  },
  { name: "Ativo", field: "is_active", type: "boolean", formatter: (value) => (value ? "Sim" : "Não")  },
]);
</script>

<template>
  <BaseList
    ref="baseList"
    :title="'Lotes'"
    :api="batchesApi"
    :cols="cols"
    :can-create="false"
    :can-edit="false"
  >
    <template #extra-actions>
      <button
        class="btn btn-lg btn-success"
        @click="$router.push({ name: 'batch-form' })"
        title="Adicionar lote"
      >
        <i class="fa fa-plus"></i>
      </button>
    </template>

    <template #row-actions="{ row }">
      <button
        class="btn btn-lg btn-warning"
        @click="$router.push({ name: 'batch-form', params: { id: row.id } })"
        title="Editar lote"
      >
        <i class="fa fa-pencil"></i>
      </button>
    </template>
  </BaseList>
</template>
