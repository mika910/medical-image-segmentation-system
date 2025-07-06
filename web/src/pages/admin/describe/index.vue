<template>
  <div class="home-div">
    <div class="content">
      <p>医学图像分割平台简介</p>
      <br />

      <p class="cwp">
        本平台基于 Vue 前端框架 与 Django 后端框架 开发，致力于为研究人员和医疗从业者提供高效、直观的医学图像分割可视化与交互工具。
      </p>
    <br />
      <p  class="cwp">
        平台支持ACDC (Automated Cardiac Diagnosis Challenge) 和 Synapse (Multi-Atlas Abdomen Segmentation Challenge) 数据集的分割结果展示。用户可轻松上传医学图像，并借助预训练的深度学习模型实时生成高精度分割结果，为临床研究和医学影像分析提供有力支持。此外，平台鼓励用户上传并分享自定义医学图像数据集，推动数据共享与学术交流。界面简洁友好，操作流畅，适用于医学影像分析的初学者和专业人士。
      </p>
      <br />
      <p  class="cwp">欢迎体验本平台，探索医学图像分割的更多可能！</p>
    </div>
  </div>
</template>
<script setup></script>
<style scoped>
.home-div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-size: 1.5rem;
}

.content {
  width: 50rem;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.cwp{
  text-indent: 3rem; /* 缩进第一行 */
  min-width: 50rem;
  text-align: justify;
}

</style>
