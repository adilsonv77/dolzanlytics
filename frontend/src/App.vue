<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>
<template>
  <nav class="rounded">
    <a href="/" class="logo"><img src="/favicon.ico" alt="Logo" style="width: 35px;"></a>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/cadastro">Cadastro</RouterLink>
    <RouterLink to="/dashboard">Dashboard</RouterLink>
    <RouterLink to="/saved">Salvos</RouterLink>
    <RouterLink to="/about">Sobre</RouterLink>
  </nav>
  <RouterView />
</template>
<style scoped></style>
