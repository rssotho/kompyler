import store from '@/store'

export default {
  install(Vue) {
    // Global loading method
    Vue.prototype.$loading = {
      show(message = '') {
        store.dispatch('loading/show', message)
      },
      hide() {
        store.dispatch('loading/hide')
      },
      isLoading() {
        return store.state.loading.isLoading
      }
    }
  }
}
