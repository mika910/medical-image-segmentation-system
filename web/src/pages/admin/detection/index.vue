<template>
  <div class="detection-main">
    <div class="img-div">
      <div class="up-img select-div">
        <div>
          <div class="title">选择模型：</div>
          <div>
            <el-select
              v-model="form.model"
              placeholder="请选择"
              @change="
                () => {
                  form.files_name = '';
                  form.file_name = '';
                }
              "
            >
              <el-option
                v-for="(key, val) in datas.selectMap"
                :key="val"
                :label="val"
                :value="val"
              />
            </el-select>
          </div>
        </div>
        <div>
          <div class="title">选择数据集</div>
          <div>
            <el-select
              v-model="form.files_name"
              placeholder="请选择"
              @change="
                () => {
                  form.file_name = '';
                }
              "
            >
              <el-option
                v-if="form.model != ''"
                v-for="(key, val) in datas.selectMap[form.model]"
                :key="val"
                :label="val"
                :value="val"
              />
            </el-select>
          </div>
        </div>
        <div>
          <div class="title">选择文件</div>
          <div>
            <el-select v-model="form.file_name" placeholder="请选择">
              <el-option
                v-if="form.model != '' && form.files_name != ''"
                v-for="item in datas.selectMap[form.model][form.files_name]"
                :key="item.file"
                :label="`${item.file} 范围:${item.count-1}`"
                :value="item.file"
              />
            </el-select>
          </div>
        </div>
        <div>
          <div class="title">切片范围</div>
          <div>
            <el-input-number v-model="form.slice_count" :min="0" />
          </div>
        </div>
      </div>
    </div>
    <div>
      <el-button @click="detection" type="primary">进行检测</el-button>
    </div>
    <div class="img-div">
      <div class="img-show-div">
        <img
          v-if="form.mid_handle"
          :src="detectionImgGet + form.mid_handle"
          ref="handleImgRef"
          class="img-show-css"
          alt="图片"
        />
      </div>

      <div class="up-img">
        <el-button @click="imgSave">保存到本地</el-button>
      </div>
    </div>
  </div>
</template>
<script setup>
import {
  api_detection_model_list_get,
  api_detection_post,
  detectionImgGet,
} from "@/api/api";
import { ElMessage, ElMessageBox } from "element-plus";
import { reactive, ref, onActivated, onMounted } from "vue";

const handleImgRef = ref(null);

const datas = reactive({
  selectMap: {},
});

const form = reactive({
  model: "",
  files_name: "",
  file_name: "",
  slice_count: "",
});

//检测图片
const detection = () => {
  api_detection_post(form).then((res) => {
    if (res.data.code === 200) {
      ElMessage({
        message: res.data.msg,
        type: "success",
      });

      form.mid_handle = res.data.data;
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};

//保存图片到本地
const imgSave = () => {
  let url = detectionImgGet + form.mid_handle + "&mode=down";
  const link = document.createElement("a");

  link.href = url;
  link.target = "_blank";
  link.click();
};

const dataLoad = () => {
  api_detection_model_list_get().then((res) => {
    if (res.data.code === 200) {
      datas.selectMap = res.data.data;
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};
onActivated(() => {
  dataLoad();
});

onMounted(() => {
  dataLoad();
});
</script>
<style scoped>
.detection-main {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  height: 100%;
  flex-wrap: wrap;

  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.img-div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.up-img {
  margin-top: 2rem;
}

.img-show-div {
  min-height: 30rem;
  max-height: 30rem;
  min-width: 30rem;
  max-width: 30rem;
  border: 2px solid rgb(204, 204, 204);
  border-radius: 0.2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
}
.img-show-css {
  max-width: 30rem;
  max-height: 3 0rem;
}

.title {
  margin-bottom: 0.5rem;
  margin-top: 0.5rem;
}
</style>
