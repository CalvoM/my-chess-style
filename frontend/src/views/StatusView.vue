<script setup lang="ts">
import { Brain, ChartColumn, CircleCheckBig, Flame } from 'lucide-vue-next'
import { reactive, ref, type Ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import { useFetch } from '@vueuse/core'
import { type AnalysisData, type GameData, type RoastingUserData } from '@/types'
import StatusCardWithGamesAnalysis from '@/components/StatusCardWithGamesAnalysis.vue'
import StatusCardWithRoast from '@/components/StatusCardWithRoast.vue'

const route = useRoute()
const ui = useUIStore()
const analysisData: Ref<AnalysisData> = reactive({})
const defaultSummaryCls: Ref<string> = ref('flex items-center gap-2 p-3 rounded-lg')
const categoryPresentCls: Ref<string> = ref('bg-green-100 text-green-700')
const defaultIconCls: Ref<string> = ref('h-4 w-4')
const fileUploadData: Ref<string> = ref('')
const gameData: Ref<GameData> = ref({})
const roastData: Ref<RoastingUserData> = ref({})
const chessStyleData: Ref<Object> = ref({})
const progressBarData: Ref<number> = ref(0)

watch(analysisData, (_newData, _oldData) => {
  progressBarData.value = (Object.keys(analysisData.value.result).length * 100) / 4
  console.log(progressBarData.value)
})

getAnalysisData()

async function getAnalysisData() {
  const { data, pending, error, refresh } = await useFetch(
    `/server/analysis/status/${route.params.statusId}`,
  )
  if (error.value) {
    ui.showMessage('error', 'Error', error.value)
  } else {
    analysisData.value = JSON.parse(data.value)
    console.log(analysisData.value)
    fileUploadData.value = analysisData.value.result?.file_upload
    gameData.value = analysisData.value.result?.game
    roastData.value = analysisData.value.result?.roasting_user
    chessStyleData.value = analysisData.value.result?.chess_style
  }
}
</script>
<template>
  <div class="space-y-6 w-2/3 mx-auto">
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
    <StatusCardWithGamesAnalysis :gameObjects="gameData" />
    <StatusCardWithRoast :roastData="roastData" />
  </div>
</template>
