<script setup lang="ts">
import { type GameData } from '@/types'
const props = defineProps<{
  gameObjects: GameData
}>()
</script>
<template>
  <div>
    <Card v-if="gameObjects.count">
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
          <div class="mt-4">
            <h4 class="font-black text-xl my-8">Top Openings</h4>
            <div class="flex flex-col gap-3">
              <div
                v-for="([opening, data], idx) in props.gameObjects.openings"
                :key="idx"
                class="flex items-center justify-between p-3 bg-muted rounded-lg"
              >
                <div class="flex-1">
                  <div class="font-medium text-sm">{{ opening }}</div>
                  <div class="text-xs text-muted-foreground">
                    ECO: {{ data.eco_codes.join(', ') }}
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-lg font-bold text-primary">{{ data.total }}</div>
                  <div class="text-xs text-muted-foreground">games</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>
    <Card v-else>
      <template #title>Preliminary Game Analysis</template>
      <template #content>
        <div class="grid grid-cols-1 gap-4">
          <h2 class="text-primary">No games played by user</h2>
        </div>
      </template>
    </Card>
  </div>
</template>
