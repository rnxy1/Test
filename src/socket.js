import { io } from 'socket.io-client'
import { getCachedListResource, getCachedResource } from 'frappe-ui'

const isPreview = import.meta.env.VITE_AI_STUDIO_PREVIEW === '1'

function createNoopSocket() {
  return {
    on() {},
    off() {},
    emit() {},
    disconnect() {},
    connected: false,
  }
}

export function initSocket() {
  if (isPreview) return createNoopSocket()

  const host = window.location.hostname
  const siteName = window.site_name || window.origin
  const configuredPort = import.meta.env.VITE_SOCKETIO_PORT
  const port = configuredPort ? `:${configuredPort}` : ''
  const protocol = window.location.protocol === 'https:' ? 'https' : 'http'
  const url = `${protocol}://${host}${port}/${siteName}`

  const socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
  })

  socket.on('refetch_resource', (data) => {
    if (!data?.cache_key) return
    const resource =
      getCachedResource(data.cache_key) ||
      getCachedListResource(data.cache_key)
    resource?.reload?.()
  })

  return socket
}
