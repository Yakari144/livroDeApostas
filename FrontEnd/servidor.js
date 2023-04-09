var http = require('http');
var fs = require('fs');
var url = require('url');
var axios = require('axios');
var templates = require('./templates');
var querystring = require('querystring');
var { parse } = require('querystring');
var static = require('./static');


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
                            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                            res.write("Não foi possível obter os dados da Liga Portuguesa.");
                            res.end();
                        })
                }
                else if (req.url == '/ligainglesa') {
                        axios.get('http://localhost:3000/jogos?liga=Liga%20Inglesa').then(dados => {
                            console.log(dados.data);
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
                    axios.get('http://localhost:3000/jogos?jogo=' + req.url.split('/')[2]).then(dados => {
                        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                        res.write(templates.jogo(dados));
                        res.end();
                    }).catch(erro => {
                        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
                        res.write("Não foi possível obter os dados do jogo.");
                        res.end();
                    })
    }
}}});


servidor.listen(7777);