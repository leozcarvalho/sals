<script setup>
import { reactive, ref, computed, onMounted } from "vue";
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
  tratos.value = (res.data.items || []).map(t => ({
    ...t,
    active: Number(t.percent) > 0
  }));

  loader.value.loaderOff();
};

onMounted(() => {
  refresh();
});

const totalPercent = computed(() =>
  tratos.value.reduce((acc, t) => acc + Number(t.percent || 0), 0)
);

const toggleActive = (trato) => {
  trato.active = !trato.active;

  if (!trato.active) {
    trato.percent = 0;
  }
};

const saveTratos = async () => {
  loader.value.loaderOn();
  // 🔥 força 0 se inativo
  const payload = tratos.value.map(t => ({
    ...t,
    percent: t.active ? t.percent : 0
  }));

  const res = await tratosApi.bulkUpdate(payload);
  handleApiToast(res, "Tratos atualizados com sucesso!");

  loader.value.loaderOff();
};
</script>

<template>
  <Loader ref="loader" />

  <div class="content">
    <BaseBlock title="Configurador de Tratos" content-full>

      <!-- HEADER -->
      <div class="row fw-bold mb-2 border-bottom pb-2">
        <div class="col-1">TRATO</div>
        <div class="col-1">HORA</div>
        <div class="col-1">MIN</div>
        <div class="col-2">PCT</div>
        <div class="col-2">STATUS</div>
      </div>

      <!-- LINHAS -->
      <div
        v-for="trato in tratos"
        :key="trato.id"
        class="row align-items-center mb-2"
      >
        <!-- NOME -->
        <div class="col-1">
          <input v-model="trato.name" class="form-control" disabled />
        </div>

        <!-- HORA -->
        <div class="col-1">
          <input v-model="trato.hour" type="number" class="form-control" />
        </div>
        :
        <!-- MIN -->
        <div class="col-1">
          <input v-model="trato.minute" type="number" class="form-control" />
        </div>

        <!-- PERCENT -->
        <div class="col-2">
          <NumericInput
            v-model="trato.percent"
            class="form-control"
            :min="0"
            :max="100"
            :disabled="!trato.active"
          />
        </div>

        <!-- ATIVO / INATIVO -->
        <div class="col-2">
          <button
            class="btn w-100"
            :class="trato.active ? 'btn-success' : 'btn-danger'"
            @click="toggleActive(trato)"
          >
            {{ trato.active ? "ATIVO" : "INATIVO" }}
          </button>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-3 fw-bold">
          TOTAL %
        </div>

        <div class="col-3">
          <div
            class="p-2 text-center fw-bold rounded"
            :class="totalPercent === 100 ? 'bg-success text-white' : 'bg-warning'"
          >
            {{ totalPercent }}
          </div>
        </div>
      </div>
      <div class="mt-4">
        <button
          class="btn btn-primary"
          data-bs-toggle="modal"
          data-bs-target="#modal-confirm"
          :disabled="totalPercent !== 100"
        >
          Salvar
        </button>
      </div>
    </BaseBlock>
    <div class="modal fade" id="modal-confirm" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header fw-bold">
            Confirmar Ação
          </div>

          <div class="modal-body">
            Ao salvar, TODAS as baias serão atualizadas com esses valores.
          </div>

          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">
              CANCELAR
            </button>

            <button
              class="btn btn-danger"
              data-bs-dismiss="modal"
              @click="saveTratos"
            >
              CONFIRMAR
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>