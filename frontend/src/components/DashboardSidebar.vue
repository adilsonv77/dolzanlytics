<template>
    <div class="cards rounded p-3" style="width: 20rem; min-width: 15rem;">
        <form @submit.prevent="gerarDashboard">
            <div class="mb-3">
                <label for="game" class="form-label" style="margin-top: .3rem;">Jogo:</label>
                <div class="dropdown" style="float: right;">

                    <button class="btn btn-secondary dropdown-toggle btn-sm" type="button" data-bs-toggle="dropdown"
                        aria-expanded="false" style="margin-bottom: .3rem;">
                        +
                    </button>
                    <ul class="dropdown-menu dropdown-menu-dark">
                        <li><a class="dropdown-item" href='#' @click="salvarDashboard">Salvar</a></li>
                        <li><a class="dropdown-item" href="#" @click="carregarDashboard">Carregar</a></li>
                    </ul>
                </div>
                <select class="form-select" required v-model="jogoSelecionado" id="game" @change="changeJogo">
                    <option value="" selected>Selecione um jogo...</option>
                    <option v-for="jogo in jogos" :value="jogo.sequence">{{ jogo.nome }}</option>
                </select>

                <label for="id" class="form-label">Identificador:</label>
                <select class="form-select" size="7" multiple v-model="idSelecionado" id="id">
                    <option v-for="id in ids" :value="id.id">{{ id.id }}</option>
                </select>

                <label for="artifact" class="form-label">Artefato:</label>
                <select class="form-select" size="7" multiple required v-model="artefatoSelecionado" id="artifact"
                    @change="onChangeArtefato">
                    <option v-for="artefato in artefatos" :value="artefato.id">{{ artefato.nome }}</option>
                </select>

                <label for="function" class="form-label">Função:</label>
                <select class="form-select" required v-model="funcaoSelecionada" id="function">
                    <option value="" selected>Selecione uma função...</option>
                    <option v-for="funcao in funcoes" :value="funcao.id">{{ funcao.nome }}</option>
                </select>

                <label for="type" class="form-label">Tipo de Gráfico:</label>
                <select class="form-select" required v-model="graficoSelecionado" id="type">
                    <option value="" selected>Selecione um tipo...</option>
                    <option v-for="tipo in graficos" :value="tipo.id">{{ tipo.nome }}</option>
                </select>

                <label for="date" class="form-label">Período:</label>
                <input type="datetime-local" class="form-control" id="inicio" v-model="dataInicio"
                    style="width: 12rem; margin-bottom: .3rem;" />
                <input type="datetime-local" class="form-control" id="final" v-model="dataFinal" style="width: 12rem;" />
            </div>
            <div style="float: right; margin-bottom: 10rem;">
                <button type="submit" class="btn btn-primary">Gerar</button>
            </div>
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
            ids: [],
            idSelecionado: [],
            artefatos: [],
            artefatoSelecionado: [],
            funcoes: [],
            funcaoSelecionada: '',
            graficoSelecionado: '',
            graficos: [
                { 'id': 'bar', 'nome': 'Barra' },
                { 'id': 'line', 'nome': 'Linha' },
                { 'id': 'pie', 'nome': 'Pizza' },
                { 'id': 'doughnut', 'nome': 'Rosquinha' },
                { 'id': 'polarArea', 'nome': 'Polar' },
                { 'id': 'radar', 'nome': 'Radar' },
            ],
            dataInicio: null,
            dataFinal: null
        };
    },
    methods: {
        async gerarDashboard() {
            await axios.post('/gerar-dashboard/', {
                game: this.jogoSelecionado,
                id: this.idSelecionado,
                artefato: this.artefatoSelecionado,
                funcao: this.funcaoSelecionada,
                tipo: this.graficoSelecionado,
                inicio: this.dataInicio,
                final: this.dataFinal
            })
                .then(retorno => {
                    this.$emit('dashboard', retorno)
                })
                .catch(error => {
                    this.$emit('error')
                })
        },
        changeJogo() {
            this.ids = []
            this.idSelecionado = []
            this.artefatos = []
            this.artefatoSelecionado = []

            if (this.jogoSelecionado) {
                try {
                    axios.get('/api/identifier/' + this.jogoSelecionado)
                        .then(response => {
                            response.data.forEach(element => {
                                this.ids.push(element);
                            })
                        })
                        .catch(error => {
                            this.$emit('alerta', 'Erro', 'Erro ao buscar os identificadores.')
                        })
                } catch (error) {
                    this.$emit('alerta', 'Erro', 'Erro ao buscar os identificadores.')
                }

                try {
                    axios.get('/api/artifact/game/' + this.jogoSelecionado)
                        .then(response => {
                            response.data.forEach((element) => {
                                this.artefatos.push(element);
                            })
                        })
                        .catch(error => {
                            this.$emit('alerta', 'Erro', 'Erro ao buscar os artefatos.')
                        })
                } catch (error) {
                    this.$emit('alerta', 'Erro', 'Erro ao buscar os artefatos.')
                }
            }
        },
        onChangeArtefato() {
            let type = null

            this.artefatoSelecionado.forEach(artefato => {
                if (!type) {
                    type = this.getTypeArtefato(artefato)
                } else if (this.getTypeArtefato(artefato) != type) {
                    this.artefatoSelecionado = []
                    this.$emit('alerta', 'Atenção', 'É permitido selecionar apenas artefatos do mesmo tipo.')
                }
            })
        },
        getTypeArtefato(artefato) {
            let type = null

            this.artefatos.forEach(artef => {
                if (artefato == artef.id) {
                    type = artef.type;
                    return;
                }
            })

            return type;
        },
        salvarDashboard() {
            if (Boolean(this.jogoSelecionado) && Boolean(this.artefatoSelecionado.length) && Boolean(this.funcaoSelecionada) && Boolean(this.graficoSelecionado)) {
                let info = {
                    id: this.idSelecionado,
                    artefato: this.artefatoSelecionado,
                    funcao: this.funcaoSelecionada,
                    tipo: this.graficoSelecionado,
                    inicio: this.dataInicio,
                    final: this.dataFinal
                }
                this.$emit('salvar', this.jogoSelecionado, JSON.stringify(info));
            } else {
                this.$emit('alerta', 'Atenção', 'Preencha os campos obrigatórios para salvar.')
            }
        },
        carregarDashboard() {
            if (Boolean(this.jogoSelecionado)) {
                this.$emit('carregar', this.jogoSelecionado);
            } else {
                this.$emit('alerta', 'Atenção', 'Selecione um jogo para carregar os dashboards salvos.')
            }
        },
        carregaInfo(dashboard) {
            let info = JSON.parse(dashboard.info)

            this.idSelecionado = info['id']
            this.artefatoSelecionado = info['artefato']
            this.funcaoSelecionada = info['funcao']
            this.graficoSelecionado = info['tipo']
            this.dataInicio = info['inicio']
            this.dataFinal = info['final']
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

        try {
            axios.get('/api/functions/')
                .then(response => {
                    this.funcoes = response.data
                })
                .catch(error => {
                    this.$emit('alerta', 'Erro', 'Erro ao buscar as funções.')
                });
        } catch (error) {
            this.$emit('alerta', 'Erro', 'Erro ao buscar as funções.')
        }
    }
};
</script>