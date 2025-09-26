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
  { name: "Nome", field: "name" },
  { name: "Email", field: "email" },
  { name: "Perfil", field: "profile", formatter: (item) => item.name },
]);

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
</script>

<template>
  <div>
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
    <BaseList
      ref="baseList"
      :title="'Usuários'"
      :api="userApi"
      :cols="cols"
      :permission="'manage_user'"
      @create="modalForm.openModal(true)"
      @edit="userSelected = $event; modalForm.openModal()"
    />
  </div>
</template>
