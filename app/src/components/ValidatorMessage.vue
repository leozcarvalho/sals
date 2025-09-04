<script setup>
import { defineProps, computed, onMounted, ref } from "vue";

const props = defineProps({
  isActive: {
    type: Boolean,
    description: "Is active",
  },
  type: {
    type: String,
    description: "Type",
    default: 'required'
  },
});

const message = computed(() => {
  if (props.type == 'required') return 'Campo obrigatório'
})

</script>

<template>
  <div v-if="props.isActive" class="invalid-feedback animated fadeIn">
    {{ message }}
  </div>
</template>

