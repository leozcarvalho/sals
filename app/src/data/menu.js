// src/config/menus.js
export const baseMenu = [
  {
    name: "Início",
    to: "home",
    icon: "si si-speedometer",
  },
  {
    name: "Instalações",
    to: "account-devices",
    icon: "home-variant",
    action: "view-cams",
  },
  {
    name: "Cadastros",
    to: "users-list",
    icon: "format-list-checkbox",
    action: "manage-cruds",
    sub: [
      { name: "Usuários", to: "users-list", icon: "account-group", action: "manage-cruds" },
      { name: "Cozinhas", to: "kitchens", icon: "chef-hat", action: "manage-cruds" },
      { name: "Galpões", to: "sheds", icon: "pig-variant", action: "manage-cruds" },
    ],
  },
  {
    name: "Hardware",
    icon: "devices",
    sub: [
      { name: "Placas", to: "hardware-devices", icon: "access-point" },
      { name: "Conexões", to: "hardware-connections", icon: "ethernet" },
      { name: "Pontos", to: "hardware-point-types", icon: "lightbulb" },
      { name: "Tipos de Hardware", to: "hardware-kinds", icon: "tools" },
    ]
  }
];
