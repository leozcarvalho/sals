<script setup>
import { ref, onMounted } from "vue";
import { userApi } from "../../services/usersApi";
import { useRoute } from "vue-router";

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
  <!-- modal -->
  <div
    class="modal fade"
    id="modal-quantidade"
    tabindex="-1"
    role="dialog"
    aria-labelledby="modal-quantidade"
    aria-hidden="true"
  >
    <div
      class="modal-dialog modal-dialog-centered modal-dialog-popin"
      role="document"
    >
      <div class="modal-content">
        <BaseBlock title="Quantidade de Animais" transparent class="mb-0">
          <template #options>
            <button
              type="button"
              class="btn btn-info me-1"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <i class="fa fa-fw fa-print"></i>
            </button>
            <button
              type="button"
              class="btn btn-danger me-1"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <i class="fa fa-fw fa-times"></i>
            </button>
          </template>

          <template #content>
            <div class="block-content">
              <div class="col-xl-12">
                <table class="table table-striped table-vcenter">
                  <caption></caption>
                  <tbody>
                    <tr>
                      <th class="text-center" scope="row">
                        Baia 1 de G2 está com 16 suínos
                      </th>
                      <td class="text-center">
                        <div class="btn-group">
                          <button
                            type="button"
                            class="btn btn-sm btn-alt-secondary"
                          >
                            <i class="fa fa-fw fa-times"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <th class="text-center" scope="row">
                        Baia 7 de G1 está com 11 suínos
                      </th>
                      <td class="text-center">
                        <div class="btn-group">
                          <button
                            type="button"
                            class="btn btn-sm btn-alt-secondary"
                          >
                            <i class="fa fa-fw fa-times"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </template>
        </BaseBlock>
      </div>
    </div>
  </div>

  <!-- page -->
  <BaseBackground inner-class="bg-black-50">
    <div class="content content-full text-center">
      <div class="row items-push">
        <div
          class="col-sm-4"
          data-bs-target="#modal-quantidade"
          data-bs-toggle="modal"
        >
          <BaseBlock class="d-flex flex-column h-100 mb-0">
            <template #content>
              <div
                class="block-content block-content-full d-flex justify-content-between align-items-center"
              >
                <dl class="mb-0 col-6">
                  <dt class="fs-3 fw-bold">Quantidade</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    de Animais
                  </dd>
                </dl>
                <div
                  class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-danger bg-danger-light"
                >
                  2.3%
                </div>
                <img
                  class="item item-rounded-lg bg-body-light"
                  src="@/assets/img/quantidade-de-animais.png"
                  alt="logo"
                />
              </div>
              <div class="bg-body-light rounded-bottom">
                <a
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  href="javascript:void(0)"
                >
                  <span>2 baias com 19 suínos ou menos</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
                </a>
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
                  <dt class="fs-3 fw-bold">Cocho</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    Vazio
                  </dd>
                </dl>
                <div
                  class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-danger bg-danger-light"
                >
                  2.3%
                </div>
                <img
                  class="item item-rounded-lg bg-body-light"
                  src="@/assets/img/cocho-vazio.png"
                  alt="logo"
                />
              </div>
              <div class="bg-body-light rounded-bottom">
                <a
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  href="javascript:void(0)"
                >
                  <span>2 cochos vazios</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
                </a>
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
                  <dt class="fs-3 fw-bold">Baia</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    Suja
                  </dd>
                </dl>
                <div
                  class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-warning bg-warning-light"
                >
                  2.3%
                </div>
                <img
                  class="item item-rounded-lg bg-body-light"
                  src="@/assets/img/baia-suja.png"
                  alt="logo"
                />
              </div>
              <div class="bg-body-light rounded-bottom">
                <a
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  href="javascript:void(0)"
                >
                  <span>2 baias sujas</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
                </a>
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
                  <dt class="fs-3 fw-bold">Variação</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    de Tamanho do Animal
                  </dd>
                </dl>
                <div
                  class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-danger bg-danger-light"
                >
                  10%
                </div>
                <img
                  class="item item-rounded-lg bg-body-light"
                  src="@/assets/img/variação-de-tamanho-de-animais.png"
                  alt="logo"
                />
              </div>
              <div class="bg-body-light rounded-bottom">
                <a
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  href="javascript:void(0)"
                >
                  <span>9 baias com mais de 60% de variação</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
                </a>
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
                  <dt class="fs-3 fw-bold">Frequência</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    de Rodedores
                  </dd>
                </dl>
                <div
                  class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-success bg-success-light"
                >
                  0%
                </div>
                <img
                  class="item item-rounded-lg bg-body-light"
                  src="@/assets/img/frequência-de-roedores.png"
                  alt="logo"
                />
              </div>
              <div class="bg-body-light rounded-bottom">
                <a
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  href="javascript:void(0)"
                >
                  <span>0 baias com mais de 2 roedores na semana</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
                </a>
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
                  <dt class="fs-3 fw-bold">Movimentação</dt>
                  <dd class="fs-sm fw-medium fs-sm fw-medium text-muted mb-0">
                    de Animais
                  </dd>
                </dl>
                <div
                  class="d-inline-block px-2 py-1 rounded-3 fs-xs fw-semibold text-success bg-success-light"
                >
                  <i class="fa fa-caret me-1"></i>
                  0%
                </div>
                <img
                  class="item item-rounded-lg bg-body-light"
                  src="@/assets/img/movimentação-de-animais.png"
                  alt="logo"
                />
              </div>
              <div class="bg-body-light rounded-bottom">
                <a
                  class="block-content block-content-full block-content-sm fs-sm fw-medium d-flex align-items-center justify-content-between"
                  href="javascript:void(0)"
                >
                  <span>7 baias com mais de 60% de movimentação</span>
                  <i
                    class="fa fa-arrow-alt-circle-right ms-1 opacity-25 fs-base"
                  ></i>
                </a>
              </div>
            </template>
          </BaseBlock>
        </div>
      </div>
    </div>
  </BaseBackground>
</template>
