const express = require('express');
const path = require('path');
const app = express();
const port = 3001;

// Configurar o diretório público para servir arquivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// Roteamento dinâmico para arquivos HTML na pasta 'public/html/pages'
app.get('/*.html', (req, res) => {
  const filePath = path.join(__dirname, 'public', 'html', 'pages', req.path);

  res.sendFile(filePath, err => {
    if (err) {
      res.status(404).send('Página não encontrada');
    }
  });
});

// Roteamento para a página inicial (login)
app.get('/', (req, res) => {
  res.redirect('/Login.html'); // Redireciona para a página Login.html
});

// Iniciar o servidor
app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
