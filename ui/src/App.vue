<script setup>
import { ref } from 'vue';
import PagePreview from './pages/PagePreview.vue';
import PageHome from './pages/PageHome.vue';
import globalApp from './state';

const slots = ref([]);

const showSideBar = ref(false);
const currentPage = ref('home');

const PAGE_HOME = 'home';
const PAGE_EDITOR_PREVIEW = 'editor-preview';

/** @param {string} page */
function goto(page) {
  currentPage.value = page;
  showSideBar.value = false;
}
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

</template>

<style>
#app-main {
  padding: 20px;
}
</style>
