
const hasPermission = (el, binding) => {
  const permission = binding.value;
  const userPermissions = JSON.parse(localStorage.getItem('permissions'));
  if (!userPermissions[permission]) {
    el.style.display = 'none';
  }
};

export const permissionDirective = {
  mounted: hasPermission,
  updated: hasPermission,
};