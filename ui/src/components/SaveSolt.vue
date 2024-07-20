<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
    number: Number,
    title: String,
    time: String,
    chapter: String,
    progress: String,
    gameType: { type: Number, default: 1 }
});

if (props.gameType !== 0 && props.gameType !== 1 && props.gameType !== 2 && props.gameType !== 3) {
    throw new Error('Invalid game type');
}

const isEmptySlot = computed(() => {
    return props.title === '';
});

const numberBgColors = ['red', '#525d8c', '#94556b', '#a57949'];
const numberColor = computed(() => {
    if (isEmptySlot.value)
        return numberBgColors[1];
    else
        return numberBgColors[props.gameType];
});



</script>

<template>
    <div class="save-slot" v-if="!isEmptySlot">
        <div class="save-slot-header">
            <span class="save-slot-number">{{ number }}</span>
            <span class="save-slot-title">{{ title }}</span>
            <span class="save-slot-time">{{ time }}</span>
        </div>
        <div class="save-slot-body">
            <span class="save-slot-chap">{{ chapter }}</span>
            <hr>
            <span class="save-slot-progress">{{ progress }}</span>
        </div>
    </div>
    <div class="save-slot" v-else>
        <div class="save-slot-header">
            <span class="save-slot-number">{{ number }}</span>
            <span class="save-slot-title">{{ title }}</span>
            <span class="save-slot-time">{{ time }}</span>
        </div>
        <div class="save-slot-body" style="background-color: #2982b5">
            <br>
            <br>
        </div>
        <div class="save-slot-empty-overlay">
            <p>存档不存在。</p>
        </div>
    </div>
</template>

<style>
.save-slot {
    max-width: 400px;
    font-family: 'Microsoft YaHei', sans-serif;
    border: 4px solid #2982b5;
    position: relative;
}

.save-slot-header {
    color: white;
    background-color: #2982b5;
    padding: 0px 0px 4px 0px;
}

.save-slot-title {
    font-size: 1.2rem;
}

.save-slot-time {
    float: right;
    text-align: right;
    white-space: pre;
    line-height: 1.2;
}

.save-slot-number {
    background-color: v-bind(numberColor);
    color: white;
    border: 2px solid white;

    display: inline-block;
    font-size: 1.5em;
    height: 40px;
    line-height: 40px;
    margin-right: 10px;
    text-align: center;
    width: 40px;
}

.save-slot-body {
    text-align: center;
    padding: 5px 20px;
}

.save-slot-body hr {
    border-top: 2px dashed black;
    color: white;
}

.save-slot-chap {
    font-size: 1.2em;
}

.save-slot-empty-overlay {
    position: absolute;
    top: -4px;
    left: -4px;
    width: calc(100% + 7px);
    height: calc(100% + 7px);
    text-align: center;
    vertical-align: middle;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1;
    color: white;
    font-size: large;

    display: flex;
    justify-content: center;
    align-items: center;
}
</style>