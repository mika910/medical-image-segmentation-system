// componentsPlugin.js

import MyImgUpdate from './all/ImgUpdata.vue';
import MyImgShow from './all/ImgShow.vue';


import ElTablePlus from './all/兼容表格组件/兼容移动端的表格.vue';
import ElTableColumnPlus from './all/兼容表格组件/el_table_column_plus.vue';
import devSwitch from './admin/device_switch.vue';

const componentsPlugin = {
  install: (app) => {
    app.component('my-imgup', MyImgUpdate); //图片上传
    app.component('my-img', MyImgShow); //图片显示
    app.component('el-table-plus', ElTablePlus); //移动端适配表格
    app.component('el-table-column-plus', ElTableColumnPlus); //移动端适配表格
    app.component('device-switch-button', devSwitch); //表格显示设备切换按钮
  },
};

export default componentsPlugin;