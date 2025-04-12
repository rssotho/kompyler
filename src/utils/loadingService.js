import store from '@/store'

export default {
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
