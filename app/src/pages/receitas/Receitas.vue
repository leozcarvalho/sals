<script setup>
import { ref, reactive, onMounted } from "vue"
import { ReceitasClient } from "../../services/receitasApi"
import { ApiClient } from "../../services/genericApi"
import Loader from "../../components/Loader.vue"
import { handleApiToast } from "../../components/toast"

const api = new ReceitasClient()
const cozinhasApi = new ApiClient("/kitchens")
const formulasApi = new ApiClient("/formulas")
const produtosApi  = new ApiClient("/products")
const galpoesApi   = new ApiClient("/sheds")
const salasApi     = new ApiClient("/salas")
const baiasApi     = new ApiClient("/baias")

const loader = ref(null)
const receitas = ref([])
const total = ref(0)

// lookups { id: name }
const cozinhas = ref({})
const formulas = ref({})
const produtos  = ref({})
const galpoes   = ref({})
const salas     = ref({})
const baias     = ref({})

// detalhe da receita selecionada
const receitaSelecionada  = ref(null)
const produzirItens       = ref([])
const distribuicaoItens   = ref([])
const loadingProduzir     = ref(false)
const loadingDistribuicao = ref(false)

const hoje = new Date().toISOString().slice(0, 10)
const filtro = reactive({ data: hoje, id_cz: null, status: null })

const statusConfig = {
  aguardando: { label: "Aguardando", class: "bg-secondary" },
  produzir:   { label: "Produzir",   class: "bg-warning text-dark" },
  produzindo: { label: "Produzindo", class: "bg-primary" },
  produzido:  { label: "Produzido",  class: "bg-success" },
  cancelada:  { label: "Cancelada",  class: "bg-danger" },
}

const statusProduzirConfig = {
  aguardando: { label: "Aguardando", class: "bg-secondary" },
  pesar:      { label: "Pesar",      class: "bg-warning text-dark" },
  pesando:    { label: "Pesando",    class: "bg-primary" },
  pesado:     { label: "Pesado",     class: "bg-success" },
  cancelada:  { label: "Cancelada",  class: "bg-danger" },
}

const statusDistribuicaoConfig = {
  aguardando:   { label: "Aguardando",   class: "bg-secondary" },
  distribuir:   { label: "Distribuir",   class: "bg-warning text-dark" },
  distribuindo: { label: "Distribuindo", class: "bg-primary" },
  distribuido:  { label: "Distribuído",  class: "bg-success" },
  cancelado:    { label: "Cancelado",    class: "bg-danger" },
}

const statusOptions = Object.entries(statusConfig).map(([value, cfg]) => ({
  value, label: cfg.label,
}))

const carregarLookups = async () => {
  const [resCz, resFo, resPr, resGa, resSa, resBa] = await Promise.all([
    cozinhasApi.getList(),
    formulasApi.getList(),
    produtosApi.getList(),
    galpoesApi.getList(),
    salasApi.getList(),
    baiasApi.getList(),
  ])
  const list = (res) => res?.data?.items ?? res?.data?.data?.items ?? []
  cozinhas.value = Object.fromEntries(list(resCz).map(x => [x.id, x.name]))
  formulas.value = Object.fromEntries(list(resFo).map(x => [x.id, x.name]))
  produtos.value  = Object.fromEntries(list(resPr).map(x => [x.id, x.name]))
  galpoes.value   = Object.fromEntries(list(resGa).map(x => [x.id, x.name]))
  salas.value     = Object.fromEntries(list(resSa).map(x => [x.id, x.name]))
  baias.value     = Object.fromEntries(list(resBa).map(x => [x.id, x.name ?? `Baia ${x.id}`]))
}

const carregar = async () => {
  loader.value.loaderOn()
  const params = {}
  if (filtro.data)   params.data   = filtro.data
  if (filtro.id_cz)  params.id_cz  = filtro.id_cz
  if (filtro.status) params.status = filtro.status
  const res = await api.getList(params)
  receitas.value = res?.data?.items ?? res?.data?.data?.items ?? []
  total.value    = res?.data?.count ?? res?.data?.data?.count ?? 0
  loader.value.loaderOff()
}

const abrirProduzir = async (receita) => {
  receitaSelecionada.value = receita
  produzirItens.value = []
  loadingProduzir.value = true
  const res = await api.getProduzir(receita.id)
  produzirItens.value = res?.data ?? []
  loadingProduzir.value = false
}

