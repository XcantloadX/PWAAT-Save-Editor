import { reactive } from "vue";

const globalApp = reactive({
    currentSave: {
        slots: null,
        path: null
    },

    importSystemSave: async function () {
        await pywebview.api.editor.load();
        this.currentSave.slots = await pywebview.api.get_slots();
        this.currentSave.path = await pywebview.api.editor.get_save_path();
    },
    /** @param {string} path */
    importExternalSave: async function (path) {
        await pywebview.api.editor.load(path);
        this.currentSave.slots = await pywebview.api.get_slots();
        this.currentSave.path = await pywebview.api.editor.get_save_path();
    },
    exportSaveToExternal: async function (path) {
        await pywebview.api.editor.save(path);
    },
    exportSaveToSystem: async function () {
        await pywebview.api.editor.set_account_id_from_system();
        await pywebview.api.editor.save();
    },
});

async function findSavePath() {
    return await pywebview.api.find_save_path();
}

async function findGamePath() {
    return await pywebview.api.find_game_path();
}

export async function open_file_dialog() {
    return await pywebview.api.open_file_dialog();
}

export async function save_file_dialog() {
    return await pywebview.api.save_file_dialog();
}

export async function dirname(path) {
    return await pywebview.api.dirname(path);
}

export default globalApp;
export { findSavePath, findGamePath };