<script setup>
import variableImages from "./VariableImages";
import { onMounted, defineEmits } from "vue";

const emit = defineEmits(['variableSelected'])

const toggleSelectImage = (selectedImage) => {
  variableImages.value.forEach((image) => {
    image.selected = false;
  });
  selectedImage.selected = true;
  emit('variableSelected', selectedImage?.value)
};

onMounted(() => {
  variableImages.value.forEach((image) => {
    image.selected = false;
  });
});
</script>

<style scoped>
.variable-image {
  max-height: 6rem;
  border-radius: 0.6rem;
}

.variable-button {
  max-width: 25rem;
  margin-bottom: 1rem;
  background-color: #2a384b;
  border-radius: 0.5rem;
  cursor: pointer;
}

@media (max-width: 600px) {
  .variable-button {
    max-width: 12rem;
    max-height: 14rem;
    margin-bottom: 1rem;
    background-color: #2a384b;
    border-radius: 0.5rem;
    cursor: pointer;
  }
}

.variable-button:hover {
  scale: 1.05;
  transition: all 0.2s ease-in-out;
}
.selected {
  border: 2px solid #007bff; /* Estilo para a imagem selecionada */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
}
</style>

<template>
  <div>
    <h3>Selecione a variável</h3>
    <div container>
      <div class="row d-flex justify-content-between">
        <div
          v-for="(image, index) in variableImages"
          :class="{
            'col-md-4 col-6 variable-button': true,
            selected: true === image.selected,
          }"
          :key="index"
        >
          <div
            @click="toggleSelectImage(image)"
            :class="{
              'row py-4 d-flex justify-content-between align-items-center': true,
            }"
          >
            <div class="col-md-3">
              <img :src="image.src" :alt="image.alt" class="variable-image" />
            </div>
            <div class="col-md-9 pt-md-0 pt-3">
              <h5 class="mb-0">
                {{ image.alt }}
              </h5>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
