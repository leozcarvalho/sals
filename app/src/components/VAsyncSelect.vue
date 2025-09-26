<script setup>
import { ref, watch, onMounted } from 'vue';
import VueMultiselect from 'vue-multiselect';
import { ApiClient } from "../services/genericApi";

const props = defineProps({
  modelValue: [String, Number, Object, Array, Boolean],
  entity:  {
    type: String,
  },
  fieldKey:  {
    type: String,
    default: 'name'
  },
  preFilledValue: {
    type: Number,
    default: null,
  },
  invalidFeedback: {
    type: Object,
    default: {},
  },
});

const api = new ApiClient("/" + props.entity);
const emit = defineEmits(['update:modelValue', 'item-selected']);
const internalValue = ref(props.modelValue);

watch(() => props.modelValue, async (newValue) => {
  if (typeof newValue === 'number') {
    const result = await api.get(newValue);
    internalValue.value = result.data;
  } else {
    internalValue.value = newValue;
  }
});

watch(internalValue, (newValue) => {
  emit('update:modelValue', newValue ? newValue.id : null);
});

const fetchPreFilledValue = async () => {
  if (props.preFilledValue) {
    const result = await api.get(props.preFilledValue);
    internalValue.value = result.data;
  }
};
fetchPreFilledValue()
const options = ref([]);
const search = async ($event) => {
  if ($event.length > 2) {
    let filter = {
      search: $event,
      limit: 5
    }
    let result = await api.getList(filter);
    options.value = result.data.items;
  }
}

onMounted(async () => {
  const result = await api.getList({'limit': 5});
  options.value = result.data.items;
});

const onSelect = (selectedItem) => {
  emit('item-selected', selectedItem);
};
</script>

<template>
  <VueMultiselect v-model="internalValue" tag-placeholder="Selecione" placeholder="Selecione" selectLabel=""
    deselectLabel="" selectedLabel="X" :label="fieldKey" track-by="id" :options="options" @search-change="search" @select="onSelect">
    <template #noOptions>Digite para buscar</template>
    <template #noResult>Nenhum resultado encontrado</template>
  </VueMultiselect>
  <div v-if="invalidFeedback.isInvalid" style="color: #e76868;">
    {{ invalidFeedback.message }}
  </div>
</template>

<style>
.multiselect {
  border: 1px !important;
}

.multiselect__tags {
  background-color: #09111d !important;
  border-color: #192f4d !important;
  appearance: none;
  border-radius: 0.375rem;
}

.multiselect__tags * {
  background-color: inherit;
  color: inherit;
  padding: 0%;
}
.multiselect--above {
  background-color: #09111d !important;
  border-color: #192f4d !important;
}

.multiselect__single {
  background-color: inherit;
}
.multiselect__input-wrapper {
  background-color: inherit;
}
.multiselect__content-wrapper {
  background-color: inherit;
}
</style>
