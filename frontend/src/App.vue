<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-left">
        <h1 class="logo">🏠 楼邦建材业绩报表</h1>
      </div>
      <el-menu
        :default-active="activeMenu"
        mode="horizontal"
        router
        class="nav-menu"
      >
        <el-menu-item index="/entry">
          <el-icon><Edit /></el-icon>
          <span>数据录入</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><DataAnalysis /></el-icon>
          <span>报表</span>
        </el-menu-item>
        <el-menu-item index="/salespersons">
          <el-icon><User /></el-icon>
          <span>业务员管理</span>
        </el-menu-item>
        <el-menu-item index="/member">
          <el-icon><UserFilled /></el-icon>
          <span>会员业绩汇总</span>
        </el-menu-item>
      </el-menu>
      <div class="header-right">
        <el-button type="primary" @click="refreshPage" circle>
          <el-icon><Refresh /></el-icon>
        </el-button>
      </div>
    </el-header>
    <el-main class="app-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)

const refreshPage = () => {
  window.location.reload()
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  background-color: #f5f7fa;
}

.app-container {
  min-height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #1a73e8, #4285f4);
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.header-left .logo {
  color: white;
  font-size: 20px;
  font-weight: bold;
  white-space: nowrap;
}

.nav-menu {
  background: transparent;
  border: none;
  flex: 1;
  justify-content: center;
}

.nav-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.85) !important;
  border-bottom: none !important;
  font-size: 15px;
}

.nav-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.15) !important;
  color: white !important;
}

.nav-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.25) !important;
  color: white !important;
}

.header-right .el-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.header-right .el-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.app-main {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style>
