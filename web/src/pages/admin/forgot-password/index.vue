<template>
  <div class="global">
    <div class="login_frame">
      <div class="title">重置密码</div>
      <form class="form">
        <div>
          <input
            type="text"
            v-model="form.username"
            placeholder="请输入用户名"
          />
        </div>
        <div v-if="step === 1">
          <input
            type="text"
            v-model="form.phone"
            placeholder="请输入注册手机号"
          />
        </div>
        <div v-if="step === 2">
          <input
            type="password"
            v-model="form.password"
            placeholder="请输入新密码"
          />
        </div>
        <div v-if="step === 2">
          <input
            type="password"
            v-model="form.confirmPassword"
            placeholder="请确认新密码"
          />
        </div>
      </form>
      <button class="button_group" @click="handleSubmit">
        {{ step === 1 ? '验证身份' : '重置密码' }}
      </button>

      <div class="bottom-links">
        <router-link to="/admin/login" class="login-link">返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { api_verify_identity, api_reset_password } from "@/api/api";

const Router = useRouter();
const step = ref(1); // 1: 验证身份, 2: 重置密码

const form = reactive({
  username: "",
  phone: "",
  password: "",
  confirmPassword: "",
});

// 处理表单提交
const handleSubmit = () => {
  if (step.value === 1) {
    // 验证身份
    if (!form.username) {
      ElMessage.error('请输入用户名');
      return;
    }
    if (!form.phone) {
      ElMessage.error('请输入注册手机号');
      return;
    }
    
    // 调用验证身份API
    api_verify_identity({
      username: form.username,
      phone: form.phone
    }).then((res) => {
      if (res.data.code === 200) {
        ElMessage({
          message: '身份验证成功，请设置新密码',
          type: "success",
        });
        step.value = 2;
      } else {
        ElMessage.error(res.data.msg);
      }
    });
  } else {
    // 重置密码
    if (!form.password) {
      ElMessage.error('请输入新密码');
      return;
    }
    if (form.password.length < 6) {
      ElMessage.error('密码长度不能少于6位');
      return;
    }
    if (form.password !== form.confirmPassword) {
      ElMessage.error('两次输入的密码不一致');
      return;
    }
    
    // 调用重置密码API
    api_reset_password({
      username: form.username,
      password: form.password
    }).then((res) => {
      if (res.data.code === 200) {
        ElMessage({
          message: '密码重置成功，请重新登录',
          type: "success",
        });
        Router.push('/admin/login');
      } else {
        ElMessage.error(res.data.msg);
      }
    });
  }
};
</script>

<style scoped>
.global {
  width: 100%;
  height: 100%;
  background-color: #e8f4fc; /* 修改背景颜色为更柔和的蓝色 */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
}
.login_frame {
  width: 35rem;
  height: 42.5rem;
  background-color: rgb(255, 255, 255);
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 添加轻微阴影效果 */
}

.title {
  font-size: 2rem;
  font-weight: 500;
  margin-top: 5rem;
}
.form {
  margin-top: 3.125rem;
}

.form div {
  margin-bottom: 2.5rem;
}

.form input {
  width: 18.75rem;
  height: 3.75rem;
  border-radius: 0.312rem;
  border: 0px;
  box-shadow: 0px 0px 2px rgb(146, 146, 146);
  font-size: 1.5rem;
  text-indent:1.5625rem;
  color: #333;
  caret-color: rgb(146, 146, 146);
}

.form input:focus {
  outline: none;
  border: 0px;
  box-shadow: 0px 0px 2px rgb(16, 104, 236);
}
.button_group {
  width: 18.75rem;
  height: 2.1875rem;
  font-size: 1.25rem;
  border: none;
  border-radius: 2.1875rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  background-color: black;
  color: #fff;
}

.button_group:hover {
  cursor: pointer;
}

.button_group:active {
  transform: scale(0.98);
}

.bottom-links {
  width: 18.75rem;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.login-link {
  color: #1066ec;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}
</style>