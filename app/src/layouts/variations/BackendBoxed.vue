<script setup>
import { ref, computed, onMounted } from "vue";
import { useTemplateStore } from "@/stores/template";

import BaseLayout from "@/layouts/BaseLayout.vue";
import BaseNavigation from "@/components/BaseNavigation.vue";

const messages = ref(null);


const userHasOpenedMessagesMenu = ref(false);
const messagesStatusChanged = ref(false);
//const messagesGetter = ref(null);

onMounted(() => {
  // fetchMessages();
  //messagesGetter.value = setInterval(fetchMessages, 60000);
});

// Grab menu navigation arrays
import { baseMenu } from "@/data/menu";

const navigation = ref([...baseMenu]); // cópia

// Main store
const store = useTemplateStore();

// Reactive variables
const mobileNav = ref(false);

// Set default elements for this layout
store.setLayout({
  header: true,
  sidebar: false,
  sideOverlay: false,
  footer: true,
});

// Set various template options for this layout variation
store.headerStyle({ mode: "dark" });
store.mainContent({ mode: "boxed" });

const isMobile = computed(() => {
  return window.innerWidth <= 768;
});
</script>

<style scoped>
.new-notifications {
  scale: 0.85;
}
</style>

<template>
  <BaseLayout>
    <!-- Header Content -->
    <!-- Using the available v-slot, we can override the default Header content from layouts/partials/Header.vue -->
    <template #header-content>
      <!-- Left Section -->
      <div class="d-flex align-items-center">
        <!-- Logo -->
        <!-- Logo -->
        <RouterLink :to="{ name: 'home' }">
          <div class="text-center">
            <img
              v-if="!store.settings.sidebarMini"
              class="logo"
              src="../../assets/img/sals.png"
              style="max-width: 150px"
              alt="logo"
            />
            <img
              v-else
              class="logo"
              src="../../assets/img/sals.png"
              alt="logo"
            />
          </div>
        </RouterLink>

        <!-- END Logo -->
        <div class="content py-3" v-if="!isMobile">
          <!-- Toggle Navigation -->
          <div class="d-lg-none">
            <button
              type="button"
              class="btn w-100 btn-alt-secondary d-flex justify-content-between align-items-center"
              @click="
                () => {
                  mobileNav = !mobileNav;
                }
              "
            >
              Menu
              <i class="fa fa-bars"></i>
            </button>
          </div>
          <!-- END Toggle Navigation -->

          <!-- Navigation -->
          <div
            id="main-navigation"
            class="d-lg-block mt-2 mt-lg-0"
            :class="{
              'd-none': !mobileNav,
            }"
          >
            <BaseNavigation
              :nodes="navigation"
              horizontal
              horizontal-hover
              dark
            />
          </div>
          <!-- END Navigation -->
        </div>
      </div>


      <!-- END Left Section -->
      <div class="dropdown d-inline-block">
        <button
          type="button"
          class="btn btn-alt-secondary align-items-center"
          id="page-header-user-dropdown"
          data-bs-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
        >
          <span class="si si-options"></span>
          <i
            class="fa fa-fw fa-angle-down d-none d-sm-inline-block opacity-50 ms-1 mt-1"
          ></i>
        </button>
        <div
          class="dropdown-menu dropdown-menu-md dropdown-menu-end p-0 border-0"
          aria-labelledby="page-header-user-dropdown"
        >
          <!--
          <div class="p-2">
            <RouterLink
              :to="{ name: 'user-profile' }"
              class="dropdown-item d-flex align-items-center justify-content-between"
            >
              <span class="fs-sm fw-medium">Perfil</span>
              <span class="si si-user d-none d-sm-inline-block"></span>
            </RouterLink>
          </div>
          <div role="separator" class="dropdown-divider m-0"></div>
          -->
          <div class="p-2">
            <RouterLink
              :to="{ name: 'auth-signin' }"
              class="dropdown-item d-flex align-items-center justify-content-between"
            >
              <span class="fs-sm fw-medium">Sair</span>
              <span class="si si-power d-none d-sm-inline-block"></span>
            </RouterLink>
          </div>
        </div>
      </div>
      <!-- END User Dropdown -->

      <!-- END Right Section -->
    </template>
    <!-- END Header Content -->

    <!-- Page Top Content -->
    <!-- Using the available v-slot, we can override the default Page Top Content from layouts/BaseLayout.vue -->
    <template #page-top-content v-if="isMobile">
      <div>
        <div>
          <div class="content py-3">
            <!-- Toggle Navigation -->
            <div class="d-lg-none">
              <button
                type="button"
                class="btn w-100 btn-alt-secondary d-flex justify-content-between align-items-center"
                @click="
                  () => {
                    mobileNav = !mobileNav;
                  }
                "
              >
                Menu
                <i class="fa fa-bars"></i>
              </button>
            </div>
            <!-- END Toggle Navigation -->

            <!-- Navigation -->
            <div
              id="main-navigation"
              class="d-lg-block mt-2 mt-lg-0"
              :class="{
                'd-none': !mobileNav,
              }"
            >
              <BaseNavigation
                :nodes="navigation"
                horizontal
                horizontal-hover
                dark
              />
            </div>
            <!-- END Navigation -->
          </div>
        </div>
      </div>
    </template>
    <!-- END Page Top Content -->
  </BaseLayout>
</template>
