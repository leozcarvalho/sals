<script setup>
import { reactive, ref, onMounted } from "vue";
import { TratosClient } from "../../services/tratosApi";
import Loader from "../../components/Loader.vue";
import NumericInput from "../../components/NumericInput.vue";
import { handleApiToast } from "../../components/toast";

const tratosApi = new TratosClient();
const loader = ref(null);

const tratos = ref([]);
const refresh = async () => {
  loader.value.loaderOn();
  const res = await tratosApi.getList();
  tratos.value = res.data.items || [];
  loader.value.loaderOff();
};

onMounted(() => {
  refresh();
});

const saveTratos = async () => {
  loader.value.loaderOn();
  const res = await tratosApi.bulkUpdate(tratos.value);
  handleApiToast(res, "Tratos atualizados com sucesso!");
  loader.value.loaderOff();
};

</script>

<template>
  <Loader ref="loader" />
  <div class="content">
    <BaseBlock title="Tratos" content-full>
      <div v-for="trato in tratos" :key="trato.id" class="row mb-3">
        <div class="col-1">
          <input v-model="trato.name" class="form-control" disabled />
        </div>
        <div class="col-2">
          <input v-model="trato.hour" class="form-control" />
        </div>
        <div class="col-2">
          <NumericInput v-model="trato.percent" class="form-control" :min="0" :max="100" />
        </div>
      </div>
      <div>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modal-confirm">Salvar</button>
      </div>
    </BaseBlock>
    <div class="modal fade" id="modal-confirm" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">Confirmar Ação</div>
          <div class="modal-body">Ao salvas os tratos TODAS as baias serão atualizadas pra esses valores</div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">CANCELAR</button>
            <button class="btn btn-danger" data-bs-dismiss="modal" @click="saveTratos">CONFIRMAR</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>