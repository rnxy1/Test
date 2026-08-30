import { computed, reactive } from 'vue'
import { createResource } from 'frappe-ui'
import { users } from './users'
import router from '@/router'

const isAIStudioPreview = import.meta.env.VITE_AI_STUDIO_PREVIEW === '1'

export function sessionUser() {
  if (isAIStudioPreview) {
    return 'demo@marley.local'
  }

  let cookies = new URLSearchParams(document.cookie.split('; ').join('&'))
  let _sessionUser = cookies.get('user_id')
  if (_sessionUser === 'Guest') {
    _sessionUser = null
  }

  return _sessionUser
}

export let session = reactive({
  login: createResource({
    url: 'login',
    makeParams({ email, password }) {
      return {
        usr: email,
        pwd: password,
      }
    },
    onSuccess(data) {
      users.reload()
      session.user = sessionUser()
      session.login.reset()
      router.replace(data.default_route || '/')
    },
  }),
  logout: createResource({
    url: 'logout',
    onSuccess() {
      users.reset()
      session.user = null
      window.location.href = '/login?redirect-to=/healthcare'
    },
  }),
  user: sessionUser(),
  isLoggedIn: computed(() => !!session.user),
})
