<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { required, minValue, maxValue } from "@vuelidate/validators";
import { helpers } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";

const router = useRouter();
const route = useRoute();

const formulasApi = new ApiClient("/formulas");
const productsApi = new ApiClient("/products");

const formulaId = ref(null);
const productsOptions = ref([]);

const form = reactive({
  name: "",
  description: "",
  water_percentage: null,
  stirring_time: null,
  is_active: true,
  details: []
});

// ---------------- FETCH FORMULA ----------------
const fetchFormula = async () => {
  const res = await formulasApi.get(formulaId.value);
  Object.assign(form, res.data);
};

// ---------------- FETCH PRODUCTS ----------------
const fetchProducts = async () => {
  const res = await productsApi.getList();

  const products =
    res.data.items.filter((p) => p.name.toLowerCase() !== "água") || [];

  productsOptions.value = products.map((p) => ({
    label: p.name,
    value: p.id
  }));

  // monta details mantendo valores existentes (edição)
  form.details = products.map((p) => {
    const existing = form.details.find((d) => d.product_id === p.id);

    return {
      product_id: p.id,
      product_percentage_without_moisture: existing
        ? existing.product_percentage_without_moisture
        : 0
    };
  });
};

onMounted(async () => {
  formulaId.value = route.params.id;

  if (formulaId.value) {
    await fetchFormula();
  }

  await fetchProducts();
});

// ---------------- TOTALIZADOR ----------------
const totalPercentage = computed(() => {
  return form.details.reduce((acc, item) => {
    const val = Number(item.product_percentage_without_moisture);
    return acc + (isNaN(val) ? 0 : val);
  }, 0);
});

// ---------------- VALIDAÇÃO ----------------
const rules = reactive({
  name: { required },
  description: { required },
  water_percentage: {
    required,
    minValue: minValue(0),
    maxValue: maxValue(100)
  },
  stirring_time: { required, minValue: minValue(1) },
  is_active: { required },
  details: {
    $each: helpers.forEach({
      product_percentage_without_moisture: {
        required,
        minValue: minValue(0),
        maxValue: maxValue(100)
      }
    })
  }
});

const v$ = useVuelidate(rules, form);

// ---------------- SUBMIT ----------------
const handleResponse = (res) => {
  handleApiToast(res, "Fórmula salva com sucesso");
  if (res.success) router.push({ name: "formulas" });
};

const submitted = ref(false);

const submit = async () => {
  v$.value.$touch();
  submitted.value = true;

  if (v$.value.$invalid) return;
  if (formulaId.value) {
    handleResponse(await formulasApi.update(formulaId.value, form));
  } else {
    handleResponse(await formulasApi.save(form));
  }
};
</script>

<template>
  <div class="content">
    <BaseBlock title="Fórmula">

      <!-- Nome -->
      <div class="mb-3">
        <label class="form-label">Nome</label>
        <input v-model="form.name" type="text" class="form-control"
          :class="{ 'is-invalid': v$.name.$error && submitted }" />
        <div v-if="v$.name.$error && submitted" class="invalid-feedback">
          Campo obrigatório
        </div>
      </div>

      <!-- Descrição -->
      <div class="mb-3">
        <label class="form-label">Descrição</label>
        <input v-model="form.description" type="text" class="form-control"
          :class="{ 'is-invalid': v$.description.$error && submitted }" />
        <div v-if="v$.description.$error && submitted" class="invalid-feedback">
          Campo obrigatório
        </div>
      </div>

      <!-- % Água -->
      <div class="mb-3">
        <label class="form-label">% Água</label>
        <input v-model="form.water_percentage" type="number" class="form-control"
          :class="{ 'is-invalid': v$.water_percentage.$error && submitted }" />
      </div>

      <!-- Tempo -->
      <div class="mb-3">
        <label class="form-label">Tempo de Agitação</label>
        <input v-model="form.stirring_time" type="number" class="form-control"
          :class="{ 'is-invalid': v$.stirring_time.$error && submitted }" />
      </div>

      <!-- Status -->
      <div class="mb-3">
        <label class="form-label">Status</label>
        <select v-model="form.is_active" class="form-select">
          <option :value="true">Ativo</option>
          <option :value="false">Inativo</option>
        </select>
      </div>

      <!-- DETALHES -->
      <div class="mb-3">
        <label class="form-label">Detalhes</label>
      </div>

      <div class="row mb-2">
        <div class="col-6"><strong>Produto</strong></div>
        <div class="col-4"><strong>%</strong></div>
      </div>

      <div v-for="(detail, index) in form.details"
           :key="detail.product_id"
           class="row g-2 mb-2">

        <!-- Produto -->
        <div class="col-6">
          <input
            type="text"
            class="form-control"
            :value="productsOptions.find(p => p.value === detail.product_id)?.label"
            disabled
          />
        </div>

        <!-- % -->
        <div class="col-4">
          <input
            v-model="detail.product_percentage_without_moisture"
            type="number"
            step="0.01"
            class="form-control"
            :class="{
              'is-invalid':
                v$.details.$each.$response.$data[index]
                  .product_percentage_without_moisture.$error && submitted
            }"
          />
        </div>
      </div>

      <!-- TOTAL -->
      <div class="mt-3">
        <strong>Total: </strong>
        <span :class="{
          'text-success': totalPercentage === 100,
          'text-danger': totalPercentage !== 100
        }">
          {{ totalPercentage.toFixed(2) }}%
        </span>
      </div>

      <!-- BOTÃO -->
      <button @click="submit" class="btn btn-primary my-4 btn-lg">
        Salvar
      </button>

    </BaseBlock>
  </div>
</template>