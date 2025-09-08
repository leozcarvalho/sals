<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import BaseList from "../../components/BaseList.vue";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { ProfilesClient } from "../../services/profilesApi";

const profilesApi = new ProfilesClient();

const baseList = ref(null);
const modalForm = ref(null);
const profileSelected = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Permissões", field: "permissions", sort: "" },
]);

const filter = reactive({
  name: null,
});

const onProfileSaved = () => {
  baseList.value.refresh();
  profileSelected.value = null;
};

const openModal = () => {
  modalForm.value.openModal();
};

// Opções de permissões carregadas da API
const permissionsOptions = ref([]);

onMounted(async () => {
  const res = await profilesApi.getPermissions();
  permissionsOptions.value = res.data; // [{ value: "manage_user", label: "Gerenciar Usuários" }, ...]
});

// Função utilitária para pegar labels traduzidos
const getPermissionLabels = (permissionKeys) => {
  if (!permissionKeys) return [];
  return permissionKeys.map((key) => {
    const opt = permissionsOptions.value.find((p) => p.value === key);
    return opt ? opt.label : key; // fallback para a key caso não encontre
  });
};
</script>

<template>
  <!-- Modal para criar/editar perfil -->
  <BaseModalForm
    ref="modalForm"
    v-model="profileSelected"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'permissions', label: 'Permissões', slot: 'permissionsSlot', multiple: true }
    ]"
    :api="profilesApi"
    @saved="onProfileSaved"
    @close="profileSelected = null"
  >
    <template #permissionsSlot="{ model, field }">
      <div class="d-flex flex-column">
        <div
          class="form-check"
          v-for="opt in permissionsOptions"
          :key="opt.value"
        >
          <input
            class="form-check-input"
            type="checkbox"
            :id="`perm-${opt.value}`"
            :value="opt.value"
            v-model="model[field.name]"
          />
          <label class="form-check-label" :for="`perm-${opt.value}`">
            {{ opt.label }}
          </label>
        </div>
      </div>
    </template>
  </BaseModalForm>

  <!-- Listagem de perfis -->
  <BaseList
    ref="baseList"
    :title="'Perfis'"
    :api="profilesApi"
    :cols="cols"
    :exportable="false"
    :can-create="false"
    :can-edit="false"
    :filter="filter"
    v-model:filter="filter"
  >
    <!-- Botão criar -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="openModal">
        <mdicon name="plus" />
      </button>
    </template>

    <!-- Filtros -->
    <template #filter>
      <div class="row px-5 py-5">
        <div class="col-md-4">
          <label class="form-label">Nome</label>
          <input v-model="filter.name" class="form-control" />
        </div>
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success" @click="baseList.refresh()">FILTRAR</button>
        </div>
      </div>
    </template>

    <!-- Renderização personalizada da coluna permissions -->
    <template #cell-permissions="{ row }">
      <span>
        {{ getPermissionLabels(row.permissions).join(", ") }}
      </span>
    </template>

    <!-- Ações de linha -->
    <template #row-actions="{ row }">
      <button
        class="btn btn-sm btn-warning text-white"
        @click="profileSelected = row; openModal()"
      >
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>

<style lang="scss" scoped>
@import url('../../assets/scss/custom/_tablestyle.scss');

.last-read {
  cursor: pointer;
}
</style>
