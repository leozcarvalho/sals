<script setup>
import { ref, watch, onMounted, nextTick, useAttrs } from "vue";
import { ApiClient } from "@/services/genericApi";

const props = defineProps({
  modelValue: {
    type: [String, Number, null],
    default: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["update:modelValue"]);

const pinGroups = ref([]);
const loading = ref(false);
const api = new ApiClient("/device-pins/grouped/options");

// Valor interno
const selected = ref(props.modelValue);

// Mantém selected sincronizado com o parent
watch(
  () => props.modelValue,
  (val) => {
    selected.value = val;
  },
  { immediate: true }
);

watch(selected, (val) => {
  emit("update:modelValue", val === "" || val === "null" ? null : Number(val));
});

// Carrega pins e reatribui valor inicial depois
const loadPins = async () => {
  loading.value = true;
  try {
    const res = await api.getList();
    pinGroups.value = res.data || [];

    // Aguarda DOM e reatribui valor após carregamento
    await nextTick();
    selected.value = props.modelValue;
  } finally {
    loading.value = false;
  }
};
const attrs = useAttrs();

onMounted(loadPins);
</script>

<template>
  <div>
    <select
      class="form-select"
      :disabled="disabled || loading"
      v-model="selected"
      v-bind="attrs"
    >
      <option value="">Selecione um pino</option>
      <template v-for="group in pinGroups" :key="group.board">
        <optgroup :label="group.board">
          <option
            v-for="pin in group.pins"
            :key="pin.id"
            :value="pin.id"
            :disabled="pin.in_use"
          >
            {{ pin.name }}
          </option>
        </optgroup>
      </template>
    </select>
    <small v-if="loading" class="text-muted">Carregando...</small>
  </div>
</template>
