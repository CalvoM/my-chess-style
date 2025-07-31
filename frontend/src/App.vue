<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <header>
    <div class="min-h-screen bg-background p-6">
      <div class="mx-auto flex flex-col gap-8 items-center">
        <div class="text-center flex flex-col gap-4">
          <router-link to="/">
            <h1 class="text-4xl font-bold text-foreground hover:underline hover:decoration-sky-400">
              My Chess Style
            </h1></router-link
          >
          <p class="text-xl text-muted-foreground">
            Analyze your chess games and discover your playing style
          </p>
        </div>
        <RouterView />
      </div>
    </div>
  </header>
</template>

<style scoped></style>