const abrirDistribuicao = async (receita) => {
  receitaSelecionada.value = receita
  distribuicaoItens.value = []
  loadingDistribuicao.value = true
  const res = await api.getDistribuicao(receita.id)
  distribuicaoItens.value = res?.data ?? []
  loadingDistribuicao.value = false
}

const gerar = async () => {
  loader.value.loaderOn()
  const res = await api.gerar(filtro.data)
  handleApiToast(res, "Receitas geradas com sucesso!")
  loader.value.loaderOff()
  await carregar()
}

const fmtHora     = (v) => v ? String(v).slice(0, 5) : "—"
const fmtDatetime = (v) => v ? new Date(v).toLocaleString("pt-BR") : "—"

onMounted(async () => {
  await carregarLookups()
  await carregar()
})
</script>

<template>
  <Loader ref="loader" />
  <div class="content">
    <BaseBlock title="Receitas de Produção" content-full>

      <!-- Filtros + Ação -->
      <div class="row g-2 mb-3 align-items-end">
        <div class="col-auto">
          <label class="form-label mb-1">Data</label>
          <input type="date" class="form-control form-control-lg" v-model="filtro.data" @change="carregar" />
        </div>
        <div class="col-auto">
          <label class="form-label mb-1">Cozinha</label>
          <select class="form-select form-select-lg" v-model="filtro.id_cz" @change="carregar">
            <option :value="null">Todas</option>
            <option v-for="(nome, id) in cozinhas" :key="id" :value="id">{{ nome }}</option>
          </select>
        </div>
        <div class="col-auto">
          <label class="form-label mb-1">Status</label>
          <select class="form-select form-select-lg" v-model="filtro.status" @change="carregar">
            <option value="">Todos</option>
            <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
        </div>
        <div class="col-auto ms-auto">
          <button class="btn btn-lg btn-primary" data-bs-toggle="modal" data-bs-target="#modal-gerar">
            <i class="fa fa-play me-1"></i> Gerar Receitas
          </button>
        </div>
      </div>

      <div class="text-muted small mb-2">{{ total }} receita(s) encontrada(s)</div>

      <!-- Tabela principal -->
      <div class="table-responsive">
        <table class="table table-striped align-middle">
          <thead>
            <tr>
              <th>ID</th>
              <th>SEQ</th>
              <th>Data</th>
              <th>Cozinha</th>
              <th>Fórmula</th>
              <th>Trato</th>
              <th>Etapa</th>
              <th>Peso seco (kg)</th>
              <th>Horário</th>
              <th>Início</th>
              <th>Fim</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="receitas.length === 0">
              <td colspan="13" class="text-center text-muted py-4">Nenhuma receita encontrada</td>
            </tr>
            <tr
              v-for="r in receitas"
              :key="r.id"
              :class="{ 'table-active': receitaSelecionada?.id === r.id }"
            >
              <td>{{ r.id }}</td>
              <td>{{ r.seq }}</td>
              <td>{{ r.data }}</td>
              <td :title="`ID: ${r.id_cz}`">{{ cozinhas[r.id_cz] ?? r.id_cz }}</td>
              <td :title="`ID: ${r.id_fo}`">{{ formulas[r.id_fo] ?? r.id_fo }}</td>
              <td>{{ r.trato }}</td>
              <td>{{ r.etapa }}</td>
              <td>{{ r.p_etapa_s_frac }}</td>
              <td>{{ fmtHora(r.hora_trato) }}</td>
              <td>{{ fmtDatetime(r.h_inicio) }}</td>
              <td>{{ fmtDatetime(r.h_fim) }}</td>
              <td>
                <span class="badge" :class="statusConfig[r.status]?.class ?? 'bg-secondary'">
                  {{ statusConfig[r.status]?.label ?? r.status }}
                </span>
              </td>
              <td>
                <div class="btn-group">
                  <button
                    class="btn btn-outline-secondary"
                    title="Ingredientes"
                    data-bs-toggle="modal"
                    data-bs-target="#modal-produzir"
                    @click="abrirProduzir(r)"
                  ><i class="fa fa-flask"></i></button>
                  <button
                    class="btn btn-outline-secondary"
                    title="Distribuição por baia"
                    data-bs-toggle="modal"
                    data-bs-target="#modal-distribuicao"
                    @click="abrirDistribuicao(r)"
                  ><i class="fa fa-truck"></i></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </BaseBlock>

    <!-- Modal ingredientes (RECEITAS_PRODUZIR) -->
    <div class="modal fade" id="modal-produzir" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Ingredientes — Receita #{{ receitaSelecionada?.id }}
              <span class="text-muted fw-normal fs-sm ms-2">
                {{ cozinhas[receitaSelecionada?.id_cz] }} · Trato {{ receitaSelecionada?.trato }} · Etapa {{ receitaSelecionada?.etapa }}
              </span>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingProduzir" class="text-center py-4 text-muted">Carregando...</div>
            <table v-else class="table align-middle mb-0">
              <thead>
                <tr>
                  <th>SEQ</th>
                  <th>Produto</th>
                  <th>Peso seco (kg)</th>
                  <th>Peso úmido (kg)</th>
                  <th>Volume (L)</th>
                  <th>Água</th>
                  <th>Início</th>
                  <th>Fim</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="produzirItens.length === 0">
                  <td colspan="9" class="text-center text-muted py-3">Sem ingredientes</td>
                </tr>
                <tr v-for="item in produzirItens" :key="item.id">
                  <td>{{ item.seq_dosagem }}</td>
                  <td :title="`ID: ${item.produto_id}`">{{ produtos[item.produto_id] ?? item.produto_id }}</td>
                  <td>{{ item.peso_etapa_sem_fracao_liquida }}</td>
                  <td>{{ item.peso_etapa_com_fracao_liquida }}</td>
                  <td>{{ item.volume_etapa }}</td>
                  <td>
                    <i v-if="item.produto_e_agua" class="fa fa-tint text-primary" title="Água"></i>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td>{{ fmtDatetime(item.h_inicio) }}</td>
                  <td>{{ fmtDatetime(item.h_fim) }}</td>
                  <td>
                    <span class="badge" :class="statusProduzirConfig[item.status]?.class ?? 'bg-secondary'">
                      {{ statusProduzirConfig[item.status]?.label ?? item.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button class="btn btn-lg btn-secondary" data-bs-dismiss="modal">Fechar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal distribuição (RECEITAS_DISTRIBUICAO) -->
    <div class="modal fade" id="modal-distribuicao" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Distribuição por Baia — Receita #{{ receitaSelecionada?.id }}
              <span class="text-muted fw-normal fs-sm ms-2">
                {{ cozinhas[receitaSelecionada?.id_cz] }} · Trato {{ receitaSelecionada?.trato }} · Etapa {{ receitaSelecionada?.etapa }}
              </span>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingDistribuicao" class="text-center py-4 text-muted">Carregando...</div>
            <table v-else class="table align-middle mb-0">
              <thead>
                <tr>
                  <th>Galpão</th>
                  <th>Sala</th>
                  <th>Baia</th>
                  <th>Suínos</th>
                  <th>Peso seco (kg)</th>
                  <th>Início</th>
                  <th>Fim</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="distribuicaoItens.length === 0">
                  <td colspan="8" class="text-center text-muted py-3">Sem baias</td>
                </tr>
                <tr v-for="item in distribuicaoItens" :key="item.id">
                  <td :title="`ID: ${item.galpao_id}`">{{ galpoes[item.galpao_id] ?? item.galpao_id }}</td>
                  <td :title="`ID: ${item.sala_id}`">{{ salas[item.sala_id] ?? item.sala_id }}</td>
                  <td :title="`ID: ${item.baia_id}`">{{ baias[item.baia_id] ?? item.baia_id }}</td>
                  <td>{{ item.quantidade_suinos }}</td>
                  <td>{{ item.peso_sem_fracao_liquida }}</td>
                  <td>{{ fmtDatetime(item.h_inicio) }}</td>
                  <td>{{ fmtDatetime(item.h_fim) }}</td>
                  <td>
                    <span class="badge" :class="statusDistribuicaoConfig[item.status]?.class ?? 'bg-secondary'">
                      {{ statusDistribuicaoConfig[item.status]?.label ?? item.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button class="btn btn-lg btn-secondary" data-bs-dismiss="modal">Fechar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal confirmar geração -->
    <div class="modal fade" id="modal-gerar" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">Gerar Receitas</div>
          <div class="modal-body">
            Gerar receitas para <strong>{{ filtro.data }}</strong>?<br />
            <span class="text-muted small">Se já existirem receitas para essa data, a operação será recusada.</span>
          </div>
          <div class="modal-footer">
            <button class="btn btn-lg btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-lg btn-primary" data-bs-dismiss="modal" @click="gerar">Confirmar</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
