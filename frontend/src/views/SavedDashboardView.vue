<template>
    <div class="p-3" style="display: flex; height: 53rem;">
        <SavedDashboardSidebar @dashboard="exibirDashboard" @error="error" @alerta="alerta" />
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
</template>

<script>
import SavedDashboardSidebar from '../components/SavedDashboardSidebar.vue'
import Chart from '../components/Chart.vue';

export default {
    components: {
        SavedDashboardSidebar,
        Chart
    },
    data() {
        return {
            dados: null,
            chartKey: 0,
            tituloToast: '',
            msgToast: ''
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
        }
    }
};

</script>