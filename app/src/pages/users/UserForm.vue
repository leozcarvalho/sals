<script setup>
import { reactive, computed, onMounted, ref } from "vue";
import { ApiClient } from "../../services/genericApi";
import { vMaska } from "maska";
import { useRouter, useRoute } from "vue-router";
import useVuelidate from "@vuelidate/core";
import { required, minLength, email } from "@vuelidate/validators";
import { can } from "@/helpers/permissions";
import Loader from "@/components/Loader.vue";
import { handleApiToast } from "../../components/toast";

const api = new ApiClient("users");

const router = useRouter();
const route = useRoute();
const userId = ref(null);

const rules = computed(() => {
  return {
    name: {
      required,
    },
    account_id: {
      required,
    },
    email: {
      required,
      email,
    },
    role: {
      required,
    },
  };
});

const user = reactive({
  name: "",
  email: "",
  phone_number: "",
  password: "",
  role: "",
});


onMounted(async () => {
  userId.value = route.query.id;
  const _user = await api.get(userId.value);
  Object.assign(user, _user.data);
});

const processResponse = (res) => {
  handleApiToast(res, "Usuário salvo com sucesso");
  if (res.success) {
    backToList();
  }
};

const v$ = useVuelidate(rules, user);

const isLoading = ref(false);
const submit = async () => {
  isLoading.value = true;
  const result = await v$.value.$validate();
  if (result) {
    if (userId.value)
      processResponse(await api.update(userId.value, user));
    else processResponse(await api.save(user));
  }
  isLoading.value = false;
};

const backToList = () => {
  router.push({ name: "users-list" });
};
</script>

<template>
  <Loader :loading="isLoading" />
  <div v-if="can('manage-cruds')" class="content">
    <div class="row">
      <div class="col-md-12">
        <form @submit.prevent>
          <BaseBlock :title="userId ? 'Editar Usuário' : 'Novo Usuário'">
            <div class="row justify-content-center py-sm-3 py-md-5">
              <div class="row">
                <div class="col-md-8 mb-4">
                  <label class="form-label">Nome Completo</label>
                  <input v-model="user.name" type="text" class="form-control form-control-alt" :class="{
                    'is-invalid': v$.name.$errors.length,
                  }" @blur="v$.name.$touch" />
                  <div v-if="v$.name.$errors.length" class="invalid-feedback animated fadeIn">
                    Nome é obrigatório
                  </div>
                </div>
                <div class="col-md-4 mb-4">
                  <label class="form-label">Conta</label>
                  <VAsyncSelect entity="accounts" v-model="user.account_id" :pre-filled-value="user.account_id" />
                  <div v-if="v$.account_id.$errors.length" class="small text-danger">
                    Selecione a conta
                  </div>
                </div>
                <div class="col-md-6 mb-4">
                  <label class="form-label">Email *</label>
                  <input v-model="user.email" type="text" class="form-control form-control-alt" :class="{
                    'is-invalid': v$.email.$errors.length,
                  }" @blur="v$.email.$touch" />
                  <div v-if="v$.email.required.$invalid" class="invalid-feedback animated fadeIn">
                    Email é necessário
                  </div>
                  <div v-else-if="v$.email.email" class="invalid-feedback animated fadeIn">
                    Formato de email Inválido
                  </div>
                </div>
                <div class="col-md-3 mb-4">
                  <label class="form-label">Permissões</label>
                  <select v-model="user.role" class="form-control form-control-alt" :class="{
                    'is-invalid': v$.role.$errors.length,
                  }" @blur="v$.role.$touch">
                    <option value="SYSTEM_ADMIN">
                      Administrador do Sistema
                    </option>
                    <option value="ACCOUNT_ADMIN">
                      Administrador da Conta
                    </option>
                    <option value="USER">Usuário</option>
                  </select>
                  <div v-if="v$.role.$errors.length" class="invalid-feedback animated fadeIn">
                    Permissões é obrigatório
                  </div>
                </div>
                <div class="col-md-3 mb-4">
                  <label class="form-label">Status</label>
                  <div class="form-check form-switch">
                    <input v-model="user.is_active" class="form-check-input" type="checkbox"
                      id="flexSwitchCheckChecked">
                    <label class="form-check-label" for="flexSwitchCheckChecked">{{ user.is_active ? 'Ativo' :
                      'Inativo' }}</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="btn-group mb-5 mx-3">
              <button type="button" class="btn btn-sm btn-success text-light" @click="submit">
                <mdicon name="check" />
              </button>
              <button type="button" class="btn btn-sm btn-danger" data-bs-toggle="delete" data-bs-target="#delete"
                @click="backToList">
                <mdicon name="close" />
              </button>
            </div>
          </BaseBlock>
        </form>
      </div>
    </div>
  </div>
</template>
<style scoped>
input[type="text"]:disabled {
  background: rgb(230, 228, 228) !important;
}

.form-control {
  max-height: 38px;
}
</style>
