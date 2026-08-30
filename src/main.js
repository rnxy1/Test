import './index.css'

import { createApp } from 'vue'
import {
  FrappeUI,
  Button,
  Input,
  TextInput,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  setConfig,
  frappeRequest,
  FeatherIcon,
  Avatar,
  Tooltip,
  ListView,
  ListHeader,
  ListHeaderItem,
  ListRows,
  ListRow,
  ListRowItem,
  ListSelectBanner,
  ListFooter,
} from 'frappe-ui'

const isAIStudioPreview = import.meta.env.VITE_AI_STUDIO_PREVIEW === '1'

const globalComponents = {
  Button,
  Input,
  TextInput,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  FeatherIcon,
  Avatar,
  Tooltip,
  ListView,
  ListHeader,
  ListHeaderItem,
  ListRows,
  ListRow,
  ListRowItem,
  ListSelectBanner,
  ListFooter,
}

async function bootstrap() {
  if (isAIStudioPreview) {
    const { mockResourceFetcher, seedPreviewGlobals } = await import('./demo/mockApi')
    seedPreviewGlobals()
    // Several Marley modules construct Frappe resources during import, so the
    // demo resource fetcher must be configured before App/router are imported.
    setConfig('resourceFetcher', mockResourceFetcher)
  } else {
    setConfig('resourceFetcher', frappeRequest)
  }

  const [{ default: router }, { default: App }] = await Promise.all([
    import('./router'),
    import('./App.vue'),
  ])

  const app = createApp(App)
  app.use(FrappeUI)
  app.use(router)

  for (const key in globalComponents) {
    app.component(key, globalComponents[key])
  }

  const mountApp = async (withSocket = true) => {
    if (withSocket) {
      try {
        const { initSocket } = await import('./socket')
        const socket = initSocket()
        app.config.globalProperties.$socket = socket
      } catch (error) {
        console.warn('Socket unavailable; continuing without realtime updates.', error)
      }
    }
    app.mount('#app')
  }

  if (import.meta.env.DEV && !isAIStudioPreview) {
    try {
      const values = await frappeRequest({
        url: '/api/method/marley_frontend.www.healthcare.get_context_for_dev',
      })
      for (const key in values) {
        window[key] = values[key]
      }
      await mountApp(true)
    } catch (error) {
      console.error('Unable to load Marley development context from Frappe.', error)
    }
  } else {
    await mountApp(!isAIStudioPreview)
  }
}

bootstrap().catch((error) => {
  console.error('Unable to start Marley Frontend.', error)
  const target = document.getElementById('app')
  if (target) {
    target.innerHTML = `
      <div style="font-family:system-ui;padding:32px;max-width:720px;margin:0 auto">
        <h2>Marley Frontend could not start</h2>
        <p>${String(error?.message || error)}</p>
      </div>
    `
  }
})
