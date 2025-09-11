<script setup></script>

<template>
  <!-- Page Content -->
  <div class="hero">
    <div class="hero-inner text-center">
      <div class="bg-body-extra-light">
        <div class="content content-full overflow-hidden">
          <div class="py-4">
            <!-- Error Header -->
            <h1 class="display-1 fw-bolder text-city">403</h1>
            <h2 class="h4 fw-normal text-muted mb-5">
              Você não tem permissão para acessar esta página.
            </h2>
          </div>
        </div>
      </div>
      <div class="content content-full text-muted fs-sm fw-medium">
        <!-- Error Footer -->
        <RouterLink :to="{ name: 'home' }" class="link-fx"
          >Voltar para o Início</RouterLink
        >
        <!-- END Error Footer -->
      </div>
    </div>
  </div>
  <!-- END Page Content -->
</template>
