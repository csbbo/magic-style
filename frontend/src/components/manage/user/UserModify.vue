<template>
    <div class="useradd">

    <div class="form row">
        <div class="user-type">
            <span>{{usertype | formatUserType}}</span>
            <span>{{username}}</span>
        </div>
    <form class="col s12">
      <div class="row">
        <div class="input-field col s12">
            <span>用户名:</span>
          <input v-model="username" id="username" type="text" class="validate">
        </div>
      </div>

      <div class="row">
        <div class="input-field col s12">
            <span>手机号:</span>
          <input v-model="phone" id="phone" type="text" class="validate">
        </div>
      </div>

      <div class="row">
        <div class="input-field col s12">
            <span>邮箱:</span>
          <input v-model="email" id="email" type="text" class="validate">
        </div>
      </div>

      <div class="row">
        <div class="input-field col s12">
            <span>remark:</span>
          <input v-model="remark" id="remark" type="text" class="validate">
        </div>
      </div>

      <div class="row">
        <div class="input-field col s12">
            <span>密码:</span>
          <input v-model="password" id="password" type="text" class="validate">
        </div>
      </div>

<!--        <div class=" select input-field col s12">-->
<!--            <select id="select">-->
<!--                <option value="normal_user">普通用户</option>-->
<!--                <option value="general_manager">管理员</option>-->
<!--            </select>-->
<!--            <label>用户类型</label>-->
<!--        </div>-->

    </form>

    <span class="error" v-if="errMessage != ''">
        <i class="material-icons">warning</i>{{errMessage}}
    </span>

    <span class="error success" v-if="successMessage != ''">
        <i class="material-icons">warning</i>{{successMessage}}
    </span>

    <button @click="updateUser" class="btn-confir waves-effect waves-light btn">确认</button>
    <button @click="reset" class="waves-effect waves-light btn">清空</button>
    </div>
    </div>
</template>

<script>
    import {GetUserAPI ,UpdateUserAPI} from "../../../api";
    window.$ = window.jQuery = require('jquery');
    export default {
        name: "UesrModify",
        data() {
            return {
                selected: 'normal_user',
                user: {},

                username: '',
                phone: '',
                email: '',
                remark: '',
                password: '',
                x: '',

                errMessage: '',
                successMessage: '',
            }
        },
        created() {
            GetUserAPI({'user_id': this.$route.query.id}).then(resp => {
                const data = resp.data
                this.username = data.username
                this.phone = data.phone_number
                this.email = data.email
                this.remark = data.remark
                this.usertype = data.user_type
            })
        },
        methods: {
            reset() {
                this.username = ''
                this.phone = ''
                this.email = ''
                this.remark = ''
                this.password = ''
                this.errMessage = ''
                this.successMessage = ''
            },
            updateUser() {
                this.successMessage = ''
                if ( this.username === '') {
                    this.errMessage = '用户名不能为空'
                    return
                }
                const data = {
                    'id': this.$route.query.id,
                    'username': this.username,
                    'phone_number': this.phone,
                    'user_type': this.selected,
                    'email': this.email,
                    'remark': this.remark,
                    'password': this.password,
                }

                if ( this.password === '') {
                    delete data['password']
                }
                if (this.phone === '' || this.phone === null) {
                  delete data['phone_number']
                }
                if (this.email === '' || this.email === null) {
                  delete data['email']
                }
                if (this.remark === '' || this.remark === null) {
                  delete data['remark']
                }
                UpdateUserAPI(data).then(resp => {
                    if (resp.err === null) {
                        this.errMessage = ''
                        this.usertype = this.selected
                        this.successMessage = '用户修改成功'
                    } else {
                        this.errMessage = resp.msg
                    }
                })
            }
        },
        filters: {
            formatUserType(userType) {
                if (userType === 'normal_user') {
                    return '用户'
                }
                if (userType === 'general_manager') {
                    return '管理员'
                }
                return '未知'
            }
        }
    }
</script>

<style scoped>
    .user-type {
        margin: 0 10px;
        background-color: #f5f5f5;
        padding: 20px;
        text-align: center;
        border-radius: 5px;
    }
    .user-type span {
        margin: 0 10px;
        color: #757575;
    }
    .form {
        width: 40%;
        margin-left: 20px;
        padding: 20px;
    }
    .form button {
        float: right;
        margin-top: 40px;
    }
    .form .btn-confir {
        margin-left: 20px;
        margin-right: 11px;
    }
    .form input {
        color: #8c939d;
    }
    .form .select {
        padding: 0;
    }

    .error {
        margin: 0 10px;
        padding: 8px;
        border: 1px solid #ef9a9a;
        color: #ce3737;
        border-radius: 3px;
    }
    .error i{
        font-size: 23px;
        vertical-align: bottom;
        margin-right: 5px;
    }
    .success {
        margin: 0 10px;
        padding: 8px;
        border: 1px solid #00bfa5;
        color: #00695c;
        border-radius: 3px;
    }
    .success i{
        font-size: 23px;
        vertical-align: bottom;
        margin-right: 5px;
    }
</style>