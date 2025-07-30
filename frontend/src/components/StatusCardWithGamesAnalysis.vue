<script setup lang="ts">
import { type GameData } from '@/types'
const props = defineProps<{
  gameObjects: GameData
}>()
</script>
<template>
  <div>
    <Card>
      <template #title>Preliminary Game Analysis</template>
      <template #content>
        <div class="grid grid-cols-1 gap-4">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="text-center p-4 bg-muted rounded-lg">
              <div class="text-2xl font-black text-muted-foreground">
                {{ props.gameObjects.count }}
              </div>
              <div class="text-sm text-muted-foreground">Total Games</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl text-primary font-[900]">
                {{ ((props.gameObjects.win_count * 100) / props.gameObjects.count).toFixed(1) }}%
              </div>
              <div class="text-sm text-muted-foreground">
                Win Rate ({{ props.gameObjects.win_count }} games)
              </div>
            </div>
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-extrabold text-blue-800">
                {{ ((props.gameObjects.draw_count * 100) / props.gameObjects.count).toFixed(1) }}%
              </div>
              <div class="text-sm text-muted-foreground">
                Draw Rate ({{ props.gameObjects.draw_count }} games)
              </div>
            </div>
            <div class="text-center p-4 bg-red-50 rounded-lg">
              <div class="text-2xl font-bold text-red-600">
                {{ ((props.gameObjects.loss_count * 100) / props.gameObjects.count).toFixed(1) }}%
              </div>
              <div class="text-sm text-muted-foreground">
                Loss Rate ({{ props.gameObjects.loss_count }} games)
              </div>
            </div>
          </div>
          <div class="mt-4">
            <h4 class="font-black text-xl my-8">Average Opponent Rating by Time Control</h4>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div class="text-center p-4 bg-muted rounded-lg">
                <div class="text-xl font-black text-black">
                  {{ props.gameObjects.opponents_avg_rating.bullet.toFixed(1) }}
                </div>
                <div class="text-sm text-muted-foreground">Bullet</div>
              </div>
              <div class="text-center p-4 bg-muted rounded-lg">
                <div class="text-xl font-black text-black">
                  {{ props.gameObjects.opponents_avg_rating.blitz.toFixed(1) }}
                </div>
                <div class="text-sm text-muted-foreground">Blitz</div>
              </div>
              <div class="text-center p-4 bg-muted rounded-lg">
                <div class="text-xl font-black text-black">
                  {{ props.gameObjects.opponents_avg_rating.rapid.toFixed(1) }}
                </div>
                <div class="text-sm text-muted-foreground">Rapid</div>
              </div>
              <div class="text-center p-4 bg-muted rounded-lg">
                <div class="text-xl font-black text-black">
                  {{ props.gameObjects.opponents_avg_rating.classical.toFixed(1) }}
                </div>
                <div class="text-sm text-muted-foreground">Classical</div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>
