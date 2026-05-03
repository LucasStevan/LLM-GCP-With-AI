<h1 align="center">API de Análise de Dados com BigQuery e LangChain</h1>

<p align="center">
  Documentação de setup, configuração de infraestrutura e execução do projeto utilizando Docker DevContainers para garantir a padronização do ambiente de desenvolvimento.
</p>

<hr>

<h2>1. Configuração do Google Cloud Platform (GCP)</h2>
<p>Antes de rodar a aplicação, é necessário configurar o banco de dados e as credenciais de acesso:</p>
<ol>
  <li>Criamos o ambiente no <b>BigQuery (BQ)</b> dentro do GCP para receber e armazenar os dados.</li>
  <li>Criamos uma <i>Service Account</i> (usuário de serviço) no painel de <b>IAM</b>, atribuindo os cargos e permissões necessárias para leitura e escrita no BQ.</li>
  <li>Geramos uma nova chave para este usuário e baixamos o arquivo <code>.json</code> para o projeto local (esta chave fará a autenticação da nossa API).</li>
</ol>

<h2>2. Pré-requisitos de Infraestrutura</h2>
<p>A aplicação roda de forma isolada (conteinerizada) para evitar conflitos de bibliotecas. Você precisará de:</p>
<ul>
  <li><b>Docker Desktop</b> instalado e rodando em sua máquina.</li>
  <li>Nas configurações do Docker (<i>Engrenagem > General</i>), garanta que a opção <b>"Use the WSL 2 based engine"</b> esteja ativada.</li>
  <li><b>Visual Studio Code (VS Code)</b> instalado.</li>
</ul>

<h2>3. Preparando o Ambiente de Desenvolvimento (VS Code)</h2>
<p>O VS Code precisa das extensões corretas para conseguir "entrar" no contêiner.</p>
<ol>
  <li>Abra o VS Code e vá na aba de Extensões (<code>Ctrl + Shift + X</code>).</li>
  <li>Instale a extensão oficial da Microsoft: <b>Dev Containers</b>.</li>
  <li>Instale a extensão: <b>WSL</b>.</li>
</ol>

<h2>4. Configurando o DevContainer (Primeira Execução)</h2>
<p>Se o projeto acabou de ser clonado e o contêiner não subiu automaticamente, siga os passos:</p>
<ol>
  <li>Abra a pasta do projeto no VS Code.</li>
  <li>Pressione <code>F1</code> (ou <code>Ctrl + Shift + P</code>) para abrir a paleta de comandos.</li>
  <li>Digite e selecione: <b>Dev Containers: Rebuild and Reopen in Container</b>.</li>
</ol>
<blockquote>
  <b>Nota:</b> O VS Code fará o download da imagem do Python 3.12, atualizará o Linux interno e rodará a instalação de todas as bibliotecas do <code>requirements.txt</code> automaticamente. Não é necessário criar <code>.venv</code>.
</blockquote>

<h2>5. Inicializando a Aplicação</h2>
<p>Com o ambiente do contêiner aberto (verifique a barra inferior esquerda do VS Code), nós preparamos os arquivos principais:</p>
<ul>
  <li><code>seed_db.py</code>: Script responsável pela população inicial de dados.</li>
  <li><code>main.py</code>: Código central da nossa API FastAPI.</li>
</ul>

<p>Para ligar o servidor, abra o terminal integrado do VS Code e execute:</p>

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload