import { createRouter, createWebHistory } from "vue-router";
import { isLoggedIn, loggout } from "@/helpers/userSession";

import NProgress from "nprogress/nprogress.js";

import LayoutSimple from "@/layouts/variations/Simple.vue";
import LayoutBackendBoxed from "@/layouts/variations/BackendBoxed.vue";

const BackendDashboard = () => import("@/views/dashboard/DashboardView.vue");

const UserList = () => import("@/pages/users/UsersList.vue");
const UserForm = () => import("@/pages/users/UserForm.vue");
const UserProfile = () => import("@/pages/users/UserProfile.vue");

// Auth
const AuthSignIn = () => import("@/views/auth/SignInView.vue");
const AuthReminder = () => import("@/views/auth/ReminderView.vue");
const AuthCreatePassword = () => import("@/views/auth/CreatePasswordView.vue");

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


const Instalations = () => import("@/pages/instalations/Instalations.vue");
const Instalation = () => import("@/pages/instalations/Instalation.vue");
const InstalationPinsConfig = () => import("@/pages/instalations/InstalationPinsConfig.vue");

const Kitchens = () => import("@/pages/kitchens/Kitchens.vue");
const Sheds = () => import("@/pages/sheds/ShedsList.vue");
const Shed = () => import("@/pages/sheds/Shed.vue");

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
        path: "kitchens",
        name: "kitchens",
        meta: { requiresAuth: true },
        component: Kitchens,
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
      }
    ],
  },
  {
    path: "/management",
    component: LayoutBackendBoxed,
    children: [
      {
        path: "user-management",
        name: "user-management",
        meta: { requiresAuth: true },
        component: UserList,
      },
      {
        path: "user-edit",
        name: "user-form",
        meta: { requiresAuth: true },
        component: UserForm,
      },
      {
        path: "user-profile",
        name: "user-profile",
        meta: { requiresAuth: true },

        component: UserProfile,
      },
      {
        path: "user-management",
        name: "users-list",
        meta: { requiresAuth: true },
        component: UserList,
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
        name: "instalations",
        path: "/instalacoes",
        meta: { requiresAuth: true },
        component: Instalations,
      },
      {
        name: "instalation",
        path: "/instalacao",
        meta: { requiresAuth: true },
        component: Instalation,
      },
      {
        name: "instalation-pin-config",
        path: "/instalacao/pinos",
        meta: { requiresAuth: true },
        component: InstalationPinsConfig,
      }
    ]
  },


  /*
  |
  |--------------------------------------------------------------------------
  | Auth Routes
  |--------------------------------------------------------------------------
  |
  */
  {
    path: "/auth",
    component: LayoutSimple,
    children: [
      {
        path: "reminder",
        name: "auth-reminder",
        meta: { requiresAuth: false },
        component: AuthReminder,
      },
      {
        path: "create-password",
        name: "auth-create-password",
        component: AuthCreatePassword,
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

router.beforeResolve(async (to, from, next) => {
  NProgress.start();
  if (to.meta.requiresAuth && !isLoggedIn()) {
    next({
      path: "auth-signin",
    });
  } else if (from.meta.requiresAuth && to.name === 'auth-signin') {
    loggout()
    next();
  }
  next();
});

router.afterEach((to, from) => {
  NProgress.done();
});
/*eslint-enable no-unused-vars*/

export default router;
