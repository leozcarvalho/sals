<script setup>
import { reactive, computed, onMounted, ref, defineEmits } from "vue";
import { userApi } from "../services/usersApi"

const emit = defineEmits(['shedSelected'])

const sheds = ref([])
const refresh = async () => {
  const res = await userApi.getCurrentUser()
  sheds.value = res.data.sheds || []
};

onMounted(() => {
  refresh();
});

const selectShed = (selectedShed) => {
  sheds.value.forEach((shed) => {
    shed.checked = false;
  });

  selectedShed.checked = true;
  emit('shedSelected', selectedShed)
};
</script>

<style scoped>
.selected {
  border: 2px solid #007bff; /* Estilo para a imagem selecionada */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 0.5rem;
}

.shed-button {
  min-width: 75%;
}

@media (max-width: 600px) {
  .shed-button {
    min-width: 75%;
  }
}
</style>

<template>
  <div class="d-flex flex-column mb-0 p-md-3">
    <div container>
      <div class="row">
        <div
          v-for="shed in sheds"
          class="col-4 px-md-0 py-2 d-flex justify-content-around"
        >
          <button
            :class="[
              'btn btn-secondary shed-button',
              { selected: true === shed.checked },
            ]"
            name="sheds"
            :id="shed.id"
            autocomplete="off"
            :checked="shed.checked"
            @click="selectShed(shed)"
          >
            <div class="col-12">
              <i class="fa fa-warehouse" />
            </div>
            <div class="col">{{ shed.name }}</div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
