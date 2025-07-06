<template>
  <div class="pages-main">
    <div class="top-search">
      <el-form>
        <el-form-item>
          <el-form-item
            label="账号:"
            label-width="60px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索账号" v-model="form.username" />
          </el-form-item>
          <el-form-item
            label="姓名:"
            label-width="60px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索姓名" v-model="form.name" />
          </el-form-item>
          <el-form-item
            label="手机号:"
            label-width="60px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索手机号" v-model="form.phone" />
          </el-form-item>
          <el-form-item label-width="60px" style="margin-bottom: 0.5rem">
            <el-button @click="(form.page = 1), dataLoad()">搜索</el-button>
          </el-form-item>
        </el-form-item>
      </el-form>

      <div class="button-group">
        <div>
          <el-button type="danger" @click="batch_del_fun">批量删除</el-button>
          <el-button type="success" @click="add">添加账号</el-button>
        </div>
        <div></div>
        <div>
          <device-switch-button />
        </div>
      </div>
    </div>
    <div>
      <el-table-plus
        :data="datas.dataTable"
        @selection-change="handleSelectionChange"
        :border="false"
      >
        <el-table-column-plus type="selection" width="55" />

        <el-table-column-plus prop="username" label="账号" />
        <el-table-column-plus prop="name" label="姓名" />

        <el-table-column-plus prop="phone" label="手机号" />

        <el-table-column-plus prop="CreatedAt" label="添加时间">
          <template #default="scope">
            {{ formatTime(scope.row.CreatedAt) }}
          </template>
        </el-table-column-plus>

        <el-table-column-plus prop="level" label="身份等级">
          <template #default="scope">
            {{ datas.levelDic[scope.row.level] }}
          </template>
        </el-table-column-plus>

        <el-table-column-plus label="操作" width="200">
          <template #default="scope">
            <div style="display: flex">
              <el-button @click="put(scope.row)" type="primary">修改</el-button>
              <el-button @click="del_fun(scope.row)" type="danger"
                >删除</el-button
              >
            </div>
          </template>
        </el-table-column-plus>
      </el-table-plus>
    </div>
    <div class="pagination">
      <el-pagination
        v-model:current-page="form.page"
        v-model:page-size="form.pagesize"
        :page-sizes="[30, 50, 100, 300, 500, 1000]"
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="datas.total"
        @size-change="dataLoad"
        @current-change="dataLoad"
      >
      </el-pagination>
    </div>
  </div>
</template>
<script setup>
import { onActivated, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";

import { formatTime } from "@/myTools/my_time";

import {
  api_admin_user_list_get,
  api_admin_user_list_del,
} from "@/api/api";

const Router = useRouter();

const datas = reactive({
  total: 0,
  dataTable: [],
  select: [],

  levelDic: {
    1: "用户",
    10: "超级管理员",
  },
});

const form = reactive({
  page: 1,
  pagesize: 10,
  username: "",
  name: "",
  phone: "",
});

const handleSelectionChange = (eve) => {
  datas.select = eve;
};

const add = () => {
  Router.push("/admin/user_list/add");
};
const put = (row) => {
  Router.push("/admin/user_list/put/" + row.uid);
};

const del_fun = (row) => {
  ElMessageBox.confirm("确定删除?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      let dic = {
        id: row.id,
      };
      api_admin_user_list_del(dic).then((res) => {
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
    })
    .catch(() => {});
};

const batch_del_fun = () => {
  ElMessageBox.confirm("确定删除选中数据?", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      let ids = "";
      for (let index = 0; index < datas.select.length; index++) {
        const item = datas.select[index];
        ids = ids + "," + item.id;
      }

      let dic = {
        id: ids,
      };
      api_admin_user_list_del(dic).then((res) => {
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
    })
    .catch(() => {});
};

const dataLoad = () => {
  api_admin_user_list_get(form).then((res) => {
    if (res.data.code === 200) {
      datas.dataTable = res.data.data.data;
      datas.total = res.data.data.total;
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

//在缓存加载时 重新加载一次列表数据
onActivated(() => {
  dataLoad();
});

onMounted(() => {
  dataLoad();
});
</script>
<style scoped>
.top-search {
  padding: 1rem;
  box-shadow: 0px 0px 3px rgba(0, 0, 0, 0.644);
  border-radius: 0.25rem;
  margin-bottom: 1rem;
}
.pagination {
  margin-top: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  overflow: auto;
}
.button-group {
  display: flex;
  justify-content: space-between;
}

.button-group button {
  margin: 0.5rem;
}
</style>
