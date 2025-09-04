<script setup>
import { reactive, computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useTemplateStore } from "@/stores/template";
import { getLogo } from "@/helpers/subDomainHelper"

// Vuelidate, for more info and examples you can check out https://github.com/vuelidate/vuelidate
import useVuelidate from "@vuelidate/core";
import { required, email, minLength, sameAs } from "@vuelidate/validators";
import { userApi } from "../../services/usersApi";
import { handleApiToast } from "../../components/toast";

// Main store and Router
const store = useTemplateStore();
const router = useRouter();
const route = useRoute();

const loading = ref(false);

// Input state variables
const state = reactive({
  password: null,
  confirmPassword: null,
});

// Validation rules
const rules = computed(() => {
  return {
    password: {
      required,
      minLength: minLength(6),
    },
    confirmPassword: {
      required,
      sameAs: sameAs(state.password),
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
    loading.value = true;
    const token = route.query.token;
    const data = {
      new_password: state.password,
      confirm_new_password: state.confirmPassword,
      token: token,
    }
    const res = await userApi.createPassword(data);
    handleApiToast(res, "Senha criada com sucesso");
    loading.value = false;
    if (res.success) router.push({ name: "auth-signin" });
  }
}

const showPassword = ref(false);
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const showPasswordConfirm = ref(false);
const togglePasswordConfirmVisibility = () => {
  showPasswordConfirm.value = !showPasswordConfirm.value;
};
</script>

<template>
  <!-- Page Content -->
  <div class="hero-static d-flex align-items-center">
    <div class="content">
      <div class="row justify-content-center push">
        <div class="col-md-8 col-lg-6 col-xl-4">
          <!-- Sign In Block -->
          <BaseBlock title="Cadastre sua nova senha" class="mb-0">
            <div v-if="loading" class="text-center my-5">
              <i class="fa fa-4x fa-cog fa-spin text-warning"></i>
            </div>
            <div v-else>
              <div class="text-center p-4">
                <img
                  :src="getLogo()"
                  alt="Logo"
                  style="max-width: 250px"
                />
              </div>
              <div class="p-sm-3 px-lg-4 px-xxl-5 py-lg-5">
                <!-- Sign In Form -->
                <form>
                  <div class="p-sm-3 px-lg-4 px-xxl-5 py-lg-5">
                    <div class="mb-4">
                      <div class="input-group">
                        <input
                          :type="showPassword ? 'text' : 'password'"
                          class="form-control form-control-alt form-control-lg"
                          id="login-password"
                          name="login-password"
                          placeholder="Senha"
                          :class="{
                            'is-invalid': v$.password.$errors.length,
                          }"
                          v-model="state.password"
                          @blur="v$.password.$touch"
                        />
                        <button
                          class="btn btn-outline-secondary"
                          @click.prevent="togglePasswordVisibility"
                        >
                          <i
                            :class="
                              showPassword ? 'fa fa-eye-slash' : 'fa fa-eye'
                            "
                          ></i>
                        </button>
                      </div>
                      <div
                        v-if="v$.password.$errors.length"
                        class="invalid-feedback animated fadeIn"
                      >
                        Senha é obrigatória
                      </div>
                    </div>
                    <div>
                      <div class="input-group">
                        <input
                          :type="showPasswordConfirm ? 'text' : 'password'"
                          class="form-control form-control-alt form-control-lg"
                          id="login-confirm-password"
                          name="login-confirm-password"
                          placeholder="Confirme sua Senha"
                          :class="{
                            'is-invalid': v$.confirmPassword.$errors.length,
                          }"
                          v-model="state.confirmPassword"
                          @blur="v$.confirmPassword.$touch"
                        />
                        <button
                          class="btn btn-outline-secondary"
                          @click.prevent="togglePasswordConfirmVisibility"
                        >
                          <i
                            :class="
                              showPasswordConfirm
                                ? 'fa fa-eye-slash'
                                : 'fa fa-eye'
                            "
                          ></i>
                        </button>
                      </div>
                      <div
                        v-if="v$.confirmPassword.required.$invalid"
                        class="invalid-feedback animated fadeIn"
                      >
                        Confirme sua senha
                      </div>
                      <div
                        v-else-if="v$.confirmPassword.sameAs.$invalid"
                        class="invalid-feedback animated fadeIn"
                      >
                        Senhas não coincidem!
                      </div>
                    </div>

                    <div class="my-3">
                      Sua senha deve conter:
                      <ul>
                        <li
                          :class="
                            !v$.password.minLength.$invalid &&
                            !v$.password.required.$invalid
                              ? 'text-check'
                              : ''
                          "
                        >
                          No mínimo
                          {{ v$.password.minLength.$params.min }} caracteres
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="row mb-5">
                    <div class="">
                      <button
                        class="btn rounded btn-warning green-dark border-0 text-light w-100"
                        @click="onSubmit"
                      >
                        Confirmar
                      </button>
                    </div>
                  </div>
                  <div class="text-center">
                    <span> Lembrou? </span>
                    <br />
                    <br />
                    <RouterLink
                      :to="{ name: 'auth-signin' }"
                      class="btn-primary"
                      >Ir para o login</RouterLink
                    >
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

.text-check {
  color: lightgray;
  text-decoration: line-through;
}
</style>
