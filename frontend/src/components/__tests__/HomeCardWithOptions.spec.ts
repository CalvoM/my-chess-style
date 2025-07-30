import { beforeEach, describe, expect, it } from 'vitest'
import HomeCardWithOptions from '../HomeCardWithOptions.vue'
import '@testing-library/jest-dom'
import { fireEvent, render, screen } from '@testing-library/vue'
import { setActivePinia, createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Avatar from 'primevue/avatar'
import ToggleSwitch from 'primevue/toggleswitch'
import InputText from 'primevue/inputtext'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import FileUpload from 'primevue/fileupload'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import Select from 'primevue/select'
import { mount } from '@vue/test-utils'

const testGlobalConfig = {
  plugins: [PrimeVue, ToastService],
  components: {
    Button,
    Card,
    Avatar,
    ToggleSwitch,
    InputText,
    Tabs,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    FileUpload,
    Toast,
    Select,
  },
}

describe('HomeCardWithOptions', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  it('renders pgn file upload button', async () => {
    render(HomeCardWithOptions, { global: testGlobalConfig })
    screen.getByRole('button', { name: /Analyze PGN File/i })
  })
  it('renders analyze external platform games button', async () => {
    render(HomeCardWithOptions, { global: testGlobalConfig })
    expect(screen.queryByRole('button', { name: /Analyze Games/i })).toBeNull()
    const enterUsernameBtn = screen.getByRole('tab', { name: /Enter Username/i })
    await fireEvent.click(enterUsernameBtn)
    screen.getByRole('button', { name: /Analyze Games/i })
  })
  it('renders track progress button', async () => {
    render(HomeCardWithOptions, { global: testGlobalConfig })
    expect(screen.queryByRole('button', { name: /Track Progress by ID/i })).toBeNull()
    const trackProgressBtn = screen.getByRole('tab', { name: /Track Progress/i })
    await fireEvent.click(trackProgressBtn)
    screen.getByRole('button', { name: /Track Progress by ID/i })
  })
  it('enables pgn file upload button when both username and file are present', async () => {
    const { baseElement } = render(HomeCardWithOptions, { global: testGlobalConfig })
    const targeBtn = screen.getByRole('button', { name: /Analyze PGN File/i })
    expect(targeBtn).toBeDisabled()
    // const pgnFileInput = screen.getAllByRole()
    // console.log(pgnFileInput)
    // await fireEvent.update(pgnFileInput, 'file')
    // expect(targeBtn).toBeDisabled()
    // const pgnUsernameInput = screen.getByPlaceholderText(/Enter your chess username/i)
    // await fireEvent.update(pgnUsernameInput, 'file')
    // expect(targeBtn).not.toBeDisabled()
  })
  it('disables analysis button when username is absent', {})
  it('sends file and username to the server when pgn file upload button clicked', {})
  it('sends username to the server when analysis button is clicked', {})
  it('sends trackingID when track progress button is clicked', {})
})
