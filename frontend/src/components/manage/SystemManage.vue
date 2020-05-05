<template>
    <div class="system">
        <div class="resource">
            <span class="head">资源消耗</span>
            <hr>
            <div class="content">
                <div class="cpu">
                    Cpu使用率:{{cpuUsage}}
                </div>
                <div class="memory">
                    内存使用率:{{memoreyUsage}}
                </div>
                <div class="disk">
                    磁盘总量:{{diskTotal}}
                    磁盘使用率:{{diskUsage}}
                </div>
            </div>
        </div>

        <div class="info">
            <span class="head">数据汇总</span>
            <hr>
            <div class="content">
                <div class="admin">
                    管理员{{adminCount}}人
                </div>
                <div class="nomore-user">
                    普通用户{{nomorUserCount}}人
                </div>
                <div class="style-image">
                    风格图片{{styleImageCount}}张
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    import {GetPlatformInfo} from '../../api'
    export default {
        name: "SystemManage",
        data() {
            return {
                cpuUsage: 0,
                memoreyUsage: 0,
                diskTotal: 0,
                diskUsage: 0,
                adminCount: 0,
                nomorUserCount: 0,
                styleImageCount: 0,
            }
        },
        created() {
            GetPlatformInfo().then(resp => {
                if (resp.err === null) {
                    const data = resp.data

                    this.cpuUsage = data.cpu_usage
                    this.memoreyUsage = data.memory_usage
                    this.diskTotal = data.disk_total
                    this.adminCount = data.general_manager_count
                    this.nomorUserCount = data.normal_user_count
                    this.styleImageCount = data.style_image_count

                    let diskusage = (data.disk_use / data.disk_total) * 100
                    this.diskUsage = diskusage.toFixed(2)
                }
            })
        }
    }
</script>

<style scoped>
    .system {
        margin: 40px;
    }
    .head {
        border: 2px solid #ff9800;
        padding: 5px 10px 4px 2px;
        border-left: none;
        border-bottom: none;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 4px;
        color: #8c939d;
    }
    hr {
        margin: 0 0 8px;
        border: 1px solid #ff9800;
    }
    .resource .content {
        padding: 20px;
        display: flex;
    }
    .resource .content div{
        padding: 20px;
        margin: 10px;
        border: 1px solid gray;
        border-radius: 5px;
        background-color: #00695c;
    }
    .info .content {
        padding: 20px;
        display: flex;
    }
    .info .content div{
        padding: 20px;
        margin: 10px;
        border: 1px solid gray;
        border-radius: 5px;
        background-color: #00695c;
    }
</style>