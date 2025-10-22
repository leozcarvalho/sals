import { createRouter, createWebHistory } from "vue-router";
import { loadUserFromCookie } from "@/helpers/userSession";
import { useUserStore } from "@/stores/userStore";

import NProgress from "nprogress/nprogress.js";

import LayoutSimple from "@/layouts/variations/Simple.vue";
import LayoutBackendBoxed from "@/layouts/variations/BackendBoxed.vue";
import { path } from "d3";

const BackendDashboard = () => import("@/views/dashboard/DashboardView.vue");

const Users = () => import("@/pages/users/Users.vue");

// Auth
const AuthSignIn = () => import("@/views/auth/SignInView.vue");

// Errors
const Error400 = () => import("@/views/errors/400View.vue");
const Error401 = () => import("@/views/errors/401View.vue");
const Error403 = () => import("@/views/errors/403View.vue");
const Error404 = () => import("@/views/errors/404View.vue");
const Error500 = () => import("@/views/errors/500View.vue");
const Error503 = () => import("@/views/errors/503View.vue");

//Hardware
const HardwarePointTypes = () => import("@/pages/hardware-point-types/HardwarePointTypes.vue");
const HardwareKinds = () => import("@/pages/hardware-kinds/HardwareKinds.vue");
const HardwareConnectionTemplates = () => import("@/pages/hardware-connection-templates/HardwareConnectionTemplates.vue");
const HardwareDevices = () => import("@/pages/hardware-device/HardwareDevice.vue");


const Installations = () => import("@/pages/installations/Installations.vue");
const Installation = () => import("@/pages/installations/Installation.vue");
const SettingsRoutines = () => import("@/pages/settings/Routines.vue");

const Profiles = () => import("@/pages/profiles/Profiles.vue");

const Kitchens = () => import("@/pages/kitchens/Kitchens.vue");
const KitchenForm = () => import("@/pages/kitchens/KitchenForm.vue");

const Sheds = () => import("@/pages/sheds/ShedsList.vue");
const Shed = () => import("@/pages/sheds/Shed.vue");

const Products = () => import("@/pages/products/Products.vue");
const ProductTanks = () => import("@/pages/product-tanks/ProductTanks.vue");

const Formulas = () => import("@/pages/formulas/Formulas.vue");
const FormulaForm = () => import("@/pages/formulas/FormulaForm.vue");

const FeedingCurves = () => import("@/pages/feeding-curves/FeedingCurves.vue");
const FeedingCurveForm = () => import("@/pages/feeding-curves/FeedingCurveForm.vue");

const SvgList = () => import("@/pages/svgs/SvgList.vue");
const SvgConfig = () => import("@/pages/svgs/SvgConfig.vue");

// Set all routes
const routes = [
  {
    path: "/",
    component: LayoutSimple,
    children: [
      {
        path: "",
        name: "auth-signin",
        component: AuthSignIn,
        meta: { requiresAuth: false },
      },
      {
        path: "/login",
        name: "auth-login",
        component: AuthSignIn,
        meta: { requiresAuth: false },
      },
    ],
  },

  {
    path: "/pages",
    component: LayoutBackendBoxed,
    children: [
      {
        path: "home-page",
        name: "home",
        meta: { requiresAuth: true },
        component: BackendDashboard,
      },
      {
        path: "users",
        name: "users",
        meta: { requiresAuth: true },
        component: Users,
      },
      {
        path: "profiles",
        name: "profiles",
        meta: { requiresAuth: true },
        component: Profiles,
      },
      {
        path: "svgs",
        name: "svgs",
        meta: { requiresAuth: true },
        component: SvgList,
      },
      {
        path: "svg-config/:id?",
        name: "svg-config",
        meta: { requiresAuth: true },
        component: SvgConfig,
      },
      {
        path: "kitchens",
        name: "kitchens",
        meta: { requiresAuth: true },
        component: Kitchens,
      },
      {
        path: "kitchen-form/:id?",
        name: "kitchen-form",
        meta: { requiresAuth: true },
        component: KitchenForm,
      },
      {
        path: "sheds",
        name: "sheds",
        meta: { requiresAuth: true },
        component: Sheds,
      },
      {
        path: "shed",
        name: "shed",
        meta: { requiresAuth: true },
        component: Shed,
      },
      {
        path: "products",
        name: "products",
        meta: { requiresAuth: true },
        component: Products,
      },
      {
        path: "product-tanks",
        name: "product-tanks",
        meta: { requiresAuth: true },
        component: ProductTanks,
      },
      {
        path: "formulas",
        name: "formulas",
        meta: { requiresAuth: true },
        component: Formulas,
      },
      {
        path: "formula-form/:id?",
        name: "formula-form",
        meta: { requiresAuth: true },
        component: FormulaForm,
      },
      {
        path: "feeding-curves",
        name: "feeding-curves",
        meta: { requiresAuth: true },
        component: FeedingCurves,
      },
      {
        path: "feeding-curve-form/:id?",
        name: "feeding-curve-form",
        meta: { requiresAuth: true },
        component: FeedingCurveForm,
      },
    ],
  },

  {
    path: "/hardware",
    component: LayoutBackendBoxed,
    children: [
      {
        name: "hardware-devices",
        path: "/dispositivos",
        meta: { requiresAuth: true },
        component: HardwareDevices,
      },
      {
        name: "hardware-connections",
        path: "/conexoes",
        meta: { requiresAuth: true },
        component: HardwareConnectionTemplates,
      },
      {
        name: "hardware-point-types",
        path: "/pontos",
        meta: { requiresAuth: true },
        component: HardwarePointTypes,
      },
      {
        name: "hardware-kinds",
        path: "/tipos",
        meta: { requiresAuth: true },
        component: HardwareKinds,
      },
      {
        name: "installations",
        path: "/installations",
        meta: { requiresAuth: true },
        component: Installations,
      },
      {
        name: "installation",
        path: "/installation",
        meta: { requiresAuth: true },
        component: Installation,
      },
    ]
  },
  {
    path: "/settings",
    component: LayoutBackendBoxed,
    children: [
      {
        path: "/routines",
        name: "settings-routines",
        meta: { requiresAuth: true },
        component: SettingsRoutines,
      },
    ],
  },

  /*
  |
  |--------------------------------------------------------------------------
  | Error Routes
  |--------------------------------------------------------------------------
  |
  */
  {
    path: "/errors",
    component: LayoutSimple,
    children: [
      {
        path: "400",
        name: "error-400",
        component: Error400,
      },
      {
        path: "401",
        name: "error-401",
        component: Error401,
      },
      {
        path: "403",
        name: "error-403",
        component: Error403,
      },
      {
        path: "404",
        name: "error-404",
        component: Error404,
      },
      {
        path: "500",
        name: "error-500",
        component: Error500,
      },
      {
        path: "503",
        name: "error-503",
        component: Error503,
      },
    ],
  },
];

// Create Router
const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: "active",
  linkExactActiveClass: "active",
  scrollBehavior() {
    return { left: 0, top: 0 };
  },
  routes,
});

// NProgress
/*eslint-disable no-unused-vars*/
NProgress.configure({ showSpinner: false });

router.beforeResolve((to, from, next) => {
  NProgress.start();
  const userStore = useUserStore();
  if (!userStore.id) {
    loadUserFromCookie();
  }
  if (to.meta.requiresAuth && !userStore.id) {
    return next({ path: "/auth-signin" });
  }
  if (from.meta.requiresAuth && to.name === "auth-signin") {
    userStore.logout();
  }
  next();
});



router.afterEach((to, from) => {
  NProgress.done();
});
/*eslint-enable no-unused-vars*/

export default router;
