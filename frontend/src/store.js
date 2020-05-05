import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    modifyUserId: 0
  },
  mutations: {
    setModifyUserId (state, userId) {
      state.modifyUserId = userId
    }
  }
})