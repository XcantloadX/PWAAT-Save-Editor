<script setup>
import { ref } from 'vue';
import globalApp from '../globalApp';

const showExportSystemDialog = ref(false);
const showSuccessDialog = ref(false);
const showFailDialog = ref(false);
const failMessage = ref('');

function showError(e) {
    showFailDialog.value = true;
    failMessage.value = `${e.name}: ${e.message}\n${e.stack}`;
}

function importSystemSave() {
    globalApp.importSystemSave();
}

async function importExternalSave() {
    let paths = await pywebview.api.open_file_dialog();
    if (!paths) {
        return;
    }
    await globalApp.importExternalSave(paths[0]);
}

async function exportSystemSave() {
    showExportSystemDialog.value = false;
    try {
        await globalApp.exportSaveToSystem();
        showSuccessDialog.value = true;
    } catch (e) {
        showError(e);
    }
}

async function exportExternalSave() {
    // TODO 导出前检查是否已打开存档
    try {
        let path = await pywebview.api.save_file_dialog();
        console.log(path);
        if (!path) {
            return;
        }
        await globalApp.exportSaveToExternal(path);
        showSuccessDialog.value = true;
    } catch (e) {
        showError(e);
        return;
    }
}

</script>

<template>
    <div class="page-home d-flex flex-column w-75">
        <h2 v-if="!globalApp?.currentSave?.path">未加载任何存档</h2>
        <div v-else>
            <h2>已载入存档</h2>
            <small>{{ globalApp?.currentSave?.path }}</small>
        </div>
        <br>
        <v-btn variant="text" prepend-icon="mdi-open-in-app" @click="importSystemSave()">导入系统存档</v-btn>
        <v-btn variant="text" prepend-icon="mdi-open-in-app" @click="importExternalSave">导入外部存档</v-btn>
        <v-divider></v-divider>
        <v-btn variant="text" prepend-icon="mdi-export" @click="showExportSystemDialog = true">导出当前存档至系统</v-btn>
        <v-btn variant="text" prepend-icon="mdi-export" @click="exportExternalSave()">导出当前存档至外部</v-btn>
    </div>

    <v-dialog v-model="showExportSystemDialog" width="auto">
        <v-card
            title="导出存档"
            prepend-icon="mdi-export"
        >
            <template v-slot:text>
                <p class="text-orange-darken-2"><v-icon color="orange-darken-2">mdi-alert-circle</v-icon>需要保证当前有系统存档且游戏内可正常读取，否则将无法正常导出。</p>
                <p class="text-orange-darken-2"><v-icon color="orange-darken-2">mdi-alert-circle</v-icon>导出前请先确保游戏已关闭。</p>
                <p class="text-red"><v-icon color="red">mdi-alert-circle</v-icon>当前系统存档将被覆盖，请注意备份。</p>
            </template>
            <template v-slot:actions>
                <v-btn text @click="showExportSystemDialog = false">取消</v-btn>
                <v-btn text @click="exportSystemSave">导出</v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog v-model="showSuccessDialog" width="auto">
        <v-card
            title="提示"
            prepend-icon="mdi-check"
            text="导出成功！"
        >
            <template v-slot:actions>
                <v-btn text @click="showSuccessDialog = false">确定</v-btn>
            </template>

        </v-card>
    </v-dialog>

    <v-dialog v-model="showFailDialog" width="auto">
        <v-card
            title="导出失败"
            prepend-icon="mdi-alert-circle"
        >
            <template v-slot:actions>
                <v-btn text @click="showFailDialog = false">确定</v-btn>
            </template>
            <template v-slot:text>
                <textarea rows="15" cols="50" spellcheck="false">{{ failMessage }}</textarea>
            </template>
        </v-card>
    </v-dialog>
</template>

<style>
.page-home {
    margin: 0 auto;
    text-align: center;
}
</style>