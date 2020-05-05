import Vue from 'vue'
import VueRouter from 'vue-router'
import axios from 'axios'
import Home from './components/Home'

import Navbar from "./components/Navbar";
import Transfer from "./components/Transfer";
import Manage from "./components/Manage";
import Profile from "./components/Profile";

import UserManage from "./components/manage/UserManage";
import UesrAdd from "./components/manage/user/UesrAdd";
import UserModify from "./components/manage/user/UserModify";
import StyleImage from "./components/manage/StyleImage";
import SystemManage from "./components/manage/SystemManage";
import TrainingMode from "./components/manage/TrainingMode";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/nav',
        redirect: '/transfer',
        component: Navbar,
        children: [
            {
                path: '/transfer',
                component: Transfer,
                children: [

                ]
            },
            {
                path: '/profile',
                component: Profile
            },
            {
                path: '/manage',
                redirect: '/manage/user',
                component: Manage,
                children: [
                    {
                        path: '/manage/user',
                        component: UserManage
                    },
                    {
                        path: '/manage/user/add',
                        component: UesrAdd
                    },
                    {
                        path: '/manage/user/modify',
                        component: UserModify
                    },
                    {
                        path: '/manage/styleimage',
                        component: StyleImage
                    },
                    {
                        path: '/manage/system',
                        component: SystemManage
                    },
                    {
                        path: '/manage/trainmode',
                        component: TrainingMode
                    },
                ]
            }
        ]
    },
    { path: '*', redirect: '/' },
]

const router = new VueRouter({
    routes,
    mode: 'history'
})

router.beforeEach((to, from, next) => {
    if (to.path === '/') {
        next()
    } else {
        axios('/api/LoginStatusAPI').then(resp => {
            if (resp.data.err === null) {
                next()
            } else {
                next({ path: '/' })
            }
        })
            .catch(() => {
                next({
                    path: '/',
                })
            })
    }
})

export default router