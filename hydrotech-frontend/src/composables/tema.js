/**
 * Tema do site: usa a escolha salva da pessoa; se ela nunca escolheu,
 * segue o tema do aparelho (claro/escuro) e acompanha quando ele muda.
 */
const prefereClaro = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: light)').matches

export function temaSalvo() {
  try { return localStorage.getItem('theme') } catch { return null }
}

export function temaAtual() {
  return temaSalvo() || (prefereClaro() ? 'light' : 'dark')
}

export function aplicarTema(tema = temaAtual()) {
  document.documentElement.setAttribute('data-theme', tema)
}

/** Enquanto não houver escolha salva, troca junto com o aparelho. */
export function acompanharTemaDoAparelho() {
  const mq = window.matchMedia?.('(prefers-color-scheme: light)')
  mq?.addEventListener?.('change', () => {
    if (temaSalvo()) return
    aplicarTema()
    window.dispatchEvent(new Event('theme-changed'))
  })
}
