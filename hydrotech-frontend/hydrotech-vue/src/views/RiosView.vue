<template>
  <div class="rios">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Rios Monitorados</h1>
        <p class="page-subtitle">Gerencie os rios cadastrados no sistema</p>
      </div>
    </div>

    <!-- Form Card -->
    <div class="form-section">
      <div class="form-section-header">
        <div class="form-section-icon">
          <svg v-if="!form.id" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
        </div>
        <div>
          <h2>{{ form.id ? 'Editar Rio' : 'Cadastrar Novo Rio' }}</h2>
          <p v-if="form.id">Editando: <strong>{{ form.nome }}</strong></p>
        </div>
      </div>

      <div class="form-grid">
        <div class="form-group">
          <label for="rio-nome">Nome do Rio</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
            <input id="rio-nome" v-model="form.nome" placeholder="Ex: Rio Tietê" />
          </div>
        </div>
        <div class="form-group">
          <label for="rio-cidade">Cidade</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 21h18"/><path d="M5 21V7l8-4v18"/><path d="M19 21V11l-6-4"/><path d="M9 9h.01"/><path d="M9 13h.01"/><path d="M9 17h.01"/></svg>
            <input id="rio-cidade" v-model="form.cidade" placeholder="Ex: São Paulo" />
          </div>
        </div>
        <div class="form-group">
          <label for="rio-estado">Estado</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
            <input id="rio-estado" v-model="form.estado" placeholder="Ex: SP" />
          </div>
        </div>
        <div class="form-group">
          <label for="rio-risco">Risco de Inundação</label>
          <select id="rio-risco" v-model="form.risco_inundacao">
            <option value="">Selecione o nível...</option>
            <option value="1">🟢 Baixo</option>
            <option value="2">🟡 Médio</option>
            <option value="3">🔴 Alto</option>
            <option value="4">🔴 Muito Alto</option>
          </select>
        </div>
      </div>

      <div class="form-actions">
        <button class="btn-primary" @click="save" :disabled="saving">
          <svg v-if="saving" class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"><animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="0.8s" repeatCount="indefinite"/></circle></svg>
          <svg v-else-if="form.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          {{ saving ? 'Salvando...' : form.id ? 'Atualizar' : 'Cadastrar' }}
        </button>
        <button class="btn-secondary" v-if="form.id" @click="reset">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          Cancelar
        </button>
      </div>
    </div>

    <!-- Table Card -->
    <div class="table-section">
      <div class="table-header">
        <h2 class="table-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
          Lista de Rios
        </h2>
        <span class="table-count">{{ rios.length }} registros</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Cidade</th>
              <th>Estado</th>
              <th>Risco</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="rios.length === 0">
              <td colspan="6" class="empty-state">
                <div class="empty-content">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>
                  <p>Nenhum rio cadastrado</p>
                  <span>Use o formulário acima para cadastrar o primeiro rio</span>
                </div>
              </td>
            </tr>
            <tr v-for="rio in rios" :key="rio.id" class="table-row-animated">
              <td class="td-id">#{{ rio.id }}</td>
              <td class="td-name">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
                {{ rio.nome }}
              </td>
              <td>{{ rio.cidade }}</td>
              <td><span class="state-badge">{{ rio.estado }}</span></td>
              <td>
                <span class="badge" :class="getBadgeClass(rio.risco_inundacao)">
                  <span class="badge-dot"></span>
                  {{ getRiskLabel(rio.risco_inundacao) }}
                </span>
              </td>
              <td class="td-actions">
                <button class="btn-action btn-action--edit" @click="edit(rio)" title="Editar">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
                </button>
                <button class="btn-action btn-action--delete" @click="remove(rio.id)" title="Excluir">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <ConfirmModal ref="confirmRef" />
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import api from '../services/api'
import ConfirmModal from '@/components/ConfirmModal.vue'

const toast = inject('toast')
const confirmRef = ref(null)

const rios = ref([])
const saving = ref(false)
const form = ref({ id: null, nome: '', cidade: '', estado: '', risco_inundacao: '' })

const load = async () => {
  try {
    const res = await api.getRios()
    rios.value = res.data
  } catch (err) {
    toast?.error('Erro ao carregar', 'Não foi possível carregar a lista de rios.')
  }
}

