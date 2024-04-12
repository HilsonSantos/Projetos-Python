function openDashboard(url){
    fetch(url)
    .then(response => response.json())
    .then(jsonData => {

        google.charts.load('current', {'packages':['corechart']})
        google.charts.setOnLoadCallback(drawChart)

        function drawChart() {
            /* GRÁFICO REFERENTE A QUANTIDADE DE PEDIDOS/ENTREGA POR INTERVALO */
            var data = jsonData.VendasTotalAno
            jsonData.VendasTotalAno[0].push({role: 'style'})
            jsonVendasTotalAno = jsonData.VendasTotalAno
            var formatterAno = new google.visualization.NumberFormat({pattern: '####'})
            var formatterValor = new google.visualization.NumberFormat({pattern: 'R$ #,###.00'})

            for (let i = 1; i < jsonVendasTotalAno.length; i++) {
                jsonVendasTotalAno[i].push('color: #222c66')
            }

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

            /* GRÁFICO REFERENTE A QUANTIDADE DE PEDIDOS/RETIRA POR INTERVALO */
            var data = jsonData.VendasTotalMes
            jsonData.VendasTotalMes[0].push({role: 'style'})
            jsonVendasTotalMes = jsonData.VendasTotalMes
            var formatterValor = new google.visualization.NumberFormat({pattern: 'R$ #,###.00'})
            const months = [
                    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
                  ]
            var monthNumber = 1;

            for (let i = 1; i < jsonVendasTotalMes.length; i++) {
                jsonVendasTotalMes[i].push('color: #222c66')
                jsonVendasTotalMes[i][0] = months[i - monthNumber]
            }

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
        }
    })
}