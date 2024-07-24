<script setup>
import { ref } from 'vue';
import SaveSolt from '../components/SaveSolt.vue';
import globalApp from '@/globalApp';

const slots = ref(globalApp.currentSave.slots);

/**
 * @param title {string}
 */
function get_game_type(title) {
    title = title.trim();
    if (title === '逆转裁判1')
        return 1;
    else if (title === '逆转裁判2')
        return 2;
    else if (title === '逆转裁判3')
        return 3;
    else if (title === '逆转裁判 复苏的逆转')
        return 1;
    else
        return 0;
}
</script>

<template>
    <div class="preview">
        <div class="save-slots">
            <SaveSolt v-for="(s, index) in slots" :number="index + 1" :game-type="get_game_type(s.title)"
                :title="s.title" :time="s.time" :progress="s.progress" :chapter="s.scenario" />
        </div>
    </div>
</template>

<style>
.preview {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    margin: 0 auto;
    padding: 10px;
}

.save-slots {
    height: 100%;
    flex: 1;
    /* overflow-y: scroll; */
}

.save-slots>* {
    margin: 0 auto;
    margin-bottom: 10px;
    min-width: 400px;
}
</style>