<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { ApiClient } from "../../services/genericApi";

const baseList = ref(null);
const modalForm = ref(null);

const userApi = new ApiClient("/users");
const profilesApi = new ApiClient("/profiles");

const cols = reactive([
  { name: "Nome", field: "name", sort: "" },
  { name: "Email", field: "email", sort: "" },
  { name: "Perfil", field: "profile_name", sort: "" },
]);

const filter = reactive({
  name: null,
  email: null,
});

const profilesOptions = ref([]);
onMounted(async () => {
  const res = await profilesApi.getList({ per_page: 1000 });
  profilesOptions.value = res.data.items.map((p) => ({
    label: p.name,
    value: p.id,
  }));
});

const userSelected = ref(null);

const onUserSaved = () => {
  baseList.value.refresh();
  userSelected.value = null;
};

const openModal = () => {
  modalForm.value.openModal();
};
</script>

<template>
  <div>
    <!-- Modal de Criação/Edição -->
    <BaseModalForm
      ref="modalForm"
      v-model="userSelected"
      :fields="[
        { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
        { name: 'email', label: 'Email', type: 'email', rules: 'required' },
        { name: 'password', label: 'Senha', type: 'password', rules: 'required' },
        { name: 'profile_id', label: 'Perfil', type: 'select', options: profilesOptions, rules: 'required' }
      ]"
      :api="userApi"
      @saved="onUserSaved"
      @close="userSelected = null"
    />

    <!-- Lista de Usuários -->
    <BaseList
      ref="baseList"
      :title="'Usuários'"
      :api="userApi"
      :cols="cols"
      :filter="filter"
      v-model:filter="filter"
      :exportable="true"
      :can-create="false"
      :can-edit="false"
      :permission="'manage_user'"
    >
      <!-- Botão Criar -->
      <template #extra-actions>
        <button type="button" class="btn btn-sm btn-success ms-2" @click="openModal">
          <mdicon name="plus" />
        </button>
      </template>

      <!-- Filtros -->
      <template #filter>
        <div class="row g-3 px-3 py-3">
          <div class="col-md-4">
            <label class="form-label">Nome</label>
            <input v-model="filter.name" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Email</label>
            <input v-model="filter.email" class="form-control" />
          </div>
          <div class="col-12 text-center mt-3">
            <button class="btn btn-success" @click="baseList.refresh()">Filtrar</button>
          </div>
        </div>
      </template>

      <!-- Ações de Linha -->
      <template #row-actions="{ row }">
        <button
          class="btn btn-sm btn-warning text-white"
          @click="userSelected = row; openModal()"
        >
          <mdicon name="circle-edit-outline" />
        </button>
      </template>
    </BaseList>
  </div>
</template>

<style lang="scss" scoped>
@import url("../../assets/scss/custom/_tablestyle.scss");

.last-read {
  cursor: pointer;
}
</style>
