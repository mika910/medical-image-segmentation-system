<template>
  <el-form :model="form" label-width="120px" style="max-width: 500px">
    <!-- 标题 -->
    <el-form-item label="标题:" required>
      <el-input v-model="form.title" placeholder="请输入标题" />
    </el-form-item>

    <!-- 说明 -->
    <el-form-item label="申请说明:">
      <el-input
        type="textarea"
        :rows="4"
        v-model="form.describe"
        placeholder="请输入说明"
      />
    </el-form-item>

    <!-- 数据集来源 -->
    <el-form-item label="数据集来源:" required>
      <el-input
        v-model="form.source"
        placeholder="请输入数据集来源"
        type="textarea"
        :rows="6"
      />
    </el-form-item>

    <!-- 提交按钮 -->
    <el-form-item>
      <el-button type="primary" @click="submit">提交</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { api_data_add_ask_list_post } from "@/api/api";

const form = reactive({});

const submit = () => {
  form.level = parseInt(form.level);

  api_data_add_ask_list_post(form).then((res) => {
    if (res.data.code === 200) {
      ElMessage({
        message: res.data.msg,
        type: "success",
      });
      Object.keys(form).forEach((key) => {
        form[key] = "";
      });
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};
</script>
<style scoped></style>
