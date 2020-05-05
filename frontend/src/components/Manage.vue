<template>
    <div class="manage">
        <div class="sidebar">
            <div class="head">管理</div>
            <div class="collection">
                <router-link to="/manage/user" class="collection-item">用户管理</router-link>
                <router-link to="/manage/trainmode" class="collection-item">模型训练</router-link>
                <router-link to="/manage/system" class="collection-item">系统管理</router-link>
                <router-link to="/manage/styleimage" class="collection-item">风格图片管理</router-link>
            </div>
        </div>
        <div class="manage-content"><router-view/></div>
    </div>
</template>

<script>
    export default {
        name: "Manage"
    }
</script>

<style scoped>
    .manage {
        display: flex;
        flex-direction: row;
    }
    .sidebar {
        width: 20%;
        border-right: 1px solid #e0e0e0;
    }
    .sidebar .head {
        height: 70px;
        background-color: #FFFFFF;
        padding: 23px;
        color: #e0e0e0;
    }
    .sidebar .collection {
        margin: 0;
        border-right: none;
        border-bottom: none;
        border-left: none;
    }
    .sidebar .collection .collection-item{
        height: 60px;
        text-align: right;
        padding-top: 20px;
        padding-right: 30px;
        border: none;
        color: #8c939d;
    }
    .manage-content {
        width: 80%;
    }

</style>