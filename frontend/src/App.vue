<script setup lang="ts">
import { RouterView } from 'vue-router'

</script>

<template>
  <header>
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto flex flex-col gap-8">
        <div className="text-center flex flex-col gap-4">
          <h1 className="text-4xl font-bold text-foreground">My Chess Style</h1>
          <p className="text-xl text-muted-foreground">
            Analyze your chess games and discover your playing style
          </p>
        </div>
  <RouterView />
      </div>
    </div>
  </header>

</template>

<style scoped>
</style>
