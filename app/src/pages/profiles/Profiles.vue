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
  { name: "Permissões", field: "permissions", formatter: (value, row) => getPermissionLabels(row.permissions).join(", "), sort: "" },
]);

const onProfileSaved = () => {
  baseList.value.refresh();
  profileSelected.value = null;
};

const permissionsOptions = ref([]);

onMounted(async () => {
  const res = await profilesApi.getPermissions();
  permissionsOptions.value = res.data;
});

const getPermissionLabels = (permissionKeys) => {
  if (!permissionKeys) return [];
  return permissionKeys.map((key) => {
    const opt = permissionsOptions.value.find((p) => p.value === key);
    return opt ? opt.label : key;
  });
};
</script>

<template>
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
  <BaseList
    ref="baseList"
    :title="'Perfis'"
    :api="profilesApi"
    :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="profileSelected = $event; modalForm.openModal()"
  />
</template>
