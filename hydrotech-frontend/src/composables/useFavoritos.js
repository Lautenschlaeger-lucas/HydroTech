/**
 * Favoritos e alertas do usuário — mesma lógica que estava no MonitoramentoView
 * (localStorage + API), só que compartilhada entre os componentes.
 */
import { ref, computed } from 'vue'
import api from '@/services/api'

const lerSet = chave => { try { return new Set(JSON.parse(localStorage.getItem(chave) || '[]')) } catch { return new Set() } }

const favs = ref(lerSet('ht_favs'))
const alerts = ref(lerSet('ht_alerts'))
const userData = ref((() => { try { return JSON.parse(localStorage.getItem('user_data') || '{}') } catch { return {} } })())

const salvar = () => {
  localStorage.setItem('ht_favs', JSON.stringify([...favs.value]))
  localStorage.setItem('ht_alerts', JSON.stringify([...alerts.value]))
}

export function useFavoritos() {
  const isLoggedIn = computed(() => { void userData.value; return !!localStorage.getItem('user_token') })
  const isDefesaCivil = computed(() => !!userData.value.is_defesa_civil)

  async function alternar(conjunto, id, chamada) {
    const tinha = conjunto.value.has(id)
    const novo = new Set(conjunto.value)
    tinha ? novo.delete(id) : novo.add(id)
    conjunto.value = novo
    salvar()
    if (!localStorage.getItem('user_token')) return
    try { await chamada(id) } catch (e) {
      console.error('Erro ao salvar na API:', e)
      const volta = new Set(conjunto.value)
      tinha ? volta.add(id) : volta.delete(id)
      conjunto.value = volta
      salvar()
    }
  }

  async function sincronizar() {
    if (!localStorage.getItem('user_token')) return
    try {
      const res = await api.me()
      userData.value = res.data
      localStorage.setItem('user_data', JSON.stringify(res.data))
      if (res.data.favoritos) favs.value = new Set(res.data.favoritos)
      if (res.data.alertas) alerts.value = new Set(res.data.alertas)
      salvar()
    } catch (e) {
      console.error('Erro ao sincronizar favoritos/alertas:', e)
    }
  }

  return {
    favs, alerts, isLoggedIn, isDefesaCivil, sincronizar,
    isFav: id => favs.value.has(id),
    isAlert: id => alerts.value.has(id),
    toggleFav: id => alternar(favs, id, api.toggleFavorite),
    toggleAlert: id => alternar(alerts, id, api.toggleAlert),
  }
}
