<template>
  <el-button
    title="电脑端"
    v-if="counter.device == '移动端'"
    @click="counter.deviceSwitch()"
    ><el-icon><Monitor /></el-icon
  ></el-button>
  <el-button title="移动端" v-else @click="counter.deviceSwitch()">
    <el-icon><Iphone /></el-icon
  ></el-button>
</template>
<script setup>
import { Monitor, Iphone } from "@element-plus/icons-vue";
import { useCounterStore } from "@/stores/counter";
const counter = useCounterStore();


</script>
<style scoped></style>
