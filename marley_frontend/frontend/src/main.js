import './index.css'

import { createApp } from 'vue';
import router from './router';
import App from './App.vue';
import { initSocket } from './socket';

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
	resourcesPlugin,
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

if (isAIStudioPreview) {
	window.timezone = window.timezone || { system: 'UTC', user: 'UTC' }
	window.__MARLEY_AI_STUDIO_PREVIEW__ = true
}

let globalComponents = {
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

let app = createApp(App)
setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI)
app.use(router)
// app.use(resourcesPlugin)

for (let key in globalComponents) {
	app.component(key, globalComponents[key])
}

function mountApp(withSocket = true) {
	if (withSocket) {
		try {
			const socket = initSocket()
			app.config.globalProperties.$socket = socket
		} catch (error) {
			console.warn('Socket unavailable; continuing without realtime updates.', error)
		}
	}
	app.mount('#app')
}

if (import.meta.env.DEV && !isAIStudioPreview) {
	frappeRequest({ url: '/api/method/marley_frontend.www.healthcare.get_context_for_dev' }).then(
		(values) => {
			for (let key in values) {
				window[key] = values[key]
			}
			mountApp(true)
		},
	).catch((error) => {
		console.error('Unable to load Marley development context from Frappe.', error)
	})
} else if (isAIStudioPreview) {
	// Frontend-only mode for Google AI Studio. No Frappe server is expected.
	mountApp(false)
} else {
	mountApp(true)
}
