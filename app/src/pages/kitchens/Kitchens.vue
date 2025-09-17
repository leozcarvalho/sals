<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import PinSelect from "../../components/PinSelect.vue";

const kitchensApi = new ApiClient("/kitchens");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Agitador", field: "shaker_pin_id", formatter: (value, row) => row.shaker_pin ? row.shaker_pin.name : 'N/A' },
  { name: "Bomba", field: "pump_pin_id", formatter: (value, row) => row.pump_pin ? row.pump_pin.name : 'N/A' },
  { name: "Balança", field: "scale_pin_id", formatter: (value, row) => row.scale_pin ? row.scale_pin.name : 'N/A' },
]);

const kitchenSelected = ref(null);

const onKitchenSaved = () => {
  baseList.value.refresh();
  kitchenSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="kitchenSelected" :fields="[
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'shaker_pin_id', label: 'Agitador', component: PinSelect, rules: 'required' },
    { name: 'pump_pin_id', label: 'Bomba', component: PinSelect, rules: 'required' },
    { name: 'scale_pin_id', label: 'Balança', component: PinSelect, rules: 'required' },
    { name: 'products', label: 'Produtos', slot: 'products' },
  ]" :api="kitchensApi" @saved="onKitchenSaved" @close="kitchenSelected = null">
    <template #products>
      <div>
        <button type="button" class="btn btn-sm btn-success mb-2"
          @click="kitchenSelected?.products.push({ device_pin_id: null })">
          <mdicon name="plus" />
        </button>
      </div>
      <div v-for="(product, index) in kitchenSelected?.products" :key="index" class="d-flex align-items-center mb-2">
        <PinSelect v-model="product.device_pin_id" class="me-2 w-100" />
        <button type="button" class="btn btn-sm btn-danger" @click="kitchenSelected?.products.splice(index, 1)">
          <mdicon name="close" />
        </button>
      </div>
    </template>
  </BaseModalForm>
  <BaseList ref="baseList" :title="'Cozinhas'" :api="kitchensApi" :cols="cols"
    @create="modalForm.openModal(true)" @edit="kitchenSelected = $event; modalForm.openModal()" />
</template>
