
var fs = require('fs');

exports.index = function() {
    var html = `
    <!DOCTYPE html>
<html>
<head>
	<title>Livro de Odds</title>
	<style>
        html {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 75%;
        }
        
        body {
            margin: 0;
            padding: 0;
            font-family: sans-serif;
            background-color: #024059;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }    
        
		h1 {
			font-size: 3rem;
			font-weight: bold;
			color: #ffffff;
			text-align: center;
			margin-top: 2rem;
		}

		p {
			font-size: 1.2rem;
			color: #ffffff;
			margin: 2rem;
			text-align: center;
			line-height: 1.5;
		}

		.button-container {
			display: flex;
			flex-wrap: wrap;
			justify-content: center;
			margin-top: 2rem;
		}

		.button-container a {
			margin: 1rem;
			padding: 1rem 2rem;
			border: none;
			background-color: #007bff;
			color: white;
			font-size: 1.2rem;
			border-radius: 5px;
			text-decoration: none;
			cursor: pointer;
			transition: all 0.3s ease;
		}

		.button-container a:hover {
			background-color: #0062cc;
			box-shadow: 0 2px 4px rgba(0,0,0,0.4);
		}
	</style>
</head>
<body>
	<h1>Livro de Odds</h1>
	<div class = "p">
	<p>Nesta página, poderás encontrar diversos jogos de futebol das principais ligas de futebol europeias!</p>
    <p>Através desta API, conseguirás comparar as diversas odds de cada jogo apresentadas em diferentes sites de apostas desportivas, para que possas encontrar a melhor odd para apostar!</p>
	</div>
	<div class="button-container">
		<a href="/ligaportuguesa">Liga Portuguesa</a>
		<a href="/ligainglesa">Liga Inglesa</a>
		<a href="/ligaitaliana">Liga Italiana</a>
		<a href="/ligaespanhola">Liga Espanhola</a>
	</div>
</body>
</html>
    `

    return html;
}


exports.liga = function(dados, liga) {
    // dar load a um dicionario apartir do ficheiro dicionario.json
    var dicionario = JSON.parse(fs.readFileSync('dicionario.json', 'utf-8'));
    var names = [];
    var jogos = [];
    var N = 0;
    if (dados.data.length){
        N = dados.data.length;
    }
    for(var i = 0; i < N; i++) {
        fora = dicionario[dados.data[i].jogo.split('§')[1]][0];
        casa = dicionario[dados.data[i].jogo.split('§')[0]][0];
        j = casa+"§"+fora;
        if(names.includes(j))
            continue;
        else{
            names.push(j);
            jogos.push(dados.data[i]);
        }
    }
    dados.data = jogos;

    var html = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>${liga}</title>
        <style>
            /* Define o tamanho mínimo da janela de visualização */
            html, body {
                height: 100%;
            }
            
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #fff;
                display: flex;
                flex-direction: column;
            }
            
            header {
                background-color: #024059;
                color: #fff;
                padding: 20px;
                text-align: center;
            }
            
            footer {
                background-color: #024059;
                color: #fff;
                padding: 10px;
                text-align: center;
                width: 100%;
                height: 2.5rem;
                margin-top: auto; /* Mantém o rodapé no final da página */
            }
            
            h1 {
                text-align: center;
                margin-top: 50px;
                margin-bottom: 30px;
            }
            
            table {
                border-collapse: collapse;
                margin: 20px;
                margin-left: auto;
                margin-right: auto;
                margin-top: 50px;
                width: 80%;
                max-width: 1000px;
                flex: 1; /* Faz com que a tabela ocupe todo o espaço restante */
            }
            
            th, td {
                text-align: center;
                padding: 10px;
                border: 1px solid #ddd;
            }
            
            th {
                background-color: #026873;
                color: #fff;
            }
            
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            
            tr:hover {
                background-color: #ddd;
            }
                </style>
            </head>
            <body>
                <header>
                    <h1>Lista de Jogos da ${liga}</h1>
                </header>
                <table>
                    <thead>
                        <tr>
                            <th>Equipa Casa</th>
                            <th>Equipa Visitante</th>
                            <th>Data</th>
                            <th>Local</th>
                            <th>Consultar Odds</th>
                        </tr>
                    </thead>
                    <tbody>
            `
        var jogos = []
        for (var i = 0; i < dados.data.length; i++) {
            // Verificar se o jogo já foi visto
            if (jogos.indexOf(dados.data[i].jogo) !== -1) {
                continue;
            }
            // Adicionar o jogo ao array de jogos já vistos
            jogos.push(dados.data[i].jogo);
            // Adicionar os elementos da linha da tabela HTML
            html += '<tr>';
            html += '<td>' + dados.data[i].jogo.split('§')[0] + '</td>';
            html += '<td>' + dados.data[i].jogo.split('§')[1] + '</td>';
            html += '<td>' + dados.data[i].data + '</td>';
            html += '<td>' + dados.data[i].local + '</td>';
            html += '<td><a href="/jogo/' + dados.data[i].jogo +'">Consultar Odds</a></td>';
            html += '</tr>';
        }

    html += `
                    </tbody>
                </table>
                <footer>
                    <p>&copy; ${new Date().getFullYear()} Livro de Odds. Todos os direitos reservados.</p>
                </footer>
            </body>
        </html>
        `
    return html;
}

exports.jogo = function(dados) {
    var html = `
    <!DOCTYPE html>
    <html>
        <head>
            <title>Jogo</title>
            <style>
            /* CSS para a página */
            body {
                display: flex;
                flex-direction: column;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            header {
                background-color: #024059;
                color: white;
                padding: 10px;
                text-align: center;
            }
            footer {
                background-color: #024059;
                color: white;
                padding: 10px;
                position: sticky;
                bottom: 0;
                text-align: center;
                width: 100%;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                padding: 8px;
                text-align: center;
                border: 1px solid #ddd;
            }
            th {
                background-color: #026873;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .container {
                background-color: #ffffff;
                padding: 10px;
                margin: 10px;
            }
            main {
                flex: 1; /* Faz com que o main ocupe todo o espaço restante */
            }
            </style>
        </head>
        <body>
            <header>
                <h1>Jogo</h1>
                <h2>${dados[0].jogo.split('§')[0]} vs ${dados[0].jogo.split('§')[1]}</h2>
            </header>
            <main>
            <div class="container">
                <p><b>Equipa da Casa</b>: ${dados[0].jogo.split('§')[0]}</p>
                <p><b>Equipa Fora</b>: ${dados[0].jogo.split('§')[1]}</p>
                <p><b>Data</b>: ${dados[0].data}</p>
                <p><b>Local</b>: ${dados[0].local}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Site</th>
                        <th>Odd - Casa</th>
                        <th>Odd - Empate</th>
                        <th>Odd - Visitante</th>
                    </tr>
                </thead>
                <tbody>
                    ${dados.map(item => `
                        <tr>
                            <td>${item.casa}</td>
                            <td>${item.odd1}</td>
                            <td>${item.oddx}</td>
                            <td>${item.odd2}</td>
                        </tr>
                `).join('')}
                </tbody>
            </table>
            </main>
        <footer>
            <p>&copy; ${new Date().getFullYear()} Livro de Odds. Todos os direitos reservados.</p>
        </footer>
        </body>
    </html>
`
    return html;
}