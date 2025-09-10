// src/config/menus.js
export const baseMenu = [
  {
    name: "Início",
    to: "home",
    icon: "si si-speedometer",
  },
  {
    name: "Instalações",
    to: "installations",
    icon: "fa fa-microchip",
  },
  {
    name: "Cadastros",
    icon: "format-list-checkbox",
    sub: [
      { name: "Usuários", to: "users", icon: "account-group", action: "manage_user" },
      { name: "Perfis", to: "profiles", icon: "account", action: "manage_profile" },
      { name: "Cozinhas", to: "kitchens", icon: "chef-hat", action: "manage_kitchen" },
      { name: "Galpões", to: "sheds", icon: "warehouse", action: "manage_shed" },
    ],
  },
  {
    name: "Hardware",
    icon: "devices",
    sub: [
      { name: "Placas", to: "hardware-devices", icon: "access-point", action: "manage_hardware_device" },
      { name: "Conexões", to: "hardware-connections", icon: "ethernet", action: "manage_hardware_connection_template" },
      { name: "Pontos", to: "hardware-point-types", icon: "lightbulb", action: "manage_hardware_point_type" },
      { name: "Tipos de Hardware", to: "hardware-kinds", icon: "tools", action: "manage_hardware_kind" },
    ]
  }
];
