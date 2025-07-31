<script setup lang="ts">
import { Brain, ChartColumn, CircleCheckBig, Flame } from 'lucide-vue-next'
import { reactive, ref, type Ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import {
  type AnalysisData,
  type GameData,
  type RoastingUserData,
  type FileUploadData,
} from '@/types'
import StatusCardWithGamesAnalysis from '@/components/StatusCardWithGamesAnalysis.vue'
import StatusCardWithRoast from '@/components/StatusCardWithRoast.vue'
import StatusCardWithBasicInformation from '@/components/StatusCardWithBasicInformation.vue'

const route = useRoute()
const ui = useUIStore()
const defaultSummaryCls: Ref<string> = ref('flex items-center gap-2 p-3 rounded-lg')
const categoryPresentCls: Ref<string> = ref('bg-green-100 text-green-700')
const defaultIconCls: Ref<string> = ref('h-4 w-4')

const analysisData = reactive<AnalysisData>({
  result: null,
})
const fileUploadData: Ref<FileUploadData | null> = ref(null)
const gameData: Ref<GameData | null> = ref(null)
const roastData: Ref<RoastingUserData | null> = ref(null)
const chessStyleData: Ref<object | null> = ref(null)
const progressBarData: Ref<number> = ref(0)
watch(analysisData, (_newData, _oldData) => {
  progressBarData.value = (Object.keys(analysisData.result).length * 100) / 4
})

getAnalysisData()

async function getAnalysisData() {
  try {
    const response = await fetch(`/server/analysis/status/${route.params.statusId}`)
    const data = await response.json()
    if (!response.ok) {
      ui.showMessage('error', 'Error', data.detail)
    } else {
      analysisData.result = data.result
      fileUploadData.value = analysisData.result?.file_upload
      gameData.value = analysisData.result?.game
      roastData.value = analysisData.result?.roasting_user
      chessStyleData.value = analysisData.result?.chess_style
    }
  } catch (error) {
    ui.showMessage('error', 'Error', error)
  }
}
</script>
<template>
  <Toast />
  <div v-if="analysisData.result" class="grid grid-cols-1 gap-6 w-2/3 mx-auto">
    <Card class="w-full">
      <template #title>
        <div class="flex items-center gap-2">
          <ChartColumn />
          <p class="font-[1000] text-2xl text-black">Analysis Progress</p>
        </div>
      </template>
      <template #subtitle>
        Tracking ID:
        <span class="font-mono font-extrbold text-black">{{ route.params.statusId }}</span>
      </template>
      <template #content>
        <div class="grid grid-cols-1 gap-3">
          <progress-bar :value="progressBarData" class="w-full"></progress-bar>
          <div class="grid grid-cols-4 gap-4">
            <div class="">
              <div :class="[fileUploadData ? categoryPresentCls : '', defaultSummaryCls]">
                <CircleCheckBig :class="[fileUploadData ? 'text-green-600' : '', defaultIconCls]" />
                <span class="text-sm font-medium">
                  {{ fileUploadData ? 'Games Found' : 'Loading games..' }}
                </span>
              </div>
            </div>
            <div class="">
              <div :class="[gameData ? categoryPresentCls : '', defaultSummaryCls]">
                <ChartColumn :class="[gameData ? 'text-green-600' : '', defaultIconCls]" />
                <span class="text-sm font-medium">
                  {{ gameData ? 'Stats Analyzed' : 'Analysing Games...' }}</span
                >
              </div>
            </div>
            <div v-if="roastData" class="">
              <div :class="[roastData ? categoryPresentCls : '', defaultSummaryCls]">
                <Flame class="h-4 w-4 text-red-500" />
                <span class="text-sm font-medium">{{
                  roastData ? 'User Roasted' : 'Roasting in progress...'
                }}</span>
              </div>
            </div>
            <div class="">
              <div :class="[chessStyleData ? categoryPresentCls : '', defaultSummaryCls]">
                <Brain :class="[chessStyleData ? 'text-green-600' : '', defaultIconCls]" />
                <span class="text-sm font-medium">{{
                  chessStyleData ? 'Styles Analyzed' : 'Analyzing playing styles'
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Card>
    <StatusCardWithBasicInformation v-if="fileUploadData" :informationObject="fileUploadData" />
    <StatusCardWithGamesAnalysis v-if="gameData" :gameObjects="gameData" />
    <StatusCardWithRoast v-if="roastData" :roastObjects="roastData" />
  </div>
  <div v-else class="grid grid-cols-1 gap-6 w-2/3 mx-auto">
    <Skeleton class="mb-2" borderRadius="16px"></Skeleton>
    <Skeleton class="mb-2" borderRadius="16px"></Skeleton>
    <Skeleton width="5rem" borderRadius="16px" class="mb-2"></Skeleton>
    <Skeleton height="2rem" class="mb-2" borderRadius="16px"></Skeleton>
    <Skeleton width="10rem" height="4rem" borderRadius="16px"></Skeleton>
  </div>
</template>
