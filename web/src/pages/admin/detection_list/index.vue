<template>
  <div class="pages-main">
    <div class="top-search">
      <el-form>
        <el-form-item>
          <el-form-item
            v-if="datas.level == 10"
            label="账号:"
            label-width="60px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索账号" v-model="form.username" />
          </el-form-item>

          <el-form-item
            label="模型:"
            label-width="80px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索文件名" v-model="form.model" />
          </el-form-item>

          <el-form-item
            label="数据集:"
            label-width="80px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索文件名" v-model="form.files_name" />
          </el-form-item>

          <el-form-item
            label="文件名:"
            label-width="80px"
            style="margin-bottom: 0.5rem"
          >
            <el-input placeholder="搜索文件名" v-model="form.file_name" />
          </el-form-item>

          <el-form-item label-width="60px" style="margin-bottom: 0.5rem">
            <el-button @click="(form.page = 1), dataLoad()">搜索</el-button>
          </el-form-item>
        </el-form-item>
      </el-form>

      <div class="button-group">
        <div>
          <el-button type="danger" @click="batch_del_fun">删除选中</el-button>
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

        <el-table-column-plus prop="model" label="模型" />
        <el-table-column-plus prop="files_name" label="数据集" />
        <el-table-column-plus prop="file_name" label="文件名" />

        <el-table-column-plus prop="slice_count" label="范围" />


        <el-table-column-plus prop="level" label="检测后图片">
          <template #default="scope">
            <img
              v-if="scope.row.mid_handle"
              :src="detectionImgGet + scope.row.mid_handle"
              alt="图片"
              class="img-show"
            />
          </template>
        </el-table-column-plus>

        <el-table-column-plus prop="CreatedAt" label="添加时间">
          <template #default="scope">
            {{ formatTime(scope.row.CreatedAt) }}
          </template>
        </el-table-column-plus>
        <el-table-column-plus label="操作" width="200">
          <template #default="scope">
            <div style="display: flex">
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
  api_detection_list_get,
  api_detection_list_del,
  detectionImgGet,
} from "@/api/api";

const Router = useRouter();

const datas = reactive({
  total: 0,
  dataTable: [],
  select: [],
  level: localStorage.getItem("level"),
});

const form = reactive({
  page: 1,
  pagesize: 10,
  username: "",
  file_name: "",
  created_at: [],
  created_at_start: "",
  created_at_end: "",
});

const handleSelectionChange = (eve) => {
  datas.select = eve;
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
      api_detection_list_del(dic).then((res) => {
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
  api_detection_list_get(form).then((res) => {
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

.img-show {
  max-width: 8rem;
  max-height: 8rem;
}
</style>
