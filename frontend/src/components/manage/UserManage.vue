<template>
    <div class="usermanage">
        <div class="head">
            <router-link to="/manage/user/add" class="btn-floating btn-small waves-effect waves-light red"><i class="material-icons">add</i></router-link>
            <a @click="getUsers('general_manager')" class="waves-effect waves-light btn-small">管理员</a>
            <a @click="getUsers('normal_user')" class="waves-effect waves-light btn-small">用户</a>
            <a @click="getUsers('all')" class="waves-effect waves-light btn-small">全部</a>
            <a v-if="choiseIds.length != 0" @click="deleteMultiUser" class="waves-effect waves-light btn-small">删除</a>
        </div>

        <div class="content">
            <table class="responsive-table">
                <thead>
                  <tr>
                      <p>
                      <label>
                        <input id="checkAll" @click="choiseItemAll" type="checkbox" class="filled-in"/>
                        <span></span>
                      </label>
                      </p>

                      <th>用户名</th>
                      <th>手机</th>
                      <th>邮箱</th>
                      <th>remark</th>
                      <th>最近登录</th>
                      <th>创建时间</th>
                      <th>修改时间</th>
                      <th>用户类型</th>
                      <th>操作</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-for="user in users" :key="user">

                    <p>
                    <label>
                        <input @click="choiseItem(user.id)" v-model="user.state" type="checkbox" /><span></span>
                    </label>
                    </p>

                    <td>{{user.username}}</td>
                    <td>{{user.phone_number}}</td>
                    <td>{{user.email}}</td>
                    <td>{{user.remark}}</td>
                    <td>{{user.last_login_time | formatDate}}</td>
                    <td>{{user.create_time | formatDate}}</td>
                    <td>{{user.last_update_time | formatDate}}</td>
                    <td>{{user.user_type | formatUserType}}</td>

                    <td>
                        <a @click="modifyUser(user.id)"><i class="material-icons edit">edit</i></a>
                        <i @click="deleteUser(user.id)" class="material-icons delete">delete</i>
                    </td>
                  </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    import {GetUserAPI, DeleteUserAPI} from '../../api'
    // import children from './user/UserModify'
    export default {
        name: "UserManage",
        data() {
            return {
                choiseIds: [],
                users: [],
            }
        },
        created() {
            this.getUsers('all')
        },
        methods: {
            getUsers(userType) {
                const data = {
                    'user_type': userType,
                }
                if (userType === 'all') {
                    delete data['user_type']
                }
                GetUserAPI(data).then(resp => {
                    this.users = resp.data
                })
            },
            deleteUser(user_id){
                if (!confirm('您确定要将该用户从数据库中删除?')) {
                    return
                }
                DeleteUserAPI({'user_ids': [user_id]}).then(resp => {
                    if (resp.err === null) {
                        for (let i=0; i<this.users.length; i++) {
                            if (this.users[i].id === user_id) {
                                this.users.splice(i, 1)
                            }
                        }
                        this.choiseIds = []
                    }
                })
            },
            deleteMultiUser() {
                if (!confirm('您确定要从数据库中删除选定的用户?')) {
                    return
                }
                DeleteUserAPI({'user_ids': this.choiseIds}).then(resp => {
                    if (resp.err === null) {
                        for (let i=0; i<this.users.length; i++) {
                            for (let j=0; j<this.choiseIds.length; j++) {
                                if (this.users[i].id === this.choiseIds[j]) {
                                    this.users.splice(i, 1)
                                }
                            }
                        }
                        this.choiseIds = []
                    }
                })
            },
            choiseItem(user_id) {
                const index = this.choiseIds.indexOf(user_id)
                if (index === -1) {
                    this.choiseIds.push(user_id)
                } else {
                    this.choiseIds.splice(index, 1)
                }

                const checkAllItem = document.getElementById('checkAll')
                if (this.choiseIds.length === this.users.length) {
                    checkAllItem.checked = true
                } else {
                    checkAllItem.checked = false
                }
            },
            choiseItemAll() {
                const items = document.getElementsByTagName('input')
                if (this.choiseIds.length < this.users.length) {
                    for (let i=0; i<items.length; i++) {
                        items[i].checked = true
                    }

                    for (let i=0; i<this.users.length; i++) {
                        let userId = this.users[i].id
                        if (this.choiseIds.indexOf(userId) === -1) {
                            this.choiseIds.push(userId)
                        }
                    }
                } else {
                    this.choiseIds = []
                    for (let i=0; i<items.length; i++) {
                        items[i].checked = false
                    }
                }

            },
            modifyUser(userId) {
                this.$router.push({path: '/manage/user/modify', query: {id: userId}})
            }
        },
        filters: {
            formatDate(time) {
                if (time === null) {
                    return null
                }
                const date = new Date(time*1000); //这里time是10位可能js解析时间戳为13位
                const y = date.getFullYear()
                const m = date.getMonth()
                const d = date.getDate()
                const ho = date.getHours()
                const mi = date.getMinutes()
                const se = date.getSeconds()
                return y+"."+m+"."+d+" "+ho+":"+mi+":"+se
            },
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
    .head {
        height: 70px;
        background-color: #FFFFFF;
    }
    .head a {
        float: right;
        margin-right: 20px;
    }
    .head .btn-small {
        margin-top: 17px;
    }
    .head .btn-floating {
        margin-top: 17px;
    }
    .content {
        border-top: 1px solid #e0e0e0;
        padding: 0 20px;
    }
    .content tbody i {
        background-color: #f5f5f5;
        padding: 5px;
        border-radius: 100%;
        color: #8c939d;
    }
    .content .edit{
        margin-right: 20px;
    }
    .content tbody i:hover{
        color: #616161;
    }
    .content table p {
        margin-top: 22px;
        margin-bottom: 8px;
    }
</style>