<template>
    <div class="home">
    <nav>
      <div class="nav-wrapper">
        <a href="/" class="brand-logo">Magic Style</a>
        <ul id="nav-mobile" class="right hide-on-med-and-down">
          <li><a class="modal-trigger" href="#loginModal">登录</a></li>
          <li><a class="modal-trigger" href="#registModal">注册</a></li>
        </ul>
      </div>
    </nav>

    <!-- 登录 Modal Structure -->
    <div id="loginModal" class="modal">
      <div class="modal-content">
        <h4>登录</h4>
        <div class="error" v-if="loginErrShow"><i class="material-icons">warning</i>{{loginErr}}</div>
        <div class="row">
          <form class="col s12">
            <div class="row">
              <div class="input-field col s12">
                <input v-model="loginName" id="loginName" type="text" class="validate">
                <label for="loginName">用户名/手机号/邮箱</label>
              </div>
            </div>

            <div class="row">
              <div class="input-field col s12">
                <input v-model="password" id="password" type="password" class="validate">
                <label for="password">密码</label>
              </div>
            </div>
          </form>
          <button @click="login" class="waves-effect waves-light btn">登录</button>
        </div>
      </div>
      <div class="modal-footer">
        <a href="#!" class="modal-close waves-effect waves-green btn-flat">关闭</a>
      </div>
    </div>

      <!-- 注册 Modal Structure -->
    <div id="registModal" class="modal">
      <div class="modal-content">
        <h4>注册</h4>
        <div class="row">
          <form class="col s12">
            <div class="row">
              <div class="input-field col s12">
                <input v-model="username" id="username" type="text" class="validate">
                <label for="username">用户名</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <input v-model="phoneNumber" id="phoneNumber" type="text" class="validate">
                <label for="phoneNumber">手机号</label>
              </div>
            </div>

            <div class="row">
              <div class="input-field col s12">
                <input v-model="password1" id="password1" type="password" class="validate">
                <label v-model="password1" for="password1">密码</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <input v-model="password2" id="password2" type="password" class="validate">
                <label for="password2">确认密码</label>
              </div>
            </div>
            <div class="row">
              <div class="input-field col s12">
                <input v-model="email" id="email" type="email" class="validate">
                <label for="email">邮箱(非必填)</label>
              </div>
            </div>
          </form>
          <button @click="regist" class="waves-effect waves-light btn">注册</button>
        </div>
        <div class="error" v-if="registErrShow"><i class="material-icons">warning</i>{{registErr}}</div>
      </div>
      <div class="modal-footer">
        <a href="#!" class="modal-close waves-effect waves-green btn-flat">关闭</a>
      </div>
    </div>

    <div class="carousel carousel-slider center">
      <div class="carousel-item red white-text" href="#one!">
        <h2>First Panel</h2>
        <p class="white-text">This is your first panel</p>
      </div>
      <div class="carousel-item amber white-text" href="#two!">
        <h2>Second Panel</h2>
        <p class="white-text">This is your second panel</p>
      </div>
      <div class="carousel-item green white-text" href="#three!">
        <h2>Third Panel</h2>
        <p class="white-text">This is your third panel</p>
      </div>
      <div class="carousel-item blue white-text" href="#four!">
        <h2>Fourth Panel</h2>
        <p class="white-text">This is your fourth panel</p>
      </div>
    </div>

    <div class="demoImg">
      <img src="../assets/20200216-TaikanCrane.jpg">
    </div>

    <footer class="page-footer">
      <div class="container">
        <div class="row">
          <div class="col l6 s12">
            <h5 class="white-text">Footer Content</h5>
            <p class="grey-text text-lighten-4">You can use rows and columns here to organize your footer content.</p>
          </div>
          <div class="col l4 offset-l2 s12">
            <h5 class="white-text">Links</h5>
            <ul>
              <li><a class="grey-text text-lighten-3" href="#!">Link 1</a></li>
              <li><a class="grey-text text-lighten-3" href="#!">Link 2</a></li>
              <li><a class="grey-text text-lighten-3" href="#!">Link 3</a></li>
              <li><a class="grey-text text-lighten-3" href="#!">Link 4</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="footer-copyright">
        <div class="container">
        © 2020 Copyright
        <a class="grey-text text-lighten-4 right" href="#!">桂ICP备17011922号</a>
        </div>
      </div>
    </footer>

    </div>
</template>

<script>
  import {LoginAPI, RegistAPI} from "../api";
  window.$ = window.jQuery = require('jquery');
  import ajax from 'axios'
  import * as Cookies from 'js-cookie'
  export default {
    name: "Home",
    data() {
      return {
        loginErr: '',
        loginErrShow: false,
        registErr: '',
        registErrShow: false,

        loginName: '',
        password: '',
        username: '',
        phoneNumber: '',
        password1: '',
        password2: '',
        email: '',
      }
    },
    mounted() {
      $('.modal').modal();
      $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
      });
    },
    methods: {
      login(){
        if (this.loginName === '') {
          this.loginErr = "账号不能为空"
          this.loginErrShow = true
          return
        }
        if (this.password === '') {
          this.loginErr = "密码不能为空"
          this.loginErrShow = true
          return
        }
        const data = {
          'loginname': this.loginName,
          'password': this.password
        }
        this.updateCsrfToken()
        LoginAPI(data).then(resp => {
          this.$router.push('/transfer')
          if (resp.err === null){
            this.updateCsrfToken()
            this.$router.push('/transfer')
            // alert('login success!')
          } else {
            this.loginErr = resp.msg
            this.loginErrShow = true
          }
        })
      },
      regist(){
        if (this.username === '') {
          this.registErr = '用户名不能为空'
          this.registErrShow = true
          return
        }
        if (this.phoneNumber === '') {
          this.registErr = '手机号不能为空'
          this.registErrShow = true
          return
        }
        if (this.phoneNumber.length !== 11) {
          this.registErr = '请输入正确的手机号'
          this.registErrShow = true
          return
        }
        if (this.password1 === '' || this.password2 === '') {
          this.registErr = '密码不能为空'
          this.registErrShow = true
          return
        }
        if (this.password1 !== this.password2) {
          this.registErr = '两次密码不一致'
          this.registErrShow = true
          return
        }
        const data = {
          'username': this.username,
          'phone_number': this.phoneNumber,
          'password': this.password1,
          'email': this.email
        }
        if (this.email === '') {
          delete data['email']
        }
        this.updateCsrfToken()
        RegistAPI(data).then(resp => {
          if (resp.err === null){
            this.updateCsrfToken()
            this.$router.push('/transfer')
            // alert('regist success!')
          } else {
            this.registErr = resp.msg
            this.registErrShow = true
          }
        })
      },
      updateCsrfToken() {
        ajax.get('/api/CSRFTokenAPI').then(() => {
          ajax.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken')
        })
      }
    }
  }
</script>

<style scoped>
  .modal{
    padding: 0 26px;
  }
  .modal h4{
    text-align: center;
  }
  .modal button {
    margin-left: 10px;
  }
  .modal .error {
    margin: 0 10px;
    padding: 8px;
    border: 1px solid #ef9a9a;
    color: #ce3737;
    border-radius: 3px;
  }
  .modal .error i{
    font-size: 23px;
    vertical-align: bottom;
    margin-right: 5px;
  }
  .carousel {
    height: fit-content;
  }
  .demoImg img {
    width: 100%;
  }
</style>