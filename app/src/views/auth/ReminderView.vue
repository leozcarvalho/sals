<script setup>
import { reactive, computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useTemplateStore } from "@/stores/template";
import { vMaska } from "maska";

// Vuelidate, for more info and examples you can check out https://github.com/vuelidate/vuelidate
import useVuelidate from "@vuelidate/core";
import { required, email } from "@vuelidate/validators";
import { userApi } from "../../services/usersApi"
import { handleApiToast } from "../../components/toast";


// Main store and Router
const store = useTemplateStore();
const router = useRouter();

const loading = ref(false)

// Input state variables
const state = reactive({
  email: null
});

// Validation rules
const rules = computed(() => {
  return {
    email: {
      required,
      email
    },
  };
});

// Use vuelidate
const v$ = useVuelidate(rules, state);

// On form submission
async function onSubmit() {
  const result = await v$.value.$validate();

  if (!result) {
    // notify user form is invalid
    return;
  } else {
    loading.value = true
    const res = await userApi.recoveryPassword(state.email)
    handleApiToast(res, "Email de recuperação enviado com sucesso");
    loading.value = false
    if (res.success) router.push({ name: "auth-signin" });
  }
}
</script>

<template>
  <!-- Page Content -->
  <div class="hero-static d-flex align-items-center">
    <div class="content">
      <div class="row justify-content-center push">
        <div class="col-md-8 col-lg-6 col-xl-4">
          <!-- Sign In Block -->
          <BaseBlock title="Recuperação de senha" class="mb-0">
            <div v-if="loading" class="text-center my-5">
              <i class="fa fa-4x fa-cog fa-spin text-warning"></i>
            </div>
            <div v-else>
              <div class="text-center p-4">
                <img src="../../assets/img/sals.png" style="max-width: 250px;" alt="Logo"/>
              </div>
              <div class="p-sm-3 px-lg-4 px-xxl-5 py-lg-5">
                <!-- Sign In Form -->
                <form @submit.prevent="onSubmit">
                  <div class="py-3">
                    <div class="mb-4">
                      <input type="text" class="form-control form-control-alt form-control-lg" placeholder="Email *"
                        :class="{
                          'is-invalid': v$.email.$errors.length,
                        }" v-model="state.email" @blur="v$.email.$touch" />
                      <div v-if="v$.email.required.$invalid" class="invalid-feedback animated fadeIn">
                        Email é necessário
                      </div>
                      <div v-else-if="v$.email.email" class="invalid-feedback animated fadeIn">
                        Formato de email inválido
                      </div>
                    </div>
                  </div>
                  <div class="row mb-5">
                    <div class="">
                      <button class="btn rounded btn-warning green-dark border-0 text-light w-100">
                        ENVIAR
                      </button>
                    </div>
                  </div>
                  <div class="text-center">
                    <span>
                      Lembrou?
                    </span>
                    <br />
                    <br />
                    <RouterLink :to="{ name: 'auth-signin' }" class="btn-primary">Ir para o login</RouterLink>
                  </div>
                </form>
                <!-- END Sign In Form -->
              </div>
            </div>
          </BaseBlock>
          <!-- END Sign In Block -->
        </div>
      </div>
    </div>
  </div>
  <!-- END Page Content -->
</template>

<style>
.block.block-rounded {
  border-radius: 0%;
}

.full-btn {
  width: 100%;
  height: 3rem;
}
</style>
