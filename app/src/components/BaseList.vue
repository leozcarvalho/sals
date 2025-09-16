<script setup>
import { ref, onMounted, defineExpose } from "vue";
import Paginator from "./Paginator.vue";
import { useRouter } from "vue-router";
import { handleApiToast } from "../components/toast";
import { Dataset, DatasetItem } from "vue-dataset";
import { can } from "../helpers/userSession";

const props = defineProps({
  api: { type: Object, required: true },
  formPath: { type: String, default: "" },
  cols: { type: Array, required: true },
  title: { type: String, default: "Lista" },
  canCreate: { type: Boolean, default: true },
  canEdit: { type: Boolean, default: true },
  canDelete: { type: Boolean, default: true },
  exportable: { type: Boolean, default: false },
  canFilter: { type: Boolean, default: false },
  filter: { type: Object, default: {} },
  canPaginate: { type: Boolean, default: false },
  permission: { type: String, default: null },
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
  if (!props.filter) return;
  props.filter.skip = perPage.value * (page - 1);
  emit("update:filter", props.filter);
  refresh();
};

const changePerPage = () => {
  if (!props.filter) return;
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
  <div class="content" v-if="props.permission === null || can(props.permission)">
    <BaseBlock :title="title" content-full>
      <!-- Ações -->
      <div class="d-flex justify-content-between mb-2">
        <div>
          <button class="btn btn-lg btn-primary" @click="toggleFilter" v-if="canFilter">
            <mdicon name="filter" />
          </button>
          <select v-if="canPaginate" v-model="perPage" @change="changePerPage" class="form-select d-inline w-auto ms-2">
            <option v-for="option in pages" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>
        <div>
          <slot name="extra-actions"></slot>
          <button v-if="canCreate" class="btn btn-lg btn-outline-success" @click="$emit('create')"> 
            <i class="fa fa-plus"></i>
          </button>
          <button v-if="exportable" class="btn btn-lg btn-success ms-2" @click="exportList">
            <mdicon name="file-excel" />
          </button>
        </div>
      </div>

      <!-- Slot para formulário de filtro (pai) -->
      <div v-if="showFilter" class="mb-3">
        <slot name="filter"></slot>
      </div>

      <!-- Tabela -->
      <Dataset v-slot="{ ds }" :ds-data="items" :ds-sortby="props.filter.sort_by ? [props.filter.sort_by] : []">
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
                      {{ col.formatter ? col.formatter(row[col.field], row) : row[col.field] }}
                    </slot>
                  </td>
                  <td v-if="canEdit || canDelete || $slots['row-actions']">
                    <div class="btn-group">
                      <slot name="row-actions" :row="row"></slot>
                      <button v-if="canEdit" class="btn btn-lg btn-outline-warning"
                        @click="$emit('edit', row)">
                        <i class="fa fa-pencil"></i>
                      </button>
                      <button v-if="canDelete" class="btn btn-lg btn-outline-danger" data-bs-toggle="modal"
                        data-bs-target="#modal-delete" @click="idOnDeleting = row.id">
                        <i class="fa fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </template>
            </DatasetItem>
          </table>
        </div>
        <Paginator v-if="canPaginate" :per-page="perPage" :total-rows="totalRows" @change-page="changePage" />
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
