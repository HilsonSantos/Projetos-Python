function abrirModal(){
    var formModal = document.getElementById('form-modal')
    var buttonOpen = document.getElementsByClassName('#button-operaction')
    var buttonAcao = buttonOpen.value
    if (buttonAcao = 'Inserir'){
        document.getElementById('p_title').innerHTML = 'Inclusão de Cadastro'
    } else if (buttonAcao = 'Alterar'){
        document.getElementById('p_title').innerHTML = 'Alteração de Cadastro'
    } else {
        document.getElementById('p_title').innerHTML = 'Exclusão de Cadastro'
    }
    formModal.style.display = 'flex'
}
function fecharModal(){
    var formModal = document.getElementById('form-modal')
    formModal.style.display = 'none'
}