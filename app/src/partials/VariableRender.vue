<template>
  <img
    v-if="imageSrc"
    :src="imageSrc"
    :alt="imageAlt"
    :class="[imageClass, { selected: true === isSelected }]"
    :style="imageStyle"
  />
</template>

<script>
import variableImages from "./VariableImages";

export default {
  name: "VariableRender",
  props: {
    imageName: {
      type: String,
      required: true,
    },
    isSelected: {
      type: Boolean,
      default: false,
    },
    imageClass: {
      type: String,
    },
    imageStyle: {
      type: Object,
    },
  },
  computed: {
    imageSrc() {
      const image = variableImages.value.find(
        (img) => img.name === this.imageName
      );
      return image ? image.src : null;
    },
    imageAlt() {
      const image = variableImages.value.find(
        (img) => img.name === this.imageName
      );
      return image ? image.alt : "Imagem";
    },
  },
};
</script>

<style scoped>
.image-button {
  cursor: pointer;
  margin: 0 10px; /* Espaçamento entre as imagens */
}

.image-button:hover {
  transform: scale(1.05); /* Efeito ao passar o mouse */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.selected {
  border: 3px solid #007bff; /* Estilo para a imagem selecionada */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
