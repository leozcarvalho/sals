<script setup>
import { ref, reactive, watch } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import PinSelect from "../../components/PinSelect.vue";
import NumericInput from "../../components/NumericInput.vue";

const productTanksApi = new ApiClient("/product-tanks");
const baseList = ref(null);
const tankSelected = ref(null);
const modalForm = ref(null);

// ================== LISTAGEM ==================
const cols = reactive([
  { name: "#", field: "id" },
  {
    name: "Produto",
    field: "product_id",
    formatter: (value, row) => row.product ? row.product.name : 'N/A'
  },
  { name: "Nome", field: "name" },
  { name: "Volume (L)", field: "volume" },
  { name: "Descrição", field: "description" },
  {
    name: "Pino Rosca",
    field: "screw_pin_id",
    formatter: (value, row) => row.screw_pin ? row.screw_pin.name : 'N/A'
  },
  {
    name: "Pino Balança",
    field: "scale_pin_id",
    formatter: (value, row) => row.scale_pin ? row.scale_pin.name : 'N/A'
  }
]);

// ================== EVENTOS ==================
const onTankSaved = () => {
  baseList.value.refresh();
  tankSelected.value = null;
};

// ================== LIMPEZA AUTOMÁTICA ==================
watch(
  () => tankSelected.value?.is_dosador_seco,
  (val) => {
    if (!val && tankSelected.value) {
      tankSelected.value.scale_pin_id = null;
    }
  }
);
</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="tankSelected"
    :fields="[
      { name: 'product_id', label: 'Produto', type: 'async-select', entity: 'products' },
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'description', label: 'Descrição', type: 'text' },
      { name: 'screw_pin_id', label: 'Pino Rosca', component: PinSelect },
      { name: 'volume', label: 'Volume (L)', component: NumericInput, props: { min: 0, step: 0.01 } },
      { name: 'is_dosador_seco', label: 'É Dosador Seco?', type: 'checkbox' },
      { name: 'scale_pin_id', label: 'Pino Balança', slot: 'scalePin' }
    ]"
    :api="productTanksApi"
    @saved="onTankSaved"
    @close="tankSelected = null"
  >

    <!-- ================== SLOT CONDICIONAL ================== -->
    <template #scalePin="{ field, model, v }">
      <div v-if="model.is_dosador_seco" class="mb-3">
        <!-- 👇 label agora vem daqui -->
        <label class="form-label">{{ field.label }}</label>

        <PinSelect
          v-model="model[field.name]"
          :class="{ 'is-invalid': v?.[field.name]?.$error }"
          @blur="v?.[field.name]?.$touch()"
        />

        <div v-if="v?.[field.name]?.$errors.length" class="invalid-feedback d-block">
          {{ v[field.name].$errors?.[0]?.$message || "Campo inválido" }}
        </div>
      </div>
    </template>

  </BaseModalForm>

  <BaseList
    ref="baseList"
    :title="'Tanques de Produto'"
    :api="productTanksApi"
    :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="tankSelected = $event; modalForm.openModal()"
  />
</template>