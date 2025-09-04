<script>
import { useCurrencyInput } from 'vue-currency-input'

export default {
  name: 'CurrencyInput',
  props: {
    modelValue: Number, // Vue 2: value
    options: Object,
  },
  setup(props) {
    const { inputRef } = useCurrencyInput({ currency: 'BRL' })

    return { inputRef }
  }
}
</script>

<template>
  <input ref="inputRef" type="text" />
</template>
