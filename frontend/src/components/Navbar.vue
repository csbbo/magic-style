<template>
    <div class="navbar">
    <nav>
    <div class="nav-wrapper">
      <a href="/transfer" class="logo brand-logo left">Magic</a>
      <ul id="nav-mobile" class="tab left hide-on-med-and-down">
        <li><a href="/transfer">风格迁移</a></li>
        <li v-if="userType === 'super_admin'"><a href="/manage">管理</a></li>
      </ul>

      <ul id="nav-mobile-right" class="right hide-on-med-and-down">
        <li><a class='dropdown-trigger' href='#' data-target='dropdown1'><i class="material-icons">account_circle</i></a></li>
      </ul>
    </div>
    </nav>

      <!-- Dropdown Structure -->
    <ul id='dropdown1' class='dropdown-content'>
    <li><router-link to="/profile">个人中心</router-link></li>
    <li><a @click="logout">注销</a></li>
    </ul>

    <router-view/>
    </div>
</template>

<script>
    window.$ = window.jQuery = require('jquery');
    import {LogoutAPI, UserIdentityAPI} from "../api";
    export default {
        name: "Nav",
        data() {
            return {
                'userType': '',
            }
        },
        mounted() {
            $('.dropdown-trigger').dropdown();
        },
        created() {
            this.getuser();
        },
        methods: {
            logout() {
                LogoutAPI().then(resp => {
                    if (resp.err === null) {
                        this.$router.push('/')
                    }
                })
            },
            getuser() {
                UserIdentityAPI().then(resp => {
                    this.userType = resp.data.user_type
                })
            }
        }
    }
</script>

<style scoped>
    .navbar .right li {
        margin-right: 20px;
    }
    .navbar .dropdown-content {
        position: fixed;
        top: -62px;
        border-radius: 5px;
    }
    .navbar .logo {
        margin-left: 10px;
    }
    .navbar .tab {
        margin-left: 160px;
    }

</style>