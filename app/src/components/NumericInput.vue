<script setup>
import { computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },

  /** integer | decimal */
  type: {
    type: String,
    default: 'decimal',
  },

  min: Number,
  max: Number,
});

const emit = defineEmits(['update:modelValue']);

// always show the value as string in the input
const normalizedValue = computed(() => {
  return props.modelValue !== null && props.modelValue !== undefined
    ? String(props.modelValue)
    : '';
});

const sanitize = (value) => {
  if (value === null || value === undefined) return '';
  value = String(value).replace(',', '.');

  if (props.type === 'integer') {
    return value.replace(/[^0-9]/g, '');
  }

  // decimal
  value = value.replace(/[^0-9.]/g, '');

  const parts = value.split('.');
  if (parts.length > 2) {
    value = parts.shift() + '.' + parts.join('');
  }

  return value;
};

const onBeforeInput = (e) => {
  // permite apagar, setas, etc
  const inputType = e.inputType || '';
  if (inputType.startsWith('delete')) return;

  const data = e.data ?? '';

  if (props.type === 'integer') {
    if (!/^[0-9]+$/.test(data)) {
      e.preventDefault();
    }
    return;
  }

  // decimal
  if (!/^[0-9.,]+$/.test(data)) {
    e.preventDefault();
  }
};

const onInput = (e) => {
  let value = sanitize(e.target.value);

  // convert to numeric if possible
  if (value === '') {
    emit('update:modelValue', null);
    return;
  }

  let numeric;
  if (props.type === 'integer') {
    numeric = parseInt(value, 10);
    if (Number.isNaN(numeric)) {
      emit('update:modelValue', null);
      return;
    }
  } else {
    numeric = parseFloat(value);
    if (Number.isNaN(numeric)) {
      emit('update:modelValue', null);
      return;
    }
  }

  // clamp to min/max when provided
  if (props.min !== undefined && numeric < props.min) numeric = props.min;
  if (props.max !== undefined && numeric > props.max) numeric = props.max;

  emit('update:modelValue', numeric);
};

const onPaste = (e) => {
  e.preventDefault();
  const text = e.clipboardData.getData('text');
  const value = sanitize(text);
  if (value === '') {
    emit('update:modelValue', null);
    return;
  }
  const numeric = props.type === 'integer' ? parseInt(value, 10) : parseFloat(value);
  if (Number.isNaN(numeric)) {
    emit('update:modelValue', null);
    return;
  }
  emit('update:modelValue', numeric);
};
</script>

<template>
  <input
    v-bind="$attrs"
    :value="normalizedValue"
    type="text"
    :inputmode="props.type === 'integer' ? 'numeric' : 'decimal'"
    class="form-control"
    @beforeinput="onBeforeInput"
    @input="onInput"
    @paste="onPaste"
  />
</template>
