<template>
  <el-form :model="form" label-width="85px">
    <el-form-item label="账号:" required>
      <el-input
        v-model="form.username"
        placeholder="请输入账号"
        style="width: 260px"
        disabled
      />
    </el-form-item>

    <el-form-item label="密码:" required>
      <el-input
        v-model="form.password"
        placeholder="不修改密码可不输入"
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
import { onMounted, reactive } from "vue";
import {
  api_admin_user_list_one_get,
  api_admin_user_list_put,
} from "@/api/api";
import { useRoute, useRouter } from "vue-router";
import { ElMessage ,ElMessageBox} from "element-plus";
const route = useRoute();

const form = reactive({
  username: "",
  password: "",
  name: "",
  phone: "",
  level: 1,
  uid: route.params.id,
});

const submit = () => {
  form.level = parseInt(form.level);
  api_admin_user_list_put(form).then((res) => {
    if (res.data.code === 200) {
      dataLoad();
      ElMessage({
        message: res.data.msg,
        type: "success",
      });
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

const dataLoad = () => {
  let dic = {
    uid: route.params.id,
  };
  console.log(dic);
  api_admin_user_list_one_get(dic).then((res) => {
    if (res.data.code === 200) {
      form.username = res.data.data.username;
      form.name = res.data.data.name;
      form.phone = res.data.data.phone;
      form.level = res.data.data.level;
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
