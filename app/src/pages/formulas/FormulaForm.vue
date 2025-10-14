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

const fetchFormula = async () => {
  const res = await formulasApi.get(formulaId.value);
  Object.assign(form, res.data);
};

const fetchProducts = async () => {
  const res = await productsApi.getList();
  productsOptions.value =
    res.data.items.map((p) => ({ label: p.name, value: p.id })) || [];
};

onMounted(async () => {
  formulaId.value = route.params.id;
  if (formulaId.value) await fetchFormula();
  await fetchProducts();
});

// ---- Vuelidate ----
const rules = reactive({
  name: { required },
  description: { required },
  water_percentage: { required, minValue: minValue(0), maxValue: maxValue(100) },
  stirring_time: { required, minValue: minValue(1) },
  is_active: { required },
  details: {
    $each: helpers.forEach({
      product_id: { required },
      product_percentage_without_moisture: {
        required,
        minValue: minValue(0),
        maxValue: maxValue(100)
      }
    })
  }
});

const v$ = useVuelidate(rules, form);

// ---- submit ----
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
        <div v-if="v$.name.$error && submitted" class="invalid-feedback">Campo obrigatório</div>
      </div>

      <!-- Descrição -->
      <div class="mb-3">
        <label class="form-label">Descrição</label>
        <input v-model="form.description" type="text" class="form-control"
          :class="{ 'is-invalid': v$.description.$error && submitted }" />
        <div v-if="v$.description.$error && submitted" class="invalid-feedback">Campo obrigatório</div>
      </div>

      <!-- % Água -->
      <div class="mb-3">
        <label class="form-label">% Água</label>
        <input v-model="form.water_percentage" type="number" class="form-control"
          :class="{ 'is-invalid': v$.water_percentage.$error && submitted }" />
        <div v-if="v$.water_percentage.$error && submitted" class="invalid-feedback">
          Campo obrigatório (0 ≤ valor ≤ 100)
        </div>
      </div>

      <!-- Tempo de Agitação -->
      <div class="mb-3">
        <label class="form-label">Tempo de Agitação (segundos)</label>
        <input v-model="form.stirring_time" type="number" class="form-control"
          :class="{ 'is-invalid': v$.stirring_time.$error && submitted }" />
        <div v-if="v$.stirring_time.$error && submitted" class="invalid-feedback">
          Campo obrigatório (≥ 1)
        </div>
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

      <!-- Detalhes -->
      <div class="flex">
        <label class="form-label me-3">Detalhes</label>
        <button type="button" class="btn btn-lg btn-success mb-2"
          @click="form.details.push({ product_id: null, product_percentage_without_moisture: null })">
          <mdicon name="plus" />
        </button>
      </div>
      <div class="row mb-3" v-if="form.details.length > 0">
        <div class="col-6"><strong>Produto</strong></div>
        <div class="col-4"><strong>% Produto (sem umidade)</strong></div>
        <div class="col-2"><strong></strong></div>
      </div>

      <div v-for="(detail, index) in form.details" :key="index" class="row g-2 align-items-start mb-2">
        <!-- Produto -->
        <div class="col-6">
          <select v-model="detail.product_id" class="form-select"
            :class="{ 'is-invalid': v$.details.$each.$response.$data[index].product_id.$error && submitted }">
            <option value="">Selecione um produto</option>
            <option v-for="option in productsOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <div v-if="v$.details.$each.$response.$data[index].product_id.$error && submitted" class="invalid-feedback">
            Campo obrigatório
          </div>
        </div>

        <!-- % Produto -->
        <div class="col-4">
          <input v-model="detail.product_percentage_without_moisture" type="number" step="0.01" class="form-control"
            placeholder="% Produto"
            :class="{ 'is-invalid': v$.details.$each.$response.$data[index].product_percentage_without_moisture.$error && submitted }" />
          <div v-if="v$.details.$each.$response.$data[index].product_percentage_without_moisture.$error && submitted"
            class="invalid-feedback">
            Campo obrigatório (0 ≤ valor ≤ 100)
          </div>
        </div>

        <!-- Botão remover -->
        <div class="col-auto d-flex align-items-start">
          <button type="button" class="btn btn-lg btn-danger" @click="form.details.splice(index, 1)">
            <mdicon name="close" />
          </button>
        </div>
      </div>

      <!-- Salvar -->
      <button @click="submit" class="btn btn-primary mb-4 btn-lg">Salvar</button>
    </BaseBlock>
  </div>
</template>
