//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// CHAMA A JANELA PARA INSERIR OS DADOS                                                                             //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const formInsert = document.getElementById('form-insert');
if (formInsert) {
    formInsert.addEventListener(
        'show.bs.modal', event => {
            const button = event.relatedTarget
            const modalTitle = formInsert.querySelector('.modal-title')
            modalTitle.textContent = 'Novo cadastro de banco'
        }
    )
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ESSA FUNÇÃO IMPEDI O USUÁRIO SÓ DIGITAR NÚMERO NO CAMPO CÓDIGO                                                   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function SomenteNumero(e){
    var tecla = (event) ? event.keyCode : e.which
    if (tecla >= 48 && tecla <= 57)
        return true
    else
        document.getElementById("banco-codigo").innerHTML = ''
        window.alert('Erro, o campo só aceita número.')
        return false
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ESSA FUNÇÃO FAZ A VALIDAÇÃO DOS CAMPOS CÓDIGO E DESCRIÇÃO, CASO ESTEJA SEM INFORMAÇÃO                            //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function ValidarCampos(){
      let codigo = document.getElementById('banco-codigo');
      let descricao = document.getElementById('banco-descricao');

      if (!codigo.checkValidity()) {
         alert('Código não informado!')
      } else if (!descricao.checkValidity()) {
         alert('Descrição não informado!')
      } else {
        $("#form-insert").modal('hide');
      }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ESSA FUNÇÃO DESABILITA OS MENUS DE ALTERAR E EXCLUIR, CASO NÃO EXISTA DADOS INFORMADOS                           //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function DesabilitarMenu(){
    const malterar = document.querySelector('#malterar');
    const mexcluir = document.querySelector('#mexcluir');
    let table1 = document.getElementById('tbody')
    let linhas = table1.getElementsByTagName('tr')
    let res = document.querySelector('div#totalreg')
    vs_valortotal = res.innerText +" "+linhas.length
    res.innerText = vs_valortotal
    if (linhas.length == 0) {
        malterar.classList.add('disabled');
        mexcluir.classList.add('disabled');
    }
}