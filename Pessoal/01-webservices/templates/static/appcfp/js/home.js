// Função para formatar 1 em 01
const zeroFill = n => {
    return ('0' + n).slice(-2);
}
const interval = setInterval(
    () => {
		// Pega o horário atual
	    const now = new Date();
        // Formata a data conforme dd/mm/aaaa hh:ii:ss
		const dataHora = zeroFill(now.getUTCDate()) + '/' +
		                 zeroFill((now.getMonth() + 1)) + '/' +
		                 now.getFullYear() + ' ' +
		                 zeroFill(now.getHours()) + ':' +
		                 zeroFill(now.getMinutes()) + ':' +
		                 zeroFill(now.getSeconds());
        // Exibe na tela usando a p#data-hora
		document.getElementById('data-hora').innerHTML = 'Data/Hora: ' + dataHora;
	},
	1000
);