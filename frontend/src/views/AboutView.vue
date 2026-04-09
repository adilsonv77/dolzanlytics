<template>
  <div class="m-3">
    <h1>
      Projeto desenvolvido para defesa do TCC.
    </h1>
    <div class="rounded p-3 cards">
      <h3>Como funciona?</h3>
      <div class="ms-3">
        <p>1º: Na aba Cadastro, efetue o registro de seu Jogo.</p>
        <p>2º: Na aba Cadastro, efetue o registro dos artefatos que serão monitorados (ex: Tempo de fase, Respostas de
          perguntas, etc...)</p>
        <p>3º: Utilize o endpoint /api/data/ para enviar os dados.</p>
        <p>4º: Na aba Dashboard selecione as informações para gerar os gráficos.</p>
      </div>
      <h4>Dicas!</h4>
      <div class="ms-3">
        <p>Ao gerar o Dashboard é possível selecionar mais de um artefato para exibir as informações.</p>
        <p>Utilize o campo "id" da "Data" para identificar a origem da informação "id" (ex: um usuário, uma instância,
          etc...).</p>
        <p>É possível salvar e carregar os dashboards.</p>
      </div>
    </div>
    <div class="rounded p-3 mt-3 cards">
      <h3>
        API
      </h3>
      <div class="ms-3">
        <h4 v-for="api in apis">
          {{ api.nome }}
          <ul>
            <li v-for="campo in api.campos">
              {{ campo }}
            </li>
          </ul>
        </h4>
      </div>
    </div>
    <div class="rounded p-3 mt-3 cards">
      <h3>
        Autor
      </h3>
      <div class="ms-3">
        <p>Desenvolvido por Gabriel Dolzan, estudante do curso de Engenharia de Software na UDESC. 2023.</p>
        <p>Contato: gabriel.dolzan@hotmail.com</p>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      apis: [
        {
          nome: 'Dados (/api/data/)',
          campos: [
            'game: smallint',
            'id: text (opcional)',
            'artifact: string',
            'value: string'
          ]
        }
      ]
    };
  },
}
</script>
<style></style>
