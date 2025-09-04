<script setup>
import { reactive, computed, onMounted, ref, defineEmits } from "vue";

const emit = defineEmits()

const props = defineProps({
  perPage: {
    type: Number,
    default: 10,
    description: "Items per page",
  },
  totalRows: {
    type: Number,
    default: 50,
    description: "Total items",
  },
})

const currentPage = ref(1)

const totalPages = computed(() => parseInt(Math.ceil(props.totalRows / props.perPage)))

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    emit('changePage', page)
  }
}

const firstPage = computed(() => {
  const leftOffset = 2;
  return Math.max(1, currentPage.value - leftOffset);
})

const lastPage = computed(() => {
  const rightOffset = 2;
  return Math.min(totalPages.value, currentPage.value + rightOffset);
})

const pages = computed(() => {
  const range = [];
  for (let i = firstPage.value; i <= lastPage.value; i++) {
    range.push(i);
  }
  if (firstPage.value > 2) range.unshift('...');
  if (firstPage.value > 1) range.unshift(1);
  if (lastPage.value < totalPages.value - 1) range.push('...');
  if (lastPage.value < totalPages.value) range.push(totalPages.value);
  return range;
})

</script>

<template>
  <div class="d-flex flex-md-row flex-column justify-content-center align-items-center mt-5">
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage <= 1 }">
          <a class="page-link" @click="changePage(currentPage - 1)">Anterior</a>
        </li>
        <li v-for="page in pages" :key="page" class="page-item" :class="{ active: page === currentPage, disabled: page === '...' }">
          <a class="page-link" @click="page !== '...' && changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage >= totalPages }">
          <a class="page-link" @click="changePage(currentPage + 1)">Próxima</a>
        </li>
      </ul>
    </nav>
  </div>
</template>
