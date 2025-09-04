<script setup>
import { reactive, computed, onMounted, ref } from "vue";
import { userApi } from "../../services/usersApi";
import { vMaska } from "maska";
import { useRouter, useRoute } from "vue-router";
import { toastApi } from "../../components/toast";
import useVuelidate from "@vuelidate/core";
import { required, minLength, email } from "@vuelidate/validators";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/css/index.css";

const loading = ref(false);
const loaderOn = () => (loading.value = true);
const loaderOff = () => (loading.value = false);

const router = useRouter();

const rules = computed(() => {
  return {
    phone_number: {
      minLength: minLength(15),
    },
  };
});

const user = reactive({});

onMounted(async () => {
  refresh();
});

const refresh = async () => {
  loaderOn();
  const res = await userApi.getCurrentUser();
  Object.assign(user, res.data);
  loaderOff();
};

const v$ = useVuelidate(rules, user);

const submit = async () => {
  loaderOn();
  const result = await v$.value.$validate();
  if (result) {
    user.logo_colors = JSON.stringify(user.logo_colors_json);
    const res = await userApi.updateUser(user.id, user);
    toastApi(res.data.status, res.data.detail);
    if (res.data.status === "success") refresh();
  }
  loaderOff();
};

const onHover = ref(false);



</script>

<style scoped>
.image {
  position: relative;
}

.center-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.gray {
  opacity: 50%;
  cursor: pointer;
}

.accordion-item {
  background-color: white;
}
</style>

<template>
  <div class="content">
    <Loading :active="loading" />
    <div class="row">
      <div class="col-md-12">
        <form @submit.prevent>
          <BaseBlock v-if="user" :title="'Perfil'">
            <div class="row justify-content-center py-sm-3 py-md-5">
              
              <div class="accordion" id="accordionExample">
                <div class="accordion-item">
                  <h2 class="accordion-header" id="headingOne">
                    <button
                      class="accordion-button"
                      type="button"
                      data-bs-toggle="collapse"
                      data-bs-target="#collapseOne"
                      aria-expanded="true"
                      aria-controls="collapseOne"
                    >
                      Informações
                    </button>
                  </h2>
                  <div
                    id="collapseOne"
                    class="accordion-collapse collapse show"
                    aria-labelledby="headingOne"
                    data-bs-parent="#accordionExample"
                  >
                    <div class="accordion-body">
                      <div class="mt-3">
                        <label class="form-label">Nome</label>
                        <div class="input-group">
                          <button
                            type="button"
                            class="btn btn-alt-primary"
                            disabled
                          >
                            <mdicon name="account"></mdicon>
                          </button>
                          <input
                            v-model="user.name"
                            type="text"
                            class="form-control form-control-alt"
                            disabled
                          />
                        </div>
                      </div>
                      <div class="mt-3">
                        <label class="form-label">Email *</label>
                        <div class="input-group">
                          <button
                            type="button"
                            class="btn btn-alt-primary"
                            disabled
                          >
                            <mdicon name="mail"></mdicon>
                          </button>
                          <input
                            v-model="user.email"
                            type="text"
                            class="form-control form-control-alt"
                            disabled
                          />
                        </div>
                      </div>
                      <div class="mt-3">
                        <label class="form-label">Celular</label>
                        <div class="input-group">
                          <button
                            type="button"
                            class="btn btn-alt-primary"
                            disabled
                          >
                            <mdicon name="phone"></mdicon>
                          </button>
                          <input
                            v-model="user.phone_number"
                            v-maska
                            data-maska="(##) #####-####"
                            type="text"
                            class="form-control"
                            :class="{
                              'is-invalid': v$.phone_number.$errors.length,
                            }"
                            @blur="v$.phone_number.$touch"
                          />
                          <div
                            v-if="v$.phone_number.$errors.length"
                            class="invalid-feedback animated fadeIn"
                          >
                            Telefone é inválido
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="my-3">
                <button
                  class="btn btn-lg btn-alt-success float-end"
                  @click="submit"
                >
                  Salvar
                </button>
              </div>
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
</style>