const save = async () => {
  if (!form.value.nome || !form.value.cidade || !form.value.estado || !form.value.risco_inundacao) {
    toast?.warning('Campos obrigatórios', 'Preencha todos os campos antes de salvar.')
    return
  }
  saving.value = true
  try {
    const data = { ...form.value }
    data.risco_inundacao = parseInt(data.risco_inundacao)
    if (form.value.id) {
      await api.updateRio(form.value.id, data)
      toast?.success('Rio atualizado', `"${form.value.nome}" foi atualizado com sucesso.`)
    } else {
      await api.createRio(data)
      toast?.success('Rio cadastrado', `"${form.value.nome}" foi adicionado ao monitoramento.`)
    }
    reset()
    load()
  } catch (err) {
    toast?.error('Erro ao salvar', 'Ocorreu um erro ao salvar os dados do rio.')
  } finally {
    saving.value = false
  }
}

const edit = (rio) => {
  form.value = { ...rio }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const remove = async (id) => {
  const confirmed = await confirmRef.value?.show({
    title: 'Excluir rio',
    message: 'Tem certeza que deseja excluir este rio? Esta ação não pode ser desfeita.',
    confirmText: 'Sim, excluir',
    type: 'danger'
  })

  if (confirmed) {
    try {
      await api.deleteRio(id)
      toast?.success('Rio excluído', 'O rio foi removido do monitoramento.')
      load()
    } catch (err) {
      toast?.error('Erro ao excluir', 'Não foi possível excluir o rio.')
    }
  }
}

const reset = () => {
  form.value = { id: null, nome: '', cidade: '', estado: '', risco_inundacao: '' }
}

const getBadgeClass = (risco) => {
  if (risco === 1) return 'badge--low'
  if (risco === 2) return 'badge--medium'
  if (risco === 3 || risco === 4) return 'badge--high'
  return 'badge--low'
}

const getRiskLabel = (risco) => {
  const labels = { 1: 'Baixo', 2: 'Médio', 3: 'Alto', 4: 'Muito Alto' }
  return labels[risco] || 'Desconhecido'
}

onMounted(load)
</script>

<style scoped>
.rios {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeInUp 0.4s ease-out;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-top: 4px;
}

/* Form Section */
.form-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 36px 32px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.form-section:hover {
  box-shadow: var(--shadow-md);
}

.form-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--accent-gradient);
}

.form-section-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.form-section-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: var(--accent-soft);
  color: var(--accent);
  flex-shrink: 0;
}

.form-section-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.form-section-header p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 22px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  padding-left: 40px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--accent-gradient);
  color: white;
  padding: 10px 22px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border);
  padding: 10px 22px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-secondary:hover {
  background: var(--bg-tertiary);
}

.spinner {
  animation: spin 0.8s linear infinite;
}

/* Table Section */
.table-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.table-section:hover {
  box-shadow: var(--shadow-md);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}

.table-title svg { color: var(--accent); }

.table-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
  background: var(--bg-secondary);
  padding: 4px 12px;
  border-radius: var(--radius-full);
}

.table-wrapper { overflow-x: auto; }

.td-id {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.td-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.state-badge {
  display: inline-block;
  padding: 2px 10px;
  background: var(--bg-secondary);
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}

.badge-dot {
  width: 7px;
  height: 7px;
  border-radius: var(--radius-full);
}

.badge--high { background: var(--risk-high-bg); color: var(--risk-high); }
.badge--high .badge-dot { background: var(--risk-high); }
.badge--medium { background: var(--risk-medium-bg); color: var(--risk-medium); }
.badge--medium .badge-dot { background: var(--risk-medium); }
.badge--low { background: var(--risk-low-bg); color: var(--risk-low); }
.badge--low .badge-dot { background: var(--risk-low); }

.td-actions {
  display: flex;
  gap: 6px;
  white-space: nowrap;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--card-bg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-action--edit {
  color: var(--accent);
}

.btn-action--edit:hover {
  background: var(--accent-soft);
  border-color: var(--accent);
  transform: none;
}

.btn-action--delete {
  color: var(--risk-high);
}

.btn-action--delete:hover {
  background: var(--risk-high-bg);
  border-color: var(--risk-high);
  transform: none;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 48px 24px !important;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
}

.empty-content p {
  font-weight: 600;
  color: var(--text-secondary);
}

.empty-content span {
  font-size: 0.85rem;
}

.table-row-animated {
  animation: fadeInUp 0.3s ease-out both;
}

/* Responsive */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary, .btn-secondary {
    justify-content: center;
  }
}
</style>