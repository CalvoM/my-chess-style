<script setup lang="ts">
import { ref, type Ref } from 'vue'
import { useFetch } from '@vueuse/core'
import { useUIStore } from '@/stores/ui'
import type { PlatformOptions } from '@/types'

const uploadFile = ref()
const pgnUsername: Ref<string> = ref('')
const platformUsername: Ref<string> = ref('')
const externalPlatform: Ref<PlatformOptions> = ref({})
const trackingID: Ref<string> = ref('')
const toastClass: Ref<string> = ref('')
const includeRoast: Ref<boolean> = ref(false)

const supportedPlatforms = ref([
  { name: 'Chess.com', code: 'chess.com' },
  { name: 'Lichess', code: 'lichess' },
])

const ui = useUIStore()

async function uploadPGNFile() {
  const formData = new FormData()
  formData.append('pgn_file', uploadFile.value.files[0])
  formData.append('usernames', pgnUsername.value)
  formData.append('include_roast', includeRoast.value)
  const { data, pending, error, refresh } = await useFetch('/server/pgn/upload', {
    method: 'POST',
    body: formData,
  }).json()
  if (error.value) {
    toastClass.value = ui.showMessage('error', 'Error', error.value)
  } else {
    await navigator.clipboard.writeText(data.value.status_id)
    toastClass.value = ui.showMessage(
      'success',
      'Upload successful',
      `Tracking ID copied to clipboard!`,
    )
  }
}

async function uploadPlatformUsernames() {
  const { data, pending, error, refresh } = await useFetch('/server/pgn/external_user/')
    .post({
      username: platformUsername.value,
      platform: externalPlatform.value.code,
      include_roast: includeRoast.value,
    })
    .json()
  if (error.value) {
    toastClass.value = ui.showMessage('error', 'Error', error.value)
  } else {
    await navigator.clipboard.writeText(data.value.status_id)
    toastClass.value = ui.showMessage(
      'success',
      'Upload successful',
      `Tracking ID copied to clipboard!`,
    )
  }
}

async function checkStatusByTransactionID() {
  const { data, pending, error, refresh } = await useFetch(
    `/server/analysis/status/${trackingID.value}`,
  ).json()
  if (error.value) {
    toastClass.value = ui.showMessage('error', 'Error', error.value)
  } else {
    toastClass.value = ui.showMessage('success', 'Upload successful', `Tracking ID: ${data.value}`)
  }
}
</script>

<template>
  <Toast />
  <Card class="w-full shadow-xl">
    <template #title> Start Your Analysis </template>
    <template #subtitle>
      Upload a PGN file, provide your username from Lichess or Chess.com, or track existing analysis
    </template>
    <template #content>
      <Tabs value="upload_pgn" class="w-full">
        <TabList class="w-full">
          <Tab value="upload_pgn" class="flex items-center gap-2 grow">
            <i class="pi pi-upload"></i>
            Upload PGN File
          </Tab>
          <Tab value="enter_username" class="flex items-center gap-2 grow">
            <i class="pi pi-user"></i>
            Enter Username
          </Tab>
          <Tab value="track_progress" class="flex items-center gap-2 grow">
            <i class="pi pi-search"></i>
            Track Progress
          </Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="upload_pgn" class="flex flex-col gap-4 mt-6">
            <div class="flex flex-col gap-2">
              <label for="pgn-file">PGN File</label><br />
              <fileUpload
                id="pgn-file"
                ref="uploadFile"
                mode="basic"
                name="demo[]"
                accept=".pgn"
                :multiple="false"
              />
            </div>
            <div class="flex flex-col gap-2">
              <label for="pgn-username">Your Username (for analysis)</label><br />
              <InputText
                id="pgn-username"
                type="text"
                placeholder="Enter your chess username"
                v-model="pgnUsername"
                class="w-full"
              />
            </div>
            <div class="flex items-center space-x-2">
              <ToggleSwitch id="include-roast-username" v-model="includeRoast" />
              <label for="include-roast-username" class="text-md pl-2">
                Include AI roast & commentary (prepare yourself! 🔥)
              </label>
            </div>
            <Button
              class="w-full"
              :disabled="!pgnUsername || uploadFile.files.length == 0"
              @click="uploadPGNFile"
            >
              Analyze PGN File
            </Button>
          </TabPanel>
          <TabPanel value="enter_username" class="flex flex-col gap-4 mt-6">
            <div class="flex flex-col gap-2">
              <label for="platform">Platform</label><br />
              <Select
                id="platform"
                v-model="externalPlatform"
                :options="supportedPlatforms"
                optionLabel="name"
                placeholder="Select chess platform"
                class="w-full border border-input bg-background rounded-md"
              />
            </div>
            <div class="flex flex-col gap-2">
              <label for="username">Username</label><br />
              <InputText
                id="username"
                placeholder="Enter your username"
                v-model="platformUsername"
              />
            </div>
            <div class="flex items-center space-x-2">
              <ToggleSwitch id="include-roast-username" v-model="includeRoast" />
              <label for="include-roast-username" class="text-md pl-2">
                Include AI roast & commentary (prepare yourself! 🔥)
              </label>
            </div>
            <Button class="w-full" :disabled="!platformUsername" @click="uploadPlatformUsernames">
              Analyze Games
            </Button>
          </TabPanel>
          <TabPanel value="track_progress" class="flex flex-col gap-4 mt-6">
            <div class="flex flex-col gap-2">
              <label for="tracking-id">Tracking ID</label><br />
              <InputText
                id="tracking-id"
                placeholder="Enter your tracking ID (e.g., CGA-1234567890-ABC123)"
                v-model="trackingID"
              />
            </div>
            <Button class="w-full" :disabled="!trackingID" @click="checkStatusByTransactionID">
              Track Progress by ID
            </Button>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </template>
  </Card>
</template>
<style lang="css" scoped>
label {
  font-weight: bold;
}
</style>
