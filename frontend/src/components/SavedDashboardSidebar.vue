<template>
    <div class="cards rounded p-3" style="width: 20rem; min-width: 15rem; height: 14rem;">
        <form @submit.prevent="gerarDashboard">
            <div class="mb-3">
                <label for="game" class="form-label">Jogo:</label>
                <select class="form-select" required v-model="jogoSelecionado" id="game" @change="changeJogo">
                    <option value="" selected>Selecione um jogo...</option>
                    <option v-for="jogo in jogos" :value="jogo.sequence">{{ jogo.nome }}</option>
                </select>
                <label for="dashboard" class="form-label">Dashboard:</label>
                <select class="form-select" required v-model="dashboardSelecionado" id="dashboard">
                    <option value="" selected>Selecione um dashboard...</option>
                    <option v-for="dashboard in dashboards" :value="dashboard.sequence">{{ dashboard.nome }}</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Gerar</button>
        </form>
    </div>
</template>
<script>
import axios from 'axios'

export default {
    data() {
        return {
            jogos: [],
            jogoSelecionado: '',
            dashboards: [],
            dashboardSelecionado: ''
        };
    },
    methods: {
        changeJogo() {
            this.dashboards = []
            this.dashboardSelecionado = ''

            if (this.jogoSelecionado) {
                try {
                    axios.get('/api/dashboard/' + this.jogoSelecionado)
                        .then(response => {
                            response.data.forEach(element => {
                                this.dashboards.push(element);
                            })
                        })
                        .catch(error => {
                            this.$emit('alerta', 'Erro', 'Erro ao buscar os dashboards.')
                        })
                } catch (error) {
                    this.$emit('alerta', 'Erro', 'Erro ao buscar os dashboards.')
                }
            }
        },
        async gerarDashboard() {
            await axios.post('/gerar-dashboard-saved/', {
                    sequence: this.dashboardSelecionado
                })
                .then(retorno => {
                    this.$emit('dashboard', retorno)
                })
                .catch(error => {
                    this.$emit('error')
                })
        }
    },
    created() {
        try {
            axios.get('/api/game/')
                .then(response => {
                    response.data.forEach((element) => {
                        this.jogos.push(element);
                    });
                })
                .catch(error => {
                    this.$emit('alerta', 'Erro', 'Erro ao buscar os jogos.')
                });
        } catch (error) {
            this.$emit('alerta', 'Erro', 'Erro ao buscar os jogos.')
        }
    }
};
</script>