<script setup lang="ts">
import { type FileUploadData } from '@/types'
const props = defineProps<{
  informationObject: FileUploadData
}>()
const sources = ['Chess.com', 'Lichess', 'PGN file']
const source = sources[props.informationObject.source - 1]
</script>
<template>
  <div>
    <Card>
      <template #title>Basic Information</template>
      <template #content>
        <div class="grid grid-cols-2 gap-7">
          <div class="text-center p-4 bg-muted rounded-lg">
            <div class="text-xl font-black text-black">
              {{ props.informationObject.usernames }}
            </div>
            <div class="text-sm text-muted-foreground">Username</div>
          </div>
          <div class="text-center p-4 bg-muted rounded-lg">
            <div class="text-xl font-black text-black">
              {{ source }}
            </div>
            <div class="text-sm text-muted-foreground">Source</div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>
