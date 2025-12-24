<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { required, minValue, requiredIf } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import { ApiClient } from "../../services/genericApi";
import { BatchClient } from "../../services/batchesApi";
import { handleApiToast } from "../../components/toast";
import Loader from "@/components/Loader.vue";
import { helpers } from "@vuelidate/validators";
import { formatDateBrl } from "@/helpers/formatters";

const router = useRouter();
const route = useRoute();

const batchesApi = new BatchClient();
const shedsApi = new ApiClient("/sheds");
const feedingCurvesApi = new ApiClient("/feeding-curves");
const movimentKindsApi = new ApiClient("/moviment-kinds");
const baiasApi = new ApiClient("/baias");
const salaApi = new ApiClient("/salas");

const batchId = ref(null);

const shedsOptions = ref([]);
const SalasOptions = ref([]);
const feedingCurvesOptions = ref([]);
const feedingCurveDays = ref([]);
const movimentKindOptions = ref([]);

const form = reactive({
  name: "",
  description: "",
  initial_day: null,
  is_active: true,
  feeding_curve_id: null,
  shed_id: null,
  sala_id: null,
  moviments: [],
  sala: {},
});

const fetchBatch = async () => {
  const res = await batchesApi.get(batchId.value);
  Object.assign(form, res.data);
  if (form.shed_id) await fetchRooms(form.shed_id);
  if (form.feeding_curve_id) await setFeedingCurveDays(form.feeding_curve_id);
  if (form.sala_id) await fetchStallOptions(form.sala_id);
};

const fetchSheds = async () => {
  const res = await shedsApi.getList();
  shedsOptions.value =
    res.data.items.map((s) => ({ label: s.name, value: s.id, rooms: s.rooms })) || [];
};

const fetchRooms = async (shedId) => {
  const res = await salaApi.getList({ shed_id: shedId, is_in_batch: false });
  SalasOptions.value = res.data.items.map((r) => ({ label: r.name, value: r.id })) || [];
};

const fetchFeedingCurves = async () => {
  const res = await feedingCurvesApi.getList();
  feedingCurvesOptions.value =
    res.data.items.map((c) => ({ label: c.name, value: c.id, details: c.details })) || [];
};

const setFeedingCurveDays = async (curveId) => {
  const selectedCurve = feedingCurvesOptions.value.find((c) => c.value === curveId);
  if (selectedCurve) {
    feedingCurveDays.value = selectedCurve.details?.map((d) => d.age_day) || [];
  }
};

const fetchMovimentKinds = async () => {
  const res = await movimentKindsApi.getList();
  movimentKindOptions.value = res.data.items.map((mk) => ({ label: mk.code, value: mk.id, kind: mk.kind })) || [];
};

const onRoomChange = async () => {
  if (!form.sala_id) return;
  await fetchBaiasOptions(form.sala_id);
  if (!batchId.value) generateMoviments();
};

const baiasOptions = ref([]);

const fetchBaiasOptions = async (roomId) => {
  if (!roomId) return;
  const res = await baiasApi.getList({ sala_id: roomId });
  baiasOptions.value = res.data.items.map((s) => ({ label: s.name, value: s.id, qnt: s.animals_quantity })) || [];
};

const generateMoviments = () => {
  form.moviments = baiasOptions.value.map((baia) => ({
    moviment_kind_code: "ENTRADA_LOTE",
    moviment_kind_id:
      movimentKindOptions.value.find((x) => x.label === "ENTRADA_LOTE")?.value || null,
    stall_origin_id: baia.value,
    stall_destination_id: null,
    quantity: 0,
    description: "",
    isNew: true,
  }));
};


const newMoviment = reactive({
  moviment_kind_: {},
  stall_origin_id: null,
  stall_destination_id: null,
  quantity: null,
  description: "",
});

onMounted(async () => {
  batchId.value = route.params.id;
  await Promise.all([fetchSheds(), fetchFeedingCurves(), fetchMovimentKinds(), fetchStallOptions()]);
  if (batchId.value) {
    await fetchBatch();
  }
});

const rules = reactive({
  name: { required },
  description: {},
  is_active: { required },
  initial_day: { required, minValue: minValue(1) },
  feeding_curve_id: { required },
  shed_id: { required },
  sala_id: { required },
  moviments: {
    $each: helpers.forEach({
      quantity: { required, minValue: minValue(0) },
    }),
  },
});

const v$ = useVuelidate(rules, form);

const submitted = ref(false);
const loading = ref(false);

const handleResponse = async (res) => {
  handleApiToast(res, "Lote salvo com sucesso");
  if (res.success) {
    if (!batchId.value) {
      router.push({ name: "batch-form", params: { id: res.data.id } });
      batchId.value = res.data.id;
    }
    await fetchBatch();
  }
};

const submit = async () => {
  v$.value.$touch();
  submitted.value = true;
  if (v$.value.$invalid) return;
  loading.value = true;
  try {
    const res = batchId.value ? await batchesApi.update(batchId.value, form) : await batchesApi.save(form);
    await handleResponse(res);
  } finally {
    loading.value = false;
  }
};

// MOVIMENTOS
const movimentRules = computed(() => ({
  moviment_kind_id: { required },

  stall_origin_id: {
    required: requiredIf(() =>
      ["ENTRADA", "TRANSFERENCIA"].includes(movimentKindAction.value)
    ),
  },

  stall_destination_id: {
    required: requiredIf(() =>
      ["SAIDA", "TRANSFERENCIA"].includes(movimentKindAction.value)
    ),
  },

  quantity: { required, minValue: minValue(1) },
}));

const vMoviment$ = useVuelidate(movimentRules, newMoviment);

const showMovimentModal = ref(false);

const openModalMoviment = () => {
  Object.assign(newMoviment, {
    moviment_kind_id: null,
    stall_origin_id: null,
    stall_destination_id: null,
    quantity: null,
    description: "",
  });
  showMovimentModal.value = true;
};

const movimentKindAction = ref(null)
const onMovimentKindChange = () => {
  const selectedKind = movimentKindOptions.value.find(mk => mk.value === newMoviment.moviment_kind_id);
  movimentKindAction.value = selectedKind ? selectedKind.kind : null;
}

const execMoviment = async () => {
  vMoviment$.value.$touch();
  if (vMoviment$.value.$invalid) return;
  const res = await batchesApi.execMoviment(batchId.value, newMoviment);
  handleApiToast(res, "Movimento registrado com sucesso");
  if (res.success) {
    showMovimentModal.value = false;
    await fetchBatch();
  }
};
</script>

<template>
  <Loader ref="loader" />
  <div class="content">
    <BaseBlock title="Lote">
      <div class="row">
        <div class="mb-3 col-6">
          <label class="form-label">Nome</label>
          <input v-model="form.name" type="text" class="form-control"
            :class="{ 'is-invalid': v$.name.$error && submitted }" :disabled="batchId" />
          <div v-if="v$.name.$error && submitted" class="invalid-feedback"> Campo obrigatório </div>
        </div>

        <div class="mb-3 col-6">
          <label class="form-label">Status</label>
          <select v-model="form.is_active" class="form-select">
            <option :value="true">Ativo</option>
            <option :value="false">Inativo</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Descrição</label>
          <input v-model="form.description" type="text" class="form-control" :disabled="batchId" />
        </div>

        <div class="mb-3 col-6">
          <label class="form-label">Galpão</label>
          <select v-model="form.shed_id" class="form-select" :class="{ 'is-invalid': v$.shed_id.$error && submitted }"
            @change="fetchRooms(form.shed_id)" :disabled="batchId">
            <option value="">Selecione</option>
            <option v-for="opt in shedsOptions" :key="opt.value" :value="opt.value"> {{ opt.label }} </option>
          </select>
          <div v-if="v$.shed_id.$error && submitted" class="invalid-feedback"> Campo obrigatório </div>
        </div>

        <div class="mb-3 col-6">
          <label class="form-label">Sala</label>
          <div v-if="batchId">
            <input :value="form.sala.name" class="form-control" disabled />
          </div>
          <select v-model="form.sala_id" class="form-select" v-else
            :class="{ 'is-invalid': v$.sala_id.$error && submitted }" @change="onRoomChange" :disabled="batchId">
            <option value="">Selecione</option>
            <option v-for="opt in SalasOptions" :key="opt.value" :value="opt.value"> {{ opt.label }} </option>
          </select>
          <div v-if="v$.sala_id.$error && submitted" class="invalid-feedback"> Campo obrigatório </div>
        </div>

        <div class="mb-3 col-6">
          <label class="form-label">Curva de Alimentação</label>
          <select v-model="form.feeding_curve_id" class="form-select"
            :class="{ 'is-invalid': v$.feeding_curve_id.$error && submitted }"
            @change="setFeedingCurveDays(form.feeding_curve_id)">
            <option value="">Selecione</option>
            <option v-for="opt in feedingCurvesOptions" :key="opt.value" :value="opt.value"> {{ opt.label }} </option>
          </select>
          <div v-if="v$.feeding_curve_id.$error && submitted" class="invalid-feedback"> Campo obrigatório </div>
        </div>

        <div class="mb-3 col-6">
          <label class="form-label">Dia Inicial</label>
          <select v-model="form.initial_day" class="form-select"
            :class="{ 'is-invalid': v$.initial_day.$error && submitted }" :disabled="feedingCurveDays.length === 0">
            <option value="">Selecione</option>
            <option v-for="day in feedingCurveDays" :key="day" :value="day"> Dia {{ day }} </option>
          </select>
          <div v-if="v$.initial_day.$error && submitted" class="invalid-feedback"> Selecione o dia inicial do lote
          </div>
        </div>
      </div>

      <div>
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h5 class="m-0">Movimentos</h5>
          <div>
            <button type="button" class="btn btn-success btn-sm" v-if="batchId" @click="openModalMoviment">
              <mdicon name="plus" /> Novo Movimento
            </button>
          </div>
        </div>

        <div v-if="form.moviments.length > 0" class="mb-3">
          <div class="row mb-3">
            <div class="col-2"><strong>Tipo Movimento</strong></div>
            <div class="col-2"><strong>Baia Origem</strong></div>
            <div class="col-2"><strong>Baia Destino</strong></div>
            <div class="col-1"><strong>Qnt</strong></div>
            <div class="col-2"><strong>Descrição</strong></div>
            <div class="col-3"><strong>Data</strong></div>
          </div>

          <div v-for="(mov, index) in form.moviments" :key="index" class="row g-2 align-items-start mb-2">
            <div class="col-2">
              <select v-model="mov.moviment_kind_id" class="form-select" :disabled="!mov.isNew">
                <option value="">Selecione o tipo</option>
                <option v-for="option in movimentKindOptions" :key="option.value" :value="option.value"> {{ option.label
                }} </option>
              </select>
            </div>

            <div class="col-2">
              <select v-model="mov.baia_origin_id" class="form-select" :disabled="!mov.isNew">
                <option value="">Origem</option>
                <option v-for="baia in baiasOptions" :key="baia.value" :value="baia.value"> {{ baia.label }}
                </option>
              </select>
            </div>

            <div class="col-2">
              <select v-model="mov.baia_destination_id" class="form-select" :disabled="!mov.isNew">
                <option value="">Destino</option>
                <option v-for="baia in baiasOptions" :key="baia.value" :value="baia.value"> {{ baia.label }}
                </option>
              </select>
            </div>

            <div class="col-1">
              <input :class="{ 'is-invalid': v$.moviments.$each.$response.$data[index].quantity.$error && submitted }"
                v-model.number="mov.quantity" type="number" min="1" class="form-control" :disabled="!mov.isNew" />
            </div>

            <div class="col-2">
              <input v-model="mov.description" rows="2" class="form-control" placeholder="Descrição opcional"
                :disabled="!mov.isNew" />
            </div>

            <div class="col-2 col-md-3" v-if="mov.id">
              <input :value="formatDateBrl(mov.created_at)" class="form-control" disabled />
            </div>
          </div>
        </div>
      </div>
      <button @click="submit" class="btn btn-primary mb-4 btn-lg" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span> Salvar
      </button>
      <div v-if="showMovimentModal" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Novo Movimento</h5>
              <button type="button" class="btn-close" @click="showMovimentModal = false"></button>
            </div>

            <div class="modal-body">
              <div class="mb-3">
                <label>Tipo de Movimento</label>
                <select v-model="newMoviment.moviment_kind_id" class="form-select"
                  :class="{ 'is-invalid': vMoviment$.moviment_kind_id.$error }" @change="onMovimentKindChange">
                  <option value="">Selecione</option>
                  <option v-for="option in movimentKindOptions" :key="option.value" :value="option.value"> {{
                    option.label }} </option>
                </select>
                <div v-if="vMoviment$.moviment_kind_id.$error" class="invalid-feedback"> Campo obrigatório </div>
              </div>

              <!-- Origem -->
              <div class="mb-3" v-if="['ENTRADA', 'TRANSFERENCIA'].includes(movimentKindAction)">
                <label>Baia Origem</label>
                <select v-model="newMoviment.baia_origin_id" class="form-select"
                  :class="{ 'is-invalid': vMoviment$.baia_origin_id.$error }">
                  <option value="">Selecione</option>
                  <option v-for="baia in baiasOptions" :key="baia.value" :value="baia.value">
                    {{ baia.label }} ({{ baia.qnt }} animais)
                  </option>
                </select>
                <div v-if="vMoviment$.stall_origin_id.$error" class="invalid-feedback"> Campo obrigatório </div>
              </div>

              <!-- Destino -->
              <div class="mb-3" v-if="['SAIDA', 'TRANSFERENCIA'].includes(movimentKindAction)">
                <label>Baia Destino</label>
                <select v-model="newMoviment.baia_destination_id" class="form-select"
                  :class="{ 'is-invalid': vMoviment$.baia_destination_id.$error }">
                  <option value="">Selecione</option>
                  <option v-for="baia in baiasOptions" :key="baia.value" :value="baia.value">
                    {{ baia.label }} ({{ baia.qnt }} animais)
                  </option>
                </select>
                <div v-if="vMoviment$.baia_destination_id.$error" class="invalid-feedback"> Campo obrigatório </div>
              </div>

              <div class="mb-3">
                <label>Quantidade</label>
                <input v-model.number="newMoviment.quantity" type="number" min="1" class="form-control"
                  :class="{ 'is-invalid': vMoviment$.quantity.$error }" />
                <div v-if="vMoviment$.quantity.$error" class="invalid-feedback"> Campo obrigatório </div>
              </div>

              <div class="mb-3">
                <label>Descrição (opcional)</label>
                <textarea v-model="newMoviment.description" class="form-control"></textarea>
              </div>
            </div>

            <div class="modal-footer">
              <button class="btn btn-secondary" @click="showMovimentModal = false">Cancelar</button>
              <button class="btn btn-success" @click="execMoviment">Salvar Movimento</button>
            </div>

          </div>
        </div>
      </div>

      <!-- BACKDROP -->
      <div v-if="showMovimentModal" class="modal-backdrop fade show"></div>
    </BaseBlock>
  </div>
</template>
