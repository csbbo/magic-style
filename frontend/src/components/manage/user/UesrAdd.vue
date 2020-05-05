<template>
    <div class="useradd">

    <div class="form row">
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

        <div class=" select input-field col s12">
            <select id="select">
                <option value="normal_user">普通用户</option>
                <option value="general_manager">管理员</option>
            </select>
            <label>用户类型</label>
        </div>

    </form>

    <span class="error" v-if="errMessage != ''">
        <i class="material-icons">warning</i>{{errMessage}}
    </span>

    <span class="error success" v-if="successMessage != ''">
        <i class="material-icons">warning</i>{{successMessage}}
    </span>

    <button @click="addUser" class="btn-confir waves-effect waves-light btn">确认</button>
    <button @click="reset" class="waves-effect waves-light btn">重置</button>
    </div>
    </div>
</template>

<script>
    import {AddUserAPI} from "../../../api";
    window.$ = window.jQuery = require('jquery');
    export default {
        name: "UesrAdd",
        data() {
            return {
                username: '',
                phone: '',
                email: '',
                remark: '',
                password: 'ms000000',

                errMessage: '',
                successMessage: '',
            }
        },
        mounted() {
            $('select').formSelect();
        },
        created() {
            this.username = 'MS' + Math.ceil(Math.random()*100000);
        },
        methods: {
            reset() {
                this.username = 'MS' + Math.ceil(Math.random()*100000);
                this.phone = ''
                this.email = ''
                this.remark = ''
                this.password = 'ms000000'
                this.errMessage = ''
                this.successMessage = ''
            },
            addUser() {
                this.successMessage = ''
                const options = $("#select option:selected")
                const user_type = options.val()
                if ( this.username === '') {
                    this.errMessage = '用户名不能为空'
                    return
                }
                if ( this.password === '') {
                    this.errMessage = '密码不能为空'
                    return
                }
                const data = {
                    'username': this.username,
                    'phone_number': this.phone,
                    'user_type': user_type,
                    'email': this.email,
                    'remark': this.remark,
                    'password': this.password,
                }

                if (this.phone === '') {
                  delete data['phone_number']
                }
                if (this.email === '') {
                  delete data['email']
                }
                if (this.remark === '') {
                  delete data['remark']
                }
                AddUserAPI(data).then(resp => {
                    if (resp.err === null) {
                        this.errMessage = ''
                        this.successMessage = '用户创建成功'
                        this.username = 'MS' + Math.ceil(Math.random()*100000);
                        this.password = 'ms000000'
                    } else {
                        this.errMessage = resp.msg
                    }
                })
            }
        }
    }
</script>

<style scoped>
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