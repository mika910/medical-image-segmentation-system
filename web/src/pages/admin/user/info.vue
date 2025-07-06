<template>
  <div class="personal-info">
    <div class="person">
      <h4 style="padding-bottom: 1rem">个人信息</h4>
      <el-form class="info-form">
        <!-- 删除了整个用户头像上传区域 -->
        
        <div class="user-info">
          <div>账号</div>
          <div>{{ datas.username }}</div>
        </div>

        <div class="user-info">
          <div>昵称</div>
          <div>{{ datas.name }}</div>
        </div>
        
        <div class="user-info">
          <div>手机号码</div>
          <div>{{ datas.phone }}</div>
        </div>

        <div class="user-info">
          <div>所属角色</div>
          <div>{{ datas.levelDic[datas.level] }}</div>
        </div>

        <div
          class="user-info"
          style="border-bottom: 1px solid rgb(230, 230, 230)"
        >
          <div>创建日期</div>
          <div>{{ datas.CreatedAt }}</div>
        </div>
      </el-form>
    </div>

    <div class="info-set">
      <h4 style="padding-bottom: 1rem">资料修改</h4>

      <div>



        
        <div class="form-group">
          <label for="age">昵称:</label>
          <el-input
            v-model="form.name"
            placeholder="请输入昵称"
            style="width: 250px"
          />
        </div>



        <div class="form-group">
          <label for="age">手机号:</label>
          <el-input
            v-model="form.phone"
            placeholder="请输入手机号"
            style="width: 250px"
          />
        </div>

        <div class="form-group">
          <label for="age">新密码:</label>
          <el-input
            v-model="form.password"
            placeholder="密码长度需要在6位以上"
            style="min-width: 200px"
          />
        </div>
        <el-button @click="submit">保存</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive } from "vue";
import {
  api_user_info_get,
  api_user_info_put,
  // 删除不需要的导入
  // userInfoImgLinkPost,
  // userInfoImgLinkGet,
} from "@/api/api";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
const router = useRouter();

const datas = reactive({
  // 保留img字段以避免报错，但不再使用
  img: "",
  levelDic: {
    1: "用户",
    10: "超级管理员",
  },
});

const form = reactive({
  password: "",
  name: "",
  phone: "",
});

// 删除与图片上传相关的变量和函数
// const headers = {
//   Authorization: localStorage.getItem("token"),
// };
// const onSuccess = (res) => {...};
// const onError = (res) => {...};

const submit = () => {
  // 保持不变
  // ...
  api_user_info_put(form).then((res) => {
    if (res.data.code === 200) {
      ElMessage({
        message: res.data.msg,
        type: "success",
      });
      dataLoad();
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

const dataLoad = () => {
  api_user_info_get().then((res) => {
    if (res.data.code === 200) {
      datas.username = res.data.data.username;
      datas.name = res.data.data.name;
      datas.phone = res.data.data.phone;
      datas.img = res.data.data.img;
      datas.level = res.data.data.level;
      datas.CreatedAt = res.data.data.CreatedAt;
      localStorage.setItem("img", res.data.data.img);

      form.name = res.data.data.name;
      form.phone = res.data.data.phone;

    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

onMounted(() => {
  dataLoad();
});
</script>

<style scoped>
.personal-info {
  border-radius: 5px;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

/* 删除与图片相关的样式 */
/* .user-info-img-div {
  display: flex;
  justify-content: center;
  width: 100%;
  align-items: center;
  margin-bottom: 2rem;
}
.user-info-img-div img {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
} */

/* 其余样式保持不变 */
.info-form {
  background-color: #fff;
  /* padding: 20px; */
  border-radius: 5px;
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.person {
  flex: 1;
  padding: 2rem;
  max-width: 280px;
  min-height: 400px;
  border: 1px solid rgb(219, 219, 219);
  border-radius: 5px;
  box-shadow: 3px 3px 10px rgb(219, 219, 219);
  margin-bottom: 1rem;
  margin-right: 2rem;
}
.person > h1 {
  margin-bottom: 2rem;
}

.user-info {
  display: flex;
  justify-content: space-between;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border-top: 1px solid rgb(230, 230, 230);
  /* border-bottom: 1px solid rgba(230, 230, 230, 0.548); */
  font-size: 14px;
  font-weight: bold;
}

.user-info-img-div {
  display: flex;
  justify-content: center;
  width: 100%;
  align-items: center;
  margin-bottom: 2rem;
}
.user-info-img-div img {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
}

.info-set {
  padding: 2rem;
  /* width: 70%; */
  min-width: 250px;
  flex: 3;
  min-height: 400px;
  border: 1px solid rgb(219, 219, 219);
  border-radius: 5px;
  box-shadow: 3px 3px 10px rgb(219, 219, 219);
  margin-bottom: 1rem;
}
</style>
