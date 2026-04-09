<template>
  <h1>Cadastro de Artefato</h1>
  <form @submit.prevent="enviarFormulario">
    <div class="mb-3">
      <label for="game" class="form-label">Jogo:</label>
      <select class="form-select" required v-model="jogoSelecionado" id="game">
        <option value="" selected>Selecione um jogo...</option>
        <option v-for="jogo in jogos" :value="jogo.sequence">{{ jogo.nome }}</option>
      </select>

      <label for="id" class="form-label">Identificador:</label>
      <input type="text" class="form-control" id="id" v-model="artefatoId" required />

      <label for="nome" class="form-label">Descrição:</label>
      <input type="text" class="form-control" id="nome" v-model="artefatoNome" required />

      <label for="tipo" class="form-label">Tipo:</label>
      <select class="form-select" required v-model="tipoSelecionado" id="tipo">
        <option value="" selected>Selecione um tipo...</option>
        <option v-for="tipo in tipos" :value="tipo">{{ tipo }}</option>
      </select>
    </div>
    <button type="submit" class="btn btn-primary">Enviar</button>
  </form>
</template>
  
<script>
import axios from 'axios'

export default {
  data() {
    return {
      jogoSelecionado: '',
      artefatoId: '',
      artefatoNome: '',
      tipoSelecionado: '',
      tipos: ['numeric', 'timestamp', 'interval', 'text', 'boolean'],
      jogos: []
    };
  },
  methods: {
    enviarFormulario() {
      try {
        axios.post('/api/artifact/', { id: this.artefatoId, nome: this.artefatoNome, game: this.jogoSelecionado, type: this.tipoSelecionado })
          .then(response => {
            this.jogoSelecionado = '';
            this.artefatoId = '';
            this.artefatoNome = '';
            this.tipoSelecionado = '';
            this.$emit('cadastroSucesso', 'Artefato');
          })
          .catch(error => {
            this.$emit('cadastroErro', 'Artefato');
          });
      } catch (error) {
        this.$emit('cadastroErro', 'Artefato');
      }
    },
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
          this.$emit('alert', 'Erro!', 'Erro ao buscar os jogos.');
        });
    } catch (error) {
      this.$emit('alert', 'Erro!', 'Erro ao buscar os jogos.');
    }
  }
};
</script>
  