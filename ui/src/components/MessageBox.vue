<script setup>
import { ref } from 'vue';

const showDialog = ref(false);
const titleRef = ref('');
const messageRef = ref('');
const typeRef = ref('');
const iconRef = ref('');

const onResult = ref(() => {});

const _show = function (title, message, type, icon) {
    return new Promise((resolve, reject) => {
        titleRef.value = title;
        messageRef.value = message;
        typeRef.value = type;
        iconRef.value = icon;
        showDialog.value = true;

        onResult.value = (result) => {
            showDialog.value = false;
            resolve(result);
        };

        // return { dialog, title, message, buttons, icon, confirm, cancel };
    });
};

defineExpose({ show: _show });
</script>

<template>
    <v-dialog v-model="showDialog" max-width="500">
        <v-card>
            <v-card-title class="headline">{{ titleRef }}</v-card-title>
            <v-card-text>{{ messageRef }}</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <template v-if="typeRef === 'okcancel'">
                    <v-btn color="primary" text @click="onResult('ok')">OK</v-btn>
                    <v-btn color="secondary" text @click="onResult('canel')">Cancel</v-btn>
                </template>
                <template v-else-if="typeRef === 'ok'">
                    <v-btn color="primary" text @click="onResult('ok')">OK</v-btn>
                </template>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
