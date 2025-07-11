<script setup lang="ts">
  import { ref } from 'vue';
  const fileupload = ref();
  const pgn_username = ref(null);
  const platform_username = ref(null);
  const trackingID = ref(null);
</script>

<template>
  <Card class="w-full shadow-xl">
    <template #title> Start Your Analysis </template>
    <template #subtitle>
      Upload a PGN file, provide your username from Lichess or Chess.com, or
      track existing analysis
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
              <label for="pgn-file">PGN File</label><br>
              <FileUpload ref="fileupload" mode="basic" name="demo[]" url="/api/upload" accept=".pgn" :maxFileSize="1000000" :multiple="false">
              </FileUpload>
            </div>
            <div class="flex flex-col gap-2">
              <label for="pgn-username">Your Username (for analysis)</label><br>
              <InputText
                id="pgn-username"
                type = "text"
                placeholder="Enter your chess username"
                v-model="pgn_username"
                class="w-full"
              />
            </div>
            <Button class="w-full" :disabled="!pgn_username || fileupload.files.length==0">
              Analyze PGN File
            </Button>
          </TabPanel>
          <TabPanel value="enter_username" class="flex flex-col gap-4 mt-6">
            <div class="flex flex-col gap-2">
                    <label for="platform">Platform</label><br>
                    <select
                      id="platform"
                      class="w-full px-3 py-2 border border-input bg-background rounded-md"
                    >
                      <option value="lichess">Lichess</option>
                      <option value="chess.com">Chess.com</option>
                    </select>
                  </div>
                  <div class="flex flex-col gap-2">
                    <label for="username">Username</label><br>
                    <InputText
                      id="username"
                      placeholder="Enter your username"
                      v-model="platform_username"
                    />
                  </div>
                  <Button class="w-full" :disabled="!platform_username">
                    Analyze Games
                  </Button>
          </TabPanel>
          <TabPanel value="track_progress" class="flex flex-col gap-4 mt-6">
            <div class="flex flex-col gap-2">
                    <label for="tracking-id">Tracking ID</label><br>
                    <InputText
                      id="tracking-id"
                      placeholder="Enter your tracking ID (e.g., CGA-1234567890-ABC123)"
                    />
                  </div>
                  <Button class="w-full" :disabled="!trackingID">
                    Track Progress
                  </Button>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </template>
  </Card>
</template>
<style lang="css" scoped>
label{
  font-weight: bold;
}
</style>
