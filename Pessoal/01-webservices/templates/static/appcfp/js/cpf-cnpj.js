function validarCpfCnpj(){
    /* A variável recebe o número do CPF ou CNPJ digitado no formulário */
    let numInformado = document.getElementById('cpf_cnpj').value
    /* A variável recebe o tipo "F" ou "J" digitado no formulário */
    let tipInformado = document.getElementById('tipo').value
    let numValidar = numInformado
    let numQuantidade = numValidar.length
    let soma = 0

    /* Valida o CPF */
    if (numQuantidade == 11){
        let cpf = numValidar
        /* Calcula os dígitos verificadores */
        for (let i = 0; i < 9; i++) {
            dig = cpf[i]
            soma += parseInt(dig) * (10 - i)
        }

        let resto = soma % 11
        let digito1 = resto < 2 ? 0 : 11 - resto

        soma = 0
        for (let i = 0; i < 10; i++) {
            dig = cpf[i]
            soma += parseInt(dig) * (11 - i)
        }

        resto = soma % 11
        let digito2 = resto < 2 ? 0 : 11 - resto

        // Verificar se os dígitos verificadores estão corretos
        if (digito1 != parseInt(cpf[9]) || digito2 != parseInt(cpf[10])){
            alert('CPF inválido!')
            return false
        } else {
            if (tipInformado == 'J'){
                alert('CPF não corresponde com tipo!')
                return false
            }
        }
    }
    else if (numQuantidade == 14){
        let cnpj = numValidar

        // Calcular os dígitos verificadores
        let tamanho = cnpj.length - 2
        let numeros = cnpj.substring(0, tamanho)
        let digitos = cnpj.substring(tamanho)
        let soma = 0
        let pos = tamanho - 7

        for (let i = tamanho; i >= 1; i--) {
            soma += parseInt(numeros.charAt(tamanho - i)) * pos--
            if (pos < 2) {
                pos = 9
            }
        }

        let resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11)

        // Verificar se o primeiro dígito verificador está correto
        if (resultado !== parseInt(digitos.charAt(0))) {
            return false
        }

        tamanho = tamanho + 1
        numeros = cnpj.substring(0, tamanho)
        soma = 0
        pos = tamanho - 7

        for (let i = tamanho; i >= 1; i--) {
            soma += parseInt(numeros.charAt(tamanho - i)) * pos--
            if (pos < 2) {
                pos = 9
            }
        }

        resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11)

        // Verificar se o segundo dígito verificador está correto
        if (resultado != parseInt(digitos.charAt(1))){
            alert('CNPJ inválido!')
            return false
        } else {
            if (tipInformado == 'F'){
                alert('CNPJ não corresponde com tipo!')
                return false
            }
        }
    }
    else if (numQuantidade != 11 || numQuantidade != 14){
        if (tipInformado == 'F'){
            alert('CPF inválido!')
            return false
        } else {
            alert('CNPJ inválido!')
            return false
        }
    }
}