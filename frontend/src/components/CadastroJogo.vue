<template>
    <h1>Cadastro de Jogo</h1>
    <form @submit.prevent="enviarFormulario">
        <div class="mb-3">
            <label for="game" class="form-label">Jogo:</label>
            <input type="text" class="form-control" id="game" v-model="gameName" required />
        </div>
        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            gameName: ''
        };
    },
    methods: {
        enviarFormulario() {
            try {
                axios.post('/api/game/', { nome: this.gameName })
                    .then(response => {
                        this.gameName = null;
                        this.$emit('cadastroSucesso', 'Jogo', ' (Código: ' + response.data.sequence + ').');
                    })
                    .catch(error => {
                        this.$emit('cadastroErro', 'Jogo');
                    });
            } catch (error) {
                this.$emit('cadastroErro', 'Jogo');
            }
        },
    },
};
</script>
  