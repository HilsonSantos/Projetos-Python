var anoSelecionado = 0

function onChance(element, callback) {
    var previousValue = element.value
    element.addEventListener('input', function() {
        var currentValue = element.value
        if (currentValue !== previousValue) {
            callback(currentValue)
            previousValue = currentValue
        }
    })
    return previousValue
}

function openDashboard(url){
    fetch(url)
    .then(response => response.json())
    .then(jsonData => {
        var arrayAno = new Array()
        var jsonVendasTotalAno = jsonData.VendasTotalAno
        var jsonVendasTotalMes = jsonData.VendasTotalMes

        arrayAno.push({valor: 0, texto: 'Todos'})
        for (let i = 1; i < jsonVendasTotalAno.length; i++) {
            arrayAno.push({valor: i, texto: jsonVendasTotalAno[i][0]})
        }

        var options = arrayAno
        var select = document.getElementById("ano-Select")
        options.forEach(function(opcao) {
            var option = document.createElement("option")   // Criar um novo elemento option
            option.value = opcao.valor                      // Definir o valor da opção
            option.text = opcao.texto                       // Definir o texto da opção
            select.add(option)                              // Adicionar a opção ao select
        })
        select.value = "0"

        jsonVendasTotalAno[0].push({role: 'style'})
        for (let i = 1; i < jsonVendasTotalAno.length; i++) {
            jsonVendasTotalAno[i].push('color: #222c66')
        }

        const months = [
                "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"
              ]
        var monthNumber = 1;

        jsonVendasTotalMes[0].push({role: 'style'})
        for (let i = 1; i < jsonVendasTotalMes.length; i++) {
            jsonVendasTotalMes[i].push('color: #222c66')
            jsonVendasTotalMes[i][0] = months[i - monthNumber]
        }

        var opcaoSelecionada = document.getElementById('ano-Select')
        onChance(opcaoSelecionada, function (value) {

        })

        /*anoSelecionado = onChance(opcao)*/
        console.log(anoSelecionado)

        var jsonVendasTotalAno = jsonData.VendasTotalAno
        var jsonVendasTotalMes = jsonData.VendasTotalMes

        if (anoSelecionado == 1) {

            var arrayVendasTotalAno = new Array()
            arrayVendasTotalAno.push(jsonVendasTotalAno[0])
            arrayVendasTotalAno.push(jsonVendasTotalAno[1])
            var jsonVendasTotalAno = arrayVendasTotalAno

        } else if (anoSelecionado == 2) {

            var arrayVendasTotalAno = new Array()
            arrayVendasTotalAno.push(jsonVendasTotalAno[0])
            arrayVendasTotalAno.push(jsonVendasTotalAno[2])
            var jsonVendasTotalAno = arrayVendasTotalAno

        } else if (anoSelecionado == 3) {

            var arrayVendasTotalAno = new Array()
            arrayVendasTotalAno.push(jsonVendasTotalAno[0])
            arrayVendasTotalAno.push(jsonVendasTotalAno[3])
            var jsonVendasTotalAno = arrayVendasTotalAno

        } else {}

        jsonVendasTotalAno[0].push({role: 'style'})
        for (let i = 1; i < jsonVendasTotalAno.length; i++) {
            jsonVendasTotalAno[i].push('color: #222c66')
        }

        google.charts.load('current', {'packages':['corechart']})
        google.charts.setOnLoadCallback(drawChart)

        function drawChart() {
            /* GRÁFICO REFERENTE A QUANTIDADE DE PEDIDOS/ENTREGA POR INTERVALO */
            var formatterAno = new google.visualization.NumberFormat({pattern: '####'})
            var formatterValor = new google.visualization.NumberFormat({pattern: 'R$ #,###.00'})
            var vendasTotalAno = google.visualization.arrayToDataTable(jsonVendasTotalAno)

            formatterAno.format(vendasTotalAno, 0)
            formatterValor.format(vendasTotalAno, 1)

            var options = {
                backgroundColor: '#ffffff',
                title: 'Análise de Vendas por Ano',
                legend: 'none',
                titleTextStyle: {fontSize: 18},
                hAxis: {
                    title: 'Ano',
                    format: {pattern: '####'},
                    titleTextStyle: {fontSize: 18},
                    titlePosition: 'in'
                },
                vAxis: {
                    title: 'Vendas'
                }
            }

            var barchart = new google.visualization.ColumnChart(document.getElementById('barchart-vendas-total-ano'))
            barchart.draw(vendasTotalAno, options)
        }
    })
}


/* GRÁFICO REFERENTE A QUAvendasTotalAnoNTIDADE DE PEDIDOS/RETIRA POR INTERVALO */
/*


var vendasTotalMes = google.visualization.arrayToDataTable(jsonVendasTotalMes)

formatterValor.format(vendasTotalMes, 1)
var options = {
        title: 'Análise de Vendas por Mês',
        legend: 'none',
        titleTextStyle: {fontSize: 18},
        hAxis: {
            title: 'Mês',
            format: {pattern: '####'},
            titleTextStyle: {fontSize: 18},
            titlePosition: 'in'
        },
        vAxis: {
            title: 'Vendas'
        }
    }

var barchart = new google.visualization.ColumnChart(document.getElementById('barchart-vendas-total-mes'))
barchart.draw(vendasTotalMes, options)
*/

