import type { NotificationTheme } from '@/types'
import { defineStore } from 'pinia'
import { useToast } from 'primevue'
import { ref, type Ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const toast = useToast()
  function showMessage(severity: NotificationTheme, summary: string, detail: string): string {
    const toastTheme = new Map<NotificationTheme, string>([
      ['error', 'bg-red-500 text-white'],
      ['success', 'bg-green-600 text-white'],
      ['secondary', 'bg-slate-200 text-black'],
      ['info', 'bg-sky-500 text-white'],
      ['warn', 'bg-orange-600 text-white'],
      ['contrast', 'bg-slate-900 text-white'],
    ])
    const toastThemeClass: string = toastTheme.get(severity) ?? 'bg-green-600 text-white'
    toast.add({
      severity: severity,
      summary: summary,
      detail: detail,
      life: 5000,
    })
    return toastThemeClass
  }
  return { showMessage }
})
