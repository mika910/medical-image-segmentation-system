<template>
  <div class="pages-main">
    <div class="top-search">
      <el-form :inline="true" label-width="auto">
        <el-form-item
          label="账号:"
          style="margin-bottom: 0.5rem"
          v-if="datas.level == 10"
        >
          <el-input placeholder="请输入" v-model="form.username" />
        </el-form-item>

        <el-form-item label="标题:" style="margin-bottom: 0.5rem">
          <el-input placeholder="请输入" v-model="form.title" />
        </el-form-item>

        <el-form-item label="说明:" style="margin-bottom: 0.5rem">
          <el-input placeholder="请输入" v-model="form.describe" />
        </el-form-item>

        <el-form-item label="数据集来源:" style="margin-bottom: 0.5rem">
          <el-input placeholder="请输入" v-model="form.source" />
        </el-form-item>

        <el-form-item label="状态:" style="margin-bottom: 0.5rem">
          <el-select v-model="form.state" placeholder="请选择">
            <el-option label="全部" value="" />
            <el-option label="等待管理员处理" value="等待管理员处理" />
            <el-option label="管理员处理中" value="管理员处理中" />
            <el-option label="已完成请求" value="已完成请求" />
            <el-option label="处理失败" value="处理失败" />
          </el-select>
        </el-form-item>

        <el-form-item label="管理员回复:" style="margin-bottom: 0.5rem">
          <el-input placeholder="请输入" v-model="form.admin_reply" />
        </el-form-item>

        <el-form-item label-width="80px" style="margin-bottom: 0.5rem">
          <el-button @click="(form.page = 1), dataLoad()">搜索</el-button>
        </el-form-item>
      </el-form>

      <div class="button-group">
        <div>
          <el-button type="success" @click="add">提交新的数据集申请</el-button>
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

        <el-table-column-plus
          prop="username"
          label="账号"
          v-if="datas.level == 10"
        />
        <el-table-column-plus prop="title" label="标题" />

        <el-table-column-plus
          prop="describe"
          show-overflow-tooltip
          label="说明"
        />
        <el-table-column-plus
          prop="source"
          show-overflow-tooltip
          label="数据集来源"
        />

        <el-table-column-plus prop="state" label="状态">
          <template #default="scope">
            <el-tag v-if="scope.row.state === '等待管理员处理'" type="warning"
              >等待管理员处理</el-tag
            >
            <el-tag v-else-if="scope.row.state === '管理员处理中'" type="info"
              >管理员处理中</el-tag
            >
            <el-tag v-else-if="scope.row.state === '已完成请求'" type="success"
              >已完成请求</el-tag
            >
            <el-tag v-else-if="scope.row.state === '处理失败'" type="danger"
              >处理失败</el-tag
            >
            <el-tag v-else type="info">{{ scope.row.state }}</el-tag>
          </template>
        </el-table-column-plus>

        <el-table-column-plus prop="admin_reply" label="管理员回复" />

        <el-table-column-plus prop="CreatedAt" label="提交时间">
          <template #default="scope">
            {{ formatTime(scope.row.CreatedAt) }}
          </template>
        </el-table-column-plus>

        <el-table-column-plus label="操作" width="200">
          <template #default="scope">
            <div style="display: flex; flex-wrap: wrap">
              <el-button @click="show(scope.row)" style="margin: 0.25rem"
                >查看详情</el-button
              >
              <el-button
                @click="put(scope.row)"
                type="primary"
                v-if="datas.level == 10"
                style="margin: 0.25rem"
                >修改</el-button
              >
              <el-button
                @click="del_fun(scope.row)"
                type="danger"
                v-if="datas.level == 10"
                style="margin: 0.25rem"
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
  api_data_add_ask_list_get,
  api_data_add_ask_list_del,
} from "@/api/api";

const Router = useRouter();

const datas = reactive({
  total: 0,
  dataTable: [],
  select: [],
  level: parseInt(localStorage.getItem("level")),
});

const form = reactive({
  page: 1,
  pagesize: 10,
});

const handleSelectionChange = (eve) => {
  datas.select = eve;
};

const add = () => {
  Router.push("/admin/data_add_ask_list/add");
};
const put = (row) => {
  Router.push("/admin/data_add_ask_list/put/" + row.id);
};
const show = (row) => {
  Router.push("/admin/data_add_ask_list/show/" + row.id);
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
      api_data_add_ask_list_del(dic).then((res) => {
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
  api_data_add_ask_list_get(form).then((res) => {
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
