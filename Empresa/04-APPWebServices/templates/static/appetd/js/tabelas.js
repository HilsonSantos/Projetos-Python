const formInsert = document.getElementById('form-insert');
if (formInsert) {
    formInsert.addEventListener(
        'show.bs.modal', event => {
            const button = event.relatedTarget
            const modalTitle = formInsert.querySelector('.modal-title')
            modalTitle.textContent = 'Novo cadastro'
        }
    )
}
