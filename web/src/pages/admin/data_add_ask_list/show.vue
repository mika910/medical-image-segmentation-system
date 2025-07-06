<template>
  <el-form :model="form" label-width="120px" style="max-width: 500px">
    <!-- 标题 -->
    <el-form-item label="标题:">
      <el-input v-model="form.title" placeholder="请输入标题" disabled />
    </el-form-item>

    <!-- 说明 -->
    <el-form-item label="说明:">
      <el-input
        type="textarea"
        :rows="4"
        v-model="form.describe"
        placeholder="请输入说明"
        disabled
      />
    </el-form-item>

    <!-- 数据集来源 -->
    <el-form-item label="数据集来源:">
      <el-input v-model="form.source" placeholder="请输入数据集来源" disabled />
    </el-form-item>

    <!-- 状态 -->
    <el-form-item label="状态:">
      <el-select v-model="form.state" placeholder="请选择状态" disabled>
        <el-option label="等待管理员处理" value="等待管理员处理" />
        <el-option label="管理员处理中" value="管理员处理中" />
        <el-option label="已完成请求" value="已完成请求" />
        <el-option label="处理失败" value="处理失败" />
      </el-select>
    </el-form-item>

    <!-- 管理员回复 -->
    <el-form-item label="管理员回复:">
      <el-input
        type="textarea"
        :rows="4"
        v-model="form.admin_reply"
        placeholder="请输入管理员回复"
        disabled
      />
    </el-form-item>
  </el-form>
</template>
<script setup>
import { onMounted, reactive } from "vue";
import { api_data_add_ask_one_get } from "@/api/api";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
const route = useRoute();

const form = reactive({});

const dataLoad = () => {
  let dic = {
    id: route.params.id,
  };

  api_data_add_ask_one_get(dic).then((res) => {
    if (res.data.code === 200) {
      Object.keys(res.data.data).forEach((key) => {
        form[key] = res.data.data[key];
      });
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

onMounted(() => {
  dataLoad();
});
</script>
<style scoped></style>
