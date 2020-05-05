<template>
    <div class="training-model">
        <div class="status">模型状态:{{status}}</div>
        <a @click="traning_mode('stop')" class="waves-effect waves-light btn">停止</a>
        <a @click="traning_mode('start')" class="waves-effect waves-light btn">训练</a>
    </div>
</template>

<script>
    import {TrainingMode} from '../../api'
    export default {
        name: "TrainingMode",
        data() {
            return {
                status: '',
            }
        },
        created() {
            this.traning_mode('status')
        },
        methods: {
            traning_mode(operation) {
                TrainingMode({'operation': operation}).then(resp => {
                    if (resp.err === null) {
                        this.status = resp.data.status
                    }
                })
            }
        }
    }
</script>

<style scoped>
.training-model{
    margin: 20px;
}
.training-model a{
    float: right;
    margin: 5px;
}
.status{
    background-color: #8c939d;
    padding: 20px;
    border-radius: 5px;
}
</style>