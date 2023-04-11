var http = require('http');
var fs = require('fs');
var url = require('url');
var axios = require('axios');
var templates = require('./templates');
var querystring = require('querystring');
var { parse } = require('querystring');
var static = require('./static');

// dar load a um dicionario apartir do ficheiro dicionario.json
var dicionario = JSON.parse(fs.readFileSync('dicionario.json', 'utf-8'));

var servidor = http.createServer((req, res) => {
    if(static.staticResource(req)){
        static.serveStaticResource(req, res)
    }
    else{
        switch (req.method) {
            case 'GET':
                if (req.url == '/') {
                        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                        res.write(templates.index());
                        res.end();
                }
                else if (req.url == '/ligaportuguesa') {
                        axios.get('http://localhost:3000/jogos?liga=Liga%20Portuguesa').then(dados => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write(templates.liga(dados, "Liga Portuguesa"));
                            res.end();
                        }).catch(erro => {
                            console.log(erro)
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write("Não foi possível obter os dados da Liga Portuguesa.");
                            res.end();
                        })
                }
                else if (req.url == '/ligainglesa') {
                        axios.get('http://localhost:3000/jogos?liga=Liga%20Inglesa').then(dados => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write(templates.liga(dados, "Liga Inglesa"));
                            res.end();
                        }).catch(erro => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write("Não foi possível obter os dados da Liga Inglesa.");
                            res.end();
                        })
                }
                else if (req.url == '/ligaitaliana') {
                        axios.get('http://localhost:3000/jogos?liga=Liga%20Italiana').then(dados => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write(templates.liga(dados, "Liga Italiana"));
                            res.end();
                        }).catch(erro => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write("Não foi possível obter os dados da Liga Italiana.");
                            res.end();
                        })
                }
                else if (req.url == '/ligaespanhola') {
                        axios.get('http://localhost:3000/jogos?liga=Liga%20Espanhola').then(dados => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write(templates.liga(dados, 'Liga Espanhola'));
                            res.end();
                        }).catch(erro => {
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write("Não foi possível obter os dados da Liga Espanhola.");
                            res.end();
                        })
                }
                else if (req.url.startsWith("/jogo/")) {
                    game = req.url.split('/')[2];
                    game = decodeURI(game)
                    var home = game.split('§')[0];
                    var away = game.split('§')[1];
                    var names = [];
                    names = names.concat(dicionario[home]);
                    names = names.concat(dicionario[away]);
                    axios.get('http://localhost:3000/jogos/').then(dados => {
                        var jogos = [];
                        dados.data.forEach(j => {
                            var casa = j['jogo'].split('§')[0];
                            var fora = j['jogo'].split('§')[1];
                            if (names.includes(casa) && names.includes(fora)) {
                                jogos.push(j);
                            }
                        })
                        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                        res.write(templates.jogo(jogos));
                        res.end();
                    }).catch(erro => {
                        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                        res.write("Não foi possível obter os dados do jogo.");
                        console.log(erro);
                        res.end();
                    })
    }
}}});


servidor.listen(7777);