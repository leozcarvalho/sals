<script setup>
import { reactive, computed, ref } from "vue";
import { useRouter } from "vue-router";

// Vuelidate, for more info and examples you can check out https://github.com/vuelidate/vuelidate
import useVuelidate from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";
import { userApi } from "../../services/usersApi";
import { handleApiToast } from "../../components/toast";
import { getLogo } from "@/helpers/subDomainHelper"
import { useUserStore } from "../../stores/userStore";
import Loader from "@/components/Loader.vue";


const router = useRouter();
const loader = ref(false);

const state = reactive({
  username: null,
  password: null,
  showPassword: false,
});

// Validation rules
const rules = computed(() => {
  return {
    username: {
      required,
      minLength: minLength(3),
    },
    password: {
      required,
      minLength: minLength(5),
    },
  };
});

// Use vuelidate
const v$ = useVuelidate(rules, state);

const userStore = useUserStore();
async function onSubmit() {
  const isValid = await v$.value.$validate();
  if (!isValid) {
    handleApiToast({ success: false, message: "Preencha os campos corretamente." });
    return;
  }

  loader.value.loaderOn()
  try {
    const res = await userApi.auth(state.username, state.password);
    console.log(res)
    handleApiToast(res, "Login efetuado com sucesso!");

    if (res.success) {
      // 🔹 Salva dados essenciais no store (em memória)
      userStore.setUser({
        id: res.data.id,
        permissions: res.data.permissions,
        accessToken: res.access_token, // mantemos só em memória
      });

      router.push({ name: "home" });
    }
  } catch (err) {
    console.error(err);
    handleApiToast({ success: false, message: "Erro no login." });
  } finally {
    loader.value.loaderOff()
  }
}

const togglePasswordVisibility = () => {
  state.showPassword = !state.showPassword;
};
</script>

<template>
  <!-- Page Content -->
  <Loader ref="loader" />
  <div class="hero-static d-flex align-items-center">
    <div class="content">
      <div class="row justify-content-center push">
        <div class="col-md-8 col-lg-6 col-xl-4">
          <!-- Sign In Block -->
          <BaseBlock title="" class="mb-0">
            <div class="text-center p-4">
              <img
                :src="getLogo()"
                alt="Logo VisioAgro"
                style="max-width: 250px"
              />
            </div>
            <div class="p-sm-3 px-lg-4 px-xxl-5 py-lg-5">
              <!-- Sign In Form -->
              <form @submit.prevent="onSubmit">
                <div class="mb-4">
                  <input
                    type="text"
                    class="form-control form-control-alt form-control-lg"
                    id="login-username"
                    name="login-username"
                    placeholder="Email"
                    :class="{
                      'is-invalid': v$.username.$errors.length,
                    }"
                    v-model="state.username"
                    @blur="v$.username.$touch"
                  />
                  <div
                    v-if="v$.username.$errors.length"
                    class="invalid-feedback animated fadeIn"
                  >
                    Email necessário
                  </div>
                </div> 
                <div>
                  <div class="input-group">
                    <input
                      :type="state.showPassword ? 'text' : 'password'"
                      class="form-control form-control-alt form-control-lg"
                      id="login-password"
                      name="login-password"
                      placeholder="Senha"
                      :class="{ 'is-invalid': v$.password.$errors.length }"
                      v-model="state.password"
                      @blur="v$.password.$touch"
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      @click="togglePasswordVisibility"
                    >
                      <i
                        class="fas"
                        :class="{
                          'fa-eye': state.showPassword,
                          'fa-eye-slash': !state.showPassword,
                        }"
                      ></i>
                    </button>
                  </div>
                  <div
                    v-if="v$.password.$errors.length"
                    class="invalid-feedback animated fadeIn"
                  >
                    Senha necessária
                  </div>
                </div>
                <div class="mb-5">
                  <RouterLink
                    :to="{ name: 'auth-reminder' }"
                    class="btn-primary"
                  >
                    Esqueci a senha
                  </RouterLink>
                </div>
                <div class="row mb-5">
                  <div class="">
                    <button
                      class="btn rounded btn-warning green-dark border-0 text-light w-100"
                    >
                      Entrar
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </BaseBlock>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.block.block-rounded {
  border-radius: 0%;
}

.full-btn {
  width: 100%;
  height: 3rem;
}
</style>
