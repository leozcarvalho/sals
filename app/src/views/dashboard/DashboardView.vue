<script setup>
import { ref, onMounted } from "vue";
import { userApi } from "../../services/usersApi";
import { useRoute } from "vue-router";
import router from "../../router";

const route = useRoute();
const user = ref(null);
const fetchUser = async () => {
  const res = await userApi.getCurrentUser();
  user.value = res.data;
};

onMounted(async () => {
  await fetchUser();
});

</script>

<template>
  <!-- page -->
  <BaseBackground inner-class="bg-black-50">
    <div class="content content-full text-center">
      <div class="row items-push">
        <div class="col-sm-4">
          <BaseBlock class="d-flex flex-column h-100 mb-0">
            <template #content>
              <div
                class="block-content block-content-full d-flex justify-content-between align-items-center"
              >
                <dl class="mb-0 col-6">
                  <dt class="fs-3 fw-bold">Instalações</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    Ver placas instaladas
                  </dd>
                </dl>
                <div
                  class="item item-rounded-lg bg-body-light"
                >
                  <i class="fa fa-3x fa-microchip text-muted"></i>
                </div>
              </div>
              <div class="bg-body-light rounded-bottom">
                <router-link
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  :to="{ name: 'installations' }"
                >
                  <span>Acessar</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
              </router-link>
              </div>
            </template>
          </BaseBlock>
        </div>

        <div class="col-sm-4">
          <BaseBlock class="d-flex flex-column h-100 mb-0">
            <template #content>
              <div
                class="block-content block-content-full d-flex justify-content-between align-items-center"
              >
                <dl class="mb-0 col-6">
                  <dt class="fs-3 fw-bold">Cozinhas</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    Ver cozinhas cadastradas
                  </dd>
                </dl>
                <div
                  class="item item-rounded-lg bg-body-light"
                >
                  <mdicon name="chef-hat" class="fa-3x text-muted" />
                </div>
              </div>
              <div class="bg-body-light rounded-bottom">
                <router-link
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  :to="{ name: 'kitchens' }"
                >
                  <span>Acessar</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
              </router-link>
              </div>
            </template>
          </BaseBlock>
        </div>

        <div class="col-sm-4">
          <BaseBlock class="d-flex flex-column h-100 mb-0">
            <template #content>
              <div
                class="block-content block-content-full d-flex justify-content-between align-items-center"
              >
                <dl class="mb-0 col-6">
                  <dt class="fs-3 fw-bold">Galpões</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    Ver galpões cadastrados
                  </dd>
                </dl>
                <div
                  class="item item-rounded-lg bg-body-light"
                >
                  <mdicon name="warehouse" class="fa-3x text-muted" />
                </div>
              </div>
              <div class="bg-body-light rounded-bottom">
                <router-link
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  :to="{ name: 'sheds' }"
                >
                  <span>Acessar</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
              </router-link>
              </div>
            </template>
          </BaseBlock>
        </div>
      </div>
    </div>
  </BaseBackground>
</template>
