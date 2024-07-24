<script setup>
import { onMounted, ref } from 'vue';
import PagePreview from './pages/PagePreview.vue';
import PageHome from './pages/PageHome.vue';
import MessageBox from './components/MessageBox.vue';
import globalApp, { findGamePath, findSavePath, dirname, open_file_dialog } from './globalApp';

const slots = ref([]);
const messageBox = ref(null);

const showSideBar = ref(false);
const currentPage = ref('home');

const PAGE_HOME = 'home';
const PAGE_EDITOR_PREVIEW = 'editor-preview';

/** @param {string} page */
function goto(page) {
  currentPage.value = page;
  showSideBar.value = false;
}
window.addEventListener('pywebviewready', async function() {
  console.log('App mounted');
  let savePath = await findSavePath();
  let gamePath = await findGamePath();
  if (!savePath) {
    await messageBox.value.show('错误', '未找到存档路径，请手动选择存档文件（systemdata 文件）。', 'ok');
    let paths = await open_file_dialog();
    if (!paths) {
      await messageBox.value.show('错误', '未选择存档文件，无法继续。', 'ok');
    }
    savePath = paths[0];
  }
  if (!gamePath) {
    await messageBox.value.show('错误', '未找到游戏路径，请手动选择游戏文件（PWAAT.exe 文件）。', 'ok');
    let paths = await open_file_dialog();
    console.log(paths);
    if (!paths) {
      await messageBox.value.show('错误', '未选择游戏文件，无法继续。', 'ok');
    }
    gamePath = paths[0];
    gamePath = await dirname(gamePath);
  }
  window.pywebview.api.init(gamePath, savePath);
});
</script>

<template>
  <v-app>
    <v-app-bar color="primary">
      <v-app-bar-title>逆转裁判 123 存档修改器</v-app-bar-title>
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click.stop="showSideBar = !showSideBar"></v-app-bar-nav-icon>
      </template>
    </v-app-bar>
    <v-navigation-drawer v-model="showSideBar" temporary>
      <v-list>
        <v-list-item link title="首页" prepend-icon="mdi-home" @click="goto(PAGE_HOME)"></v-list-item>
        <v-divider></v-divider>
        <v-list-item link title="存档预览" prepend-icon="mdi-view-agenda" @click="goto(PAGE_EDITOR_PREVIEW)"></v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main >
      <div id="app-main">
        <div v-if="currentPage === 'home'">
          <PageHome />
        </div>
        <div v-else-if="currentPage === 'editor-preview'">
          <PagePreview />
        </div>
      </div>
    </v-main>
  </v-app>

  <MessageBox ref="messageBox" />
</template>

<style>
#app-main {
  padding: 20px;
}
</style>
