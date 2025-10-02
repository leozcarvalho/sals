<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { required, minValue, maxValue } from "@vuelidate/validators";
import { helpers } from "@vuelidate/validators";
import useVuelidate from "@vuelidate/core";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import PinSelect from "../../components/PinSelect.vue";

const router = useRouter();
const route = useRoute();
const kitchensApi = new ApiClient("/kitchens");

const form = reactive({
  name: "",
  shaker_pin_id: null,
  pump_pin_id: null,
  scale_pin_id: null,
  max_bowl_weight: null,
  bowl_weight_fraction: null,
  tanks: []
});

const kitchenId = ref(null)
const fetchKitchen = async () => {
  const res = await kitchensApi.get(kitchenId.value);
  Object.assign(form, res.data);
};

const productTanksApi = new ApiClient("/product-tanks");
const tanksOptions = ref([]);

const fetchTanks = async () => {
  const res = await productTanksApi.getList();
  tanksOptions.value = res.data.items.map(tank => ({ label: tank.name, value: tank.id })) || [];
};

onMounted(async () => {
  kitchenId.value = route.params.id
  if (kitchenId.value) await fetchKitchen(kitchenId.value);
  await fetchTanks();
});

const rules = reactive({
  name: { required },
  shaker_pin_id: { required, minValue: minValue(1) },
  pump_pin_id: { required, minValue: minValue(1) },
  scale_pin_id: { required, minValue: minValue(1) },
  max_bowl_weight: { required, minValue: minValue(0) },
  bowl_weight_fraction: { required, minValue: minValue(0), maxValue: maxValue(1) },
  tanks: {
    $each: helpers.forEach({
      product_tank_id: {
        required
      }
    })
  }
});

const v$ = useVuelidate(rules, form);

const handleResponse = (res) => {
  handleApiToast(res, "Cozinha salva com sucesso");
  if (res.success) router.push({ name: "kitchens" });
};

const submitted = ref(false);
const submit = async () => {
  v$.value.$touch();
  submitted.value = true;
  if (v$.value.$invalid) return;
  if (kitchenId.value) {
    handleResponse(await kitchensApi.update(kitchenId.value, form));
  } else {
    handleResponse(await kitchensApi.save(form));
  }
}
</script>

<template>
  <div class="content">
    <BaseBlock title="Cozinha">
      <div class="mb-3">
        <label class="form-label">Nome</label>
        <input v-model="form.name" type="text" class="form-control" :class="{ 'is-invalid': v$.name.$error }" />
        <div v-if="v$.name.$error" class="invalid-feedback">Campo necessário</div>
      </div>

      <div class="mb-3">
        <label class="form-label">Agitador</label>
        <pin-select v-model="form.shaker_pin_id" :class="{ 'is-invalid': v$.shaker_pin_id.$error }" />
        <div v-if="v$.shaker_pin_id.$error" class="invalid-feedback">Campo necessário</div>
      </div>

      <div class="mb-3">
        <label class="form-label">Bomba</label>
        <pin-select v-model="form.pump_pin_id" :class="{ 'is-invalid': v$.pump_pin_id.$error }" />
        <div v-if="v$.pump_pin_id.$error" class="invalid-feedback">Campo necessário</div>
      </div>

      <div class="mb-3">
        <label class="form-label">Balança</label>
        <pin-select v-model="form.scale_pin_id" :class="{ 'is-invalid': v$.scale_pin_id.$error }" />
        <div v-if="v$.scale_pin_id.$error" class="invalid-feedback">Campo necessário</div>
      </div>

      <div class="mb-3">
        <label class="form-label">Peso máximo da cuba (kg)</label>
        <input v-model="form.max_bowl_weight" type="number" class="form-control"
          :class="{ 'is-invalid': v$.max_bowl_weight.$error }" />
        <div v-if="v$.max_bowl_weight.$error" class="invalid-feedback">
          Campo obrigatório e ≥ 0
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Fração de peso da cuba</label>
        <input v-model="form.bowl_weight_fraction" type="number" step="0.01" class="form-control"
          :class="{ 'is-invalid': v$.bowl_weight_fraction.$error }" />
        <div v-if="v$.bowl_weight_fraction.$error" class="invalid-feedback">
          Campo obrigatório (0 ≤ valor ≤ 1)
        </div>
      </div>
      <div class="flex">
        <label class="form-label me-3">Tanques</label>
        <button type="button" class="btn btn-lg btn-success mb-2" @click="form.tanks.push({ product_tank_id: null })">
          <mdicon name="plus" />
        </button>
      </div>
      <div v-for="(tank, index) in form.tanks" :key="index" class="row g-2 align-items-start mb-2">
        <div class="col-7">
          <select v-model="tank.product_tank_id" class="form-select"
            :class="{ 'is-invalid': v$.tanks.$each.$response.$data[index].product_tank_id.$error && submitted }">
            <option value="">Selecione um tanque</option>
            <option v-for="option in tanksOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
          <div v-if="v$.tanks.$each.$response.$data[index].product_tank_id.$error && submitted"
            class="invalid-feedback">
            Campo necessário
          </div>
        </div>

        <div class="col-auto d-flex align-items-start">
          <button type="button" class="btn btn-lg btn-danger" @click="form.tanks.splice(index, 1)">
            <mdicon name="close" />
          </button>
        </div>
      </div>
      <button @click="submit" class="btn btn-primary mb-4 btn-lg">Salvar</button>
    </BaseBlock>
  </div>
</template>
