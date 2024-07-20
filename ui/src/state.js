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

export default globalApp;