<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { required, minValue, maxValue } from "@vuelidate/validators";
import { helpers } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";

const router = useRouter();
const route = useRoute();

const curvesApi = new ApiClient("/feeding-curves");
const formulasApi = new ApiClient("/formulas");

const curveId = ref(null);
const formulasOptions = ref([]);

const startDay = ref(null);
const endDay = ref(null);

const form = reactive({
  name: "",
  description: "",
  is_active: true,
  details: []
});

const fetchCurve = async () => {
  const res = await curvesApi.get(curveId.value);
  Object.assign(form, res.data);
  if (form.details && form.details.length > 0) {
    startDay.value = form.details[0].age_day;
    endDay.value = form.details[form.details.length - 1].age_day;
  }
};

const fetchFormulas = async () => {
  const res = await formulasApi.getList();
  formulasOptions.value =
    res.data.items.map((f) => ({ label: f.name, value: f.id })) || [];
};

onMounted(async () => {
  curveId.value = route.params.id;
  if (curveId.value) await fetchCurve();
  await fetchFormulas();
});

const rules = reactive({
  name: { required },
  description: { required },
  is_active: { required },
  details: {
    $each: helpers.forEach({
      day: { required, minValue: minValue(1) },
      formula_id: { required },
      formula_mass: { required, minValue: minValue(0), maxValue: maxValue(100) }
    })
  }
});

const v$ = useVuelidate(rules, form);

const generateDetails = () => {
  if (!startDay.value || !endDay.value || endDay.value < startDay.value) return;
  form.details = [];
  for (let day = startDay.value; day <= endDay.value; day++) {
    form.details.push({
      age_day: day,
      formula_id: null,
      formula_mass: 0,
      is_active: true
    });
  }
};

const handleResponse = (res) => {
  handleApiToast(res, "Curva salva com sucesso");
  if (res.success) router.push({ name: "feeding-curves" });
};

const submitted = ref(false);
const loading = ref(false);

const submit = async () => {
  v$.value.$touch();
  submitted.value = true;
  if (v$.value.$invalid) return;

  loading.value = true;
  try {
    const res = curveId.value
      ? await curvesApi.update(curveId.value, form)
      : await curvesApi.save(form);
    handleResponse(res);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="content">
    <BaseBlock title="Curva de Alimentação">
      <!-- Nome -->
      <div class="mb-3">
        <label class="form-label">Nome</label>
        <input v-model="form.name" type="text" class="form-control"
          :class="{ 'is-invalid': v$.name.$error && submitted }" />
        <div v-if="v$.name.$error && submitted" class="invalid-feedback">Campo obrigatório</div>
      </div>

      <!-- Descrição -->
      <div class="mb-3">
        <label class="form-label">Descrição</label>
        <input v-model="form.description" type="text" class="form-control"
          :class="{ 'is-invalid': v$.description.$error && submitted }" />
        <div v-if="v$.description.$error && submitted" class="invalid-feedback">Campo obrigatório</div>
      </div>

      <!-- Status -->
      <div class="mb-3">
        <label class="form-label">Status</label>
        <select v-model="form.is_active" class="form-select"
          :class="{ 'is-invalid': v$.is_active.$error && submitted }">
          <option :value="true">Ativo</option>
          <option :value="false">Inativo</option>
        </select>
        <div v-if="v$.is_active.$error && submitted" class="invalid-feedback">
          Campo obrigatório
        </div>
      </div>

      <!-- Intervalo de dias -->
      <div class="row mb-3">
        <div class="col">
          <label class="form-label">Dia Inicial</label>
          <input v-model="startDay" type="number" min="1" class="form-control" />
        </div>
        <div class="col">
          <label class="form-label">Dia Final</label>
          <input v-model="endDay" type="number" min="1" class="form-control" />
        </div>
        <div class="col-auto d-flex align-items-end">
          <button type="button" class="btn btn-success" @click="generateDetails">
            Gerar Linhas
          </button>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col-2"><strong>Dia</strong></div>
        <div class="col-6"><strong>Fórmula</strong></div>
        <div class="col-4"><strong>% Fórmula</strong></div>
      </div>
      
      <div v-for="(detail, index) in form.details" :key="index" class="row g-2 align-items-start mb-2">
        <div class="col-2">
          <input v-model="detail.age_day" type="number" class="form-control" disabled />
        </div>
        <div class="col-6">
          <select v-model="detail.formula_id" class="form-select"
            :class="{ 'is-invalid': v$.details.$each.$response.$data[index].formula_id.$error && submitted }">
            <option value="">Selecione uma fórmula</option>
            <option v-for="option in formulasOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <div v-if="v$.details.$each.$response.$data[index].formula_id.$error && submitted" class="invalid-feedback">
            Campo obrigatório
          </div>
        </div>

        <!-- % Fórmula -->
        <div class="col-4">
          <input v-model="detail.formula_mass" type="number" step="0.01" class="form-control"
            placeholder="% Fórmula"
            :class="{ 'is-invalid': v$.details.$each.$response.$data[index].formula_mass.$error && submitted }" />
          <div v-if="v$.details.$each.$response.$data[index].formula_mass.$error && submitted" class="invalid-feedback">
            Campo obrigatório
          </div>
        </div>
      </div>

      <!-- Salvar -->
      <button @click="submit" class="btn btn-primary mb-4 btn-lg" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        Salvar
      </button>
    </BaseBlock>
  </div>
</template>
