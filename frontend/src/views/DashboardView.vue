<template>
    <div class="p-3" style="display: flex; height: 53rem;">
        <DashboardSidebar @dashboard="exibirDashboard" @salvar="salvarDashboard" @carregar="carregarDashboard"
            @error="error" @alerta="alerta" ref="sidebar" />
        <Chart class="ms-3 rounded cards" :info="dados" :key="chartKey" v-if="dados" />
    </div>

    <div class="toast-container position-fixed bottom-0 start-50 translate-middle-x p-3">
        <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">{{ this.tituloToast }}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Fechar"></button>
            </div>
            <div class="toast-body text-black">
                {{ this.msgToast }}
            </div>
        </div>
    </div>

    <div class="modal fade" id="modalSalvar" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content cards">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="modalLabel">Salvar Dashboard</h1>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="nome" class="form-label">Nome:</label>
                            <input type="text" class="form-control" id="nome" v-model="nome" required />
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <button type="button" class="btn btn-primary" @click="salvarDashboardModal">Confirmar</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="modalCarregar" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content cards">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="modalLabel">Carregar Dashboard</h1>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="dashboard" class="form-label">Dashboard:</label>
                            <select class="form-select" required v-model="dashboardSelecionado" id="dashboard">
                                <option value="" selected>Selecione um dashboard...</option>
                                <option v-for="dashboard in dashboards" :value="dashboard">{{ dashboard.nome }}
                                </option>
                            </select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <button type="button" class="btn btn-primary" @click="carregarDashboardModal">Confirmar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import DashboardSidebar from '../components/DashboardSidebar.vue'
import Chart from '../components/Chart.vue';
import axios from 'axios'

export default {
    components: {
        DashboardSidebar,
        Chart
    },
    data() {
        return {
            dados: null,
            chartKey: 0,
            tituloToast: '',
            msgToast: '',
            nome: '',
            jogo: '',
            info: '',
            dashboardSelecionado: '',
            dashboards: []
        }
    },
    methods: {
        exibirDashboard(dados) {
            this.dados = dados.data;
            if (this.dados.error) {
                const toastLiveExample = document.getElementById('liveToast')
                const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

                this.tituloToast = 'Erro'
                this.msgToast = this.dados.error

                toastBootstrap.show()
            } else if (this.dados) {
                this.chartKey++;
            }
        },
        error() {
            const toastLiveExample = document.getElementById('liveToast')
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

            this.tituloToast = 'Erro'
            this.msgToast = 'Erro ao gerar dashboard.'

            toastBootstrap.show()
        },
        alerta(titulo, mensagem) {
            const toastLiveExample = document.getElementById('liveToast')
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

            this.tituloToast = titulo
            this.msgToast = mensagem

            toastBootstrap.show()
        },
        salvarDashboard(jogo, informacoes) {
            this.jogo = jogo
            this.info = informacoes

            const modal = document.getElementById('modalSalvar')
            const modalBootstrap = bootstrap.Modal.getOrCreateInstance(modal)

            modalBootstrap.show()
        },
        salvarDashboardModal() {
            if (this.nome) {
                const modal = document.getElementById('modalSalvar')
                const modalBootstrap = bootstrap.Modal.getOrCreateInstance(modal)

                try {
                    axios.post('/api/dashboard/', {
                        game: this.jogo,
                        nome: this.nome,
                        info: this.info
                    }).then(response => {
                        this.alerta('Sucesso', 'Dashboard salvo com sucesso.')
                        this.nome = ''
                        modalBootstrap.hide()
                    }).catch(error => {
                        this.alerta('Erro', 'Erro ao salvar o dashboard.')
                    })
                } catch (error) {
                    this.alerta('Erro', 'Erro ao salvar o dashboard.')
                }
            } else {
                this.alerta('Atenção', 'Preencha os campos obrigatórios para salvar.')
            }
        },
        carregarDashboard(jogo) {
            this.jogo = jogo
            this.dashboards = []

            const modal = document.getElementById('modalCarregar')
            const modalBootstrap = bootstrap.Modal.getOrCreateInstance(modal)

            try {
                axios.get('/api/dashboard/' + this.jogo)
                    .then(response => {
                        response.data.forEach(element => {
                            this.dashboards.push(element);
                        })
                        modalBootstrap.show()
                    })
                    .catch(error => {
                        this.$emit('alerta', 'Erro', 'Erro ao buscar os dashboards.')
                    })
            } catch (error) {
                this.$emit('alerta', 'Erro', 'Erro ao buscar os dashboards.')
            }
        },
        carregarDashboardModal() {
            if (this.dashboardSelecionado) {
                const modal = document.getElementById('modalCarregar')
                const modalBootstrap = bootstrap.Modal.getOrCreateInstance(modal)

                this.$refs.sidebar.carregaInfo(this.dashboardSelecionado)

                this.alerta('Sucesso', 'Dashboard carregado com sucesso.')
                this.dashboardSelecionado = ''
                this.dashboards = []

                modalBootstrap.hide()
            } else {
                this.alerta('Atenção', 'Preencha os campos obrigatórios para carregar.')
            }
        }
    }
};

</script>