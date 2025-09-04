<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import { can } from '@/helpers/permissions';

const baseList = ref(null);

const userApi = new ApiClient("users");

const cols = reactive([
  { name: "Nome", field: "name", sort: "" },
  { name: "Email", field: "email", sort: "" },
  { name: "Conta", field: "account_name", sort: "" },
]);

const filter = reactive({
  role: null,
  name: null,
  email: { filter_value: null, filter_with: null },
  phone_number: null,
  account_id: null,
  skip: 0,
  limit: 10,
  sort_by: null,
  order_desc: false,
  id: null,
});

const applyFilter = () => {
  filter.skip = 0;
  baseList.value?.refresh();
};

</script>

<template>
  <div v-if="can('manage-cruds')">
    <BaseList
      ref="baseList"
      :title="'Usuários'"
      :api="userApi"
      :cols="cols"
      :filter="filter"
      v-model:filter="filter"
      :exportable="true"
      :formPath="'user-form'"
    >
      <template #filter>
        <div class="row g-3 px-3 py-3">
          <div class="col-md-4">
            <label class="form-label">Nome</label>
            <input v-model="filter.name" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Email</label>
            <input v-model="filter.email.filter_value" class="form-control" />
          </div>
          <div class="col-md-4">
            <label class="form-label">Conta</label>
            <VAsyncSelect entity="accounts" v-model="filter.account_id" :pre-filled-value="filter.account_id" />
          </div>
          <div class="col-12 text-center mt-3">
            <button class="btn btn-success" @click="applyFilter">Filtrar</button>
          </div>
        </div>
      </template>
    </BaseList>
  </div>
</template>
