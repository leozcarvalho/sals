<template>
  <div class="d-flex align-items-center mb-1">
    <div class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-danger bg-danger-light me-2">
      {{ value }}%
    </div>
    <div class="progress flex-grow-1">
      <div
        class="progress-bar progress-bar-striped progress-bar-animated"
        role="progressbar"
        :style="{ width: value + '%' }"
        :aria-valuenow="value"
        aria-valuemin="0"
        aria-valuemax="100"
      >
      </div>
    </div>
  </div>
</template>
  
  <script>
  export default {
    name: 'ProgressBar',
    props: {
      value: {
        type: Number,
        required: true
      }
    }
  }
  </script>
  
  <style scoped>
  /* Adicione estilos personalizados aqui, se necessário */
  </style>
  