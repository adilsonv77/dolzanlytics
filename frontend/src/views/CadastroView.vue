<template>
    <main class="mt-2">
        <div class="d-flex flex-wrap justify-content-around">
            <div id="app" class="container rounded m-3 w-25 cadastro cards">
                <CadastroJogo @cadastro-sucesso="cadastroSucesso" @cadastro-erro="cadastroErro" @alert="alert" />
            </div>
            <div id="app" class="container rounded m-3 w-25 cadastro cards">
                <CadastroArtefato @cadastro-sucesso="cadastroSucesso" @cadastro-erro="cadastroErro" />
            </div>
        </div>

        <div class="modal fade" id="modal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header text-black">
                        <h1 class="modal-title fs-5" id="modalLabel">{{ this.tituloToast }}</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-black">
                        {{ this.msgToast }}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>

    </main>
</template>

<script>
import CadastroJogo from '@/components/CadastroJogo.vue';
import CadastroArtefato from '@/components/CadastroArtefato.vue';

export default {
    components: {
        CadastroJogo,
        CadastroArtefato
    },
    data() {
        return {
            tituloToast: '',
            msgToast: ''
        }
    },
    methods: {
        cadastroSucesso(tipo, info = '') {
            const myModalAlternative = new bootstrap.Modal('#modal')

            this.tituloToast = 'Sucesso'
            this.msgToast = tipo + ' cadastrado com sucesso.' + info

            myModalAlternative.show()
        },
        cadastroErro(tipo) {
            const myModalAlternative = new bootstrap.Modal('#modal')

            this.tituloToast = 'Atenção'
            this.msgToast = 'Erro ao cadastrar ' + tipo + '.'

            myModalAlternative.show()
        },
        alert(titulo, mensagem) {
            const myModalAlternative = new bootstrap.Modal('#modal')

            this.tituloToast = titulo
            this.msgToast = mensagem

            myModalAlternative.show()
        }
    }
};
</script>

<style scoped>
.cadastro {
    min-width: 30rem;
}
</style>
