/* ABRI O FORMULÁRIO MODAL */
function abrirModal(event){
    // Recebe ID do formulário
    let formModal = document.getElementById('form-modal-register')
    // Recebe a ID ao clicar no botão selecionado
    let buttonClick = event.target.id
    let formTitle = ''

    if (buttonClick == 'button-insert'){
         formTitle = 'Inclusão de Cadastro'
    }
    else if (buttonClick == 'button-update'){
        formTitle = 'Alteração de Cadastro'
    }
    else {
        formTitle = 'Exclusão de Cadastro'
    }
    // Informa no título do formulário a variável "formTitle"
    document.getElementById('p_title').innerHTML = formTitle
    // Altera no CSS o parâmetro display do class "formModal"
    formModal.style.display = 'flex'
}

/* FECHA O FORMULÁRIO MODAL */
function fecharModal(){
    // Recebe ID do formulário
    let formModal = document.getElementById('form-modal-register')
    // Altera no CSS o parâmetro display do class "formModal"
    formModal.style.display = 'none'
}