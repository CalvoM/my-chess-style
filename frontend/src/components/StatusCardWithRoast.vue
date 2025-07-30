<script setup lang="ts">
import { type RoastingUserData } from '@/types'
const props = defineProps<{
  roastData: RoastingUserData
}>()
</script>
<template>
  <div>
    <Card>
      <template #title>
        <p class="text-red-600 font-black">AI Roast & Commentary 🔥</p>
      </template>
      <template #subtitle> Brutally honest analysis with a side of encouragement</template>
      <template #content>
        <div class="grid grid-cols-1 gap-6">
          <div class="p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
            <h4 class="font-semibold text-red-800 mb-2">The Roast</h4>
            <p class="text-red-700 whitespace-pre-line">{{ props.roastData.roast }}</p>
          </div>

          <div class="p-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg">
            <h4 class="font-semibold text-blue-800 mb-2">Encouragement</h4>
            <p class="text-blue-700 whitespace-pre-line">
              {{ props.roastData.encouragement }}
            </p>
          </div>

          <div class="p-4 bg-green-50 border-l-4 border-green-500 rounded-lg">
            <h4 class="font-semibold text-green-800 mb-3">Tips for Improvement</h4>
            <p class="text-green-600 whitespace-pre-line">
              {{ props.roastData.tip }}
            </p>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>
