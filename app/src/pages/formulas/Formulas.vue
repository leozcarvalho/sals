<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const formulasApi = new ApiClient("/formulas");
const baseList = ref(null);
const formulaSelected = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
  { name: "% Água", field: "water_percentage" },
  { name: "Tempo de Agitação (s)", field: "stirring_time" },
]);

const onFormulaSaved = () => {
  baseList.value.refresh();
  formulaSelected.value = null;
};

const modalForm = ref(null);

const addDetail = () => {
  formulaDetails.value.push({
    product_id: null,
    product_percentage_without_moisture: null,
  });
};

const open = (isNew, form) => {
  if (isNew) {
    formulaDetails.value = [];
  } else {
    const parsed = JSON.parse(JSON.stringify(form));
    console.log(modalForm.value.form.details);
    formulaDetails.value = parsed.details || [];
  }
};

const formulaDetails = ref([])
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="formulaSelected" :fields="[
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'description', label: 'Descrição', type: 'text', rules: 'required' },
    { name: 'water_percentage', label: '% Água', type: 'number', rules: { required: true, maxValue: 100 } },
    { name: 'stirring_time', label: 'Tempo de Agitação (segundos)', type: 'number', rules: 'required' },
    {
      name: 'is_active', label: 'Status', type: 'select', rules: 'required', options: [
        { label: 'Ativo', value: true },
        { label: 'Inativo', value: false },
      ]
    },
    { name: 'details', label: 'Detalhes', slot: 'details' },
  ]" :api="formulasApi" @saved="onFormulaSaved" @close="formulaSelected = null" @open="open" :extra-payload="{ details: formulaDetails }">
    <template #details="{ name, field, model, v }">
      <div v-if="formulaDetails.length" class="my-2">
        <div class="row g-2 mb-1">
          <div class="col-7"><strong>Produto</strong></div>
          <div class="col-3"><strong>Partes % fora água</strong></div>
        </div>
      </div>
      <div v-for="(detail, index) in formulaDetails" :key="index" class="row g-2 align-items-center mb-2">
        <div class="col-7">
          <VAsyncSelect :preFilledValue="detail.product_id" v-model="detail.product_id" entity="products" />
        </div>
        <div class="col-3">
          <input type="number" v-model="detail.product_percentage_without_moisture" class="form-control"
            placeholder="%" />
        </div>
        <div class="col-2 d-flex justify-content-end">
          <button type="button" class="btn btn-lg btn-danger" @click="formulaSelected?.details.splice(index, 1)">
            <mdicon name="close" />
          </button>
        </div>
      </div>
      <div class="text-end">
        <button type="button" class="btn btn-lg btn-success mb-2" @click="addDetail()">
          <mdicon name="plus" />
        </button>
      </div>

    </template>
  </BaseModalForm>
  <BaseList ref="baseList" :title="'Fórmulas'" :api="formulasApi" :cols="cols" @create="modalForm.openModal(true)"
    @edit="formulaSelected = $event; modalForm.openModal()" />
</template>