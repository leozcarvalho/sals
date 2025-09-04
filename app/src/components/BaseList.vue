<script setup>
import { ref, onMounted, defineExpose } from "vue";
import Paginator from "./Paginator.vue";
import { useRouter } from "vue-router";
import { handleApiToast } from "../components/toast";
import { Dataset, DatasetItem } from "vue-dataset";

// Props
const props = defineProps({
  api: { type: Object, required: true }, // agora a API vem do pai
  formPath: { type: String, default: "" },
  cols: { type: Array, required: true },
  title: { type: String, default: "Lista" },
  canCreate: { type: Boolean, default: true },
  canEdit: { type: Boolean, default: true },
  canDelete: { type: Boolean, default: true },
  exportable: { type: Boolean, default: true },
  filter: { type: Object, required: true }, // filtro controlado pelo pai
});

// Emit
const emit = defineEmits(["update:filter"]);

// Estado
const items = ref([]);
const totalRows = ref(0);
const perPage = ref(props.filter.limit || 10);
const pages = ref([5, 10, 25, 50, 100]);
const idOnDeleting = ref(null);
const showFilter = ref(false);

const router = useRouter();

// Funções
const refresh = async () => {
  const res = await props.api.getList(props.filter);
  items.value = res.data.items || res.data.data?.items || [];
  totalRows.value = res.data.count || res.data.data?.count || 0;
};

defineExpose({
  refresh,
});

const toggleFilter = () => {
  showFilter.value = !showFilter.value;
};

const changePage = (page) => {
  props.filter.skip = perPage.value * (page - 1);
  emit("update:filter", props.filter);
  refresh();
};

const changePerPage = () => {
  props.filter.limit = perPage.value;
  props.filter.skip = 0;
  emit("update:filter", props.filter);
  refresh();
};

const onSort = (i) => {
  props.filter.sort_by = props.cols[i].field;
  props.filter.order_desc = !props.filter.order_desc;

  props.cols.forEach((col, index) => {
    col.sort = index === i ? (props.filter.order_desc ? "desc" : "asc") : "";
  });

  emit("update:filter", props.filter);
  refresh();
};

const deleteItem = async () => {
  if (!idOnDeleting.value) return;
  const res = await props.api.delete(idOnDeleting.value);
  handleApiToast(res, "Item excluído com sucesso");
  refresh();
};

const exportList = async () => {
  if (!props.exportable) return;
  await props.api.export(props.filter);
};

onMounted(() => {
  refresh();
});
</script>

<template>
  <div class="content">
    <BaseBlock :title="title" content-full>
      <!-- Ações -->
      <div class="d-flex justify-content-between mb-2">
        <div>
          <button class="btn btn-sm btn-primary" @click="toggleFilter">
            <mdicon name="filter" />
          </button>
          <select v-model="perPage" @change="changePerPage" class="form-select d-inline w-auto ms-2">
            <option v-for="option in pages" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>
        <div>
          <slot name="extra-actions"></slot>
          <button v-if="canCreate" class="btn btn-sm btn-success" @click="router.push({ name: props.formPath })">
            <mdicon name="plus" />
          </button>
          <button v-if="exportable" class="btn btn-sm btn-success ms-2" @click="exportList">
            <mdicon name="file-excel" />
          </button>
        </div>
      </div>

      <!-- Slot para formulário de filtro (pai) -->
      <div v-if="showFilter" class="mb-3">
        <slot name="filter"></slot>
      </div>

      <!-- Tabela -->
      <Dataset v-slot="{ ds }" :ds-data="items" :ds-sortby="props.filter.sort_by || ''">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th v-for="(th, index) in cols" :key="th.field" :class="['sort', th.sort]" @click="onSort(index)">
                  {{ th.name }}
                </th>
                <th v-if="canEdit || canDelete || $slots['row-actions']">Ações</th>
              </tr>
            </thead>
            <DatasetItem tag="tbody" class="fs-sm">
              <template #default="{ row }">
                <tr>
                  <td v-for="col in cols" :key="col.field">
                    <!-- 🔹 Prioriza slot nomeado pelo field da coluna -->
                    <slot :name="`cell-${col.field}`" :row="row" :value="row[col.field]">
                      {{ row[col.field] }}
                    </slot>
                  </td>
                  <td v-if="canEdit || canDelete || $slots['row-actions']">
                    <div class="btn-group">
                      <slot name="row-actions" :row="row"></slot>
                      <button v-if="canEdit" class="btn btn-sm btn-warning text-white"
                        @click="router.push({ name: props.formPath, query: { id: row.id } })">
                        <mdicon name="circle-edit-outline" />
                      </button>
                      <button v-if="canDelete" class="btn btn-sm btn-danger" data-bs-toggle="modal"
                        data-bs-target="#modal-delete" @click="idOnDeleting = row.id">
                        <mdicon name="delete-circle-outline" />
                      </button>     
                    </div>
                  </td>
                </tr>
              </template>
            </DatasetItem>
          </table>
        </div>
        <Paginator :per-page="perPage" :total-rows="totalRows" @change-page="changePage" />
      </Dataset>

    </BaseBlock>

    <!-- Modal de deleção -->
    <div class="modal fade" id="modal-delete" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">Confirmar Ação</div>
          <div class="modal-body">Deseja realmente excluir este item?</div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-danger" data-bs-dismiss="modal" @click="deleteItem">Confirmar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
