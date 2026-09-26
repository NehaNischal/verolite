import {defineCliConfig} from 'sanity/cli'

export default defineCliConfig({
  api: {
    projectId: '5nckxq6b',
    dataset: 'production'
  },
  vite: (config) => ({
    ...config,
    base: '/studio/',
  }),
  deployment: {
    autoUpdates: false,
  },
})
