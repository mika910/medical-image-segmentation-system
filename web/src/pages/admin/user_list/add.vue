<template>
  <el-form :model="form" label-width="85px">
    <el-form-item label="账号:" required>
      <el-input
        v-model="form.username"
        placeholder="请输入账号"
        style="width: 260px"
      />
    </el-form-item>

    <el-form-item label="密码:" required>
      <el-input
        v-model="form.password"
        placeholder="请输入密码"
        style="width: 260px"
      />
    </el-form-item>

    <el-form-item label="昵称:" required>
      <el-input
        v-model="form.name"
        placeholder="请输入昵称"
        style="width: 260px"
      />
    </el-form-item>

    <el-form-item label="手机号:">
      <el-input
        v-model="form.phone"
        placeholder="请输入手机号"
        style="width: 260px"
      />
    </el-form-item>

    <el-form-item label="身份等级:" required>
      <el-select
        v-model="form.level"
        placeholder="请选择用户身份"
        style="width: 260px"
      >
        <el-option label="用户" :value="1" />
        <el-option label="超级管理员" :value="10" />
      </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submit">提交</el-button>
    </el-form-item>
  </el-form>
</template>
<script setup>
import { reactive } from "vue";
import { ElMessage ,ElMessageBox} from "element-plus";
import { api_admin_user_list_post } from "@/api/api";

const form = reactive({
  username: "",
  password: "",
  name: "",
  phone: "",
  level: 1,
});

const submit = () => {
  form.level = parseInt(form.level);

  api_admin_user_list_post(form).then((res) => {
    if (res.data.code === 200) {
      form.username = "";
      form.password = "";
      form.name = "";
      form.phone = "";
      form.level = 1;

      ElMessage({
        message: res.data.msg,
        type: "success",
      });
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};
</script>
<style scoped></style>
