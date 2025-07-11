Dashboard de Reclamações do Hapvida
===

Este projeto é um painel interativo (dashboard) feito em Python usando a biblioteca Dash. Ele foi criado para analisar dados de reclamações da Hapvida que foram coletadas do site Reclame Aqui. Com este dashboard, você pode explorar as reclamações de várias maneiras, como ver a distribuição do tamanho dos textos, acompanhar a evolução das reclamações ao longo do tempo, verificar a frequência dos diferentes status (resolvido, não resolvido, etc.), visualizar uma nuvem de palavras com os termos mais usados e até mesmo um mapa do Brasil mostrando onde as reclamações são mais concentradas por estado.

#### Sobre o Projeto


Este dashboard foi desenvolvido como parte do MBA em Ciência de Dados, especificamente para a disciplina de Dashboards em Python, ministrada pelo Prof. Túlio Ribeiro.


Como Usar
---


Você vai precisar das seguintes bibliotecas Python. Se não as tiver, pode instalá-las usando o pip:

~~~python
pip install dash dash-mantine-components pandas dash-iconify
~~~


Funcionalidades Principais
---

O layout do seu dashboard é dividido em algumas partes importantes para facilitar a navegação e a visualização dos dados:

* Topo da Página (Cabeçalho):
  * Título: "Dashboard - Reclame Aqui" em destaque.
  * Botão "About": Ao passar o mouse sobre ele, aparece uma pequena janela com informações sobre o projeto, incluindo o nome do curso, a disciplina e o professor.

* Menu Lateral (Barra de Navegação):

  * Filtro por Estado: Você pode selecionar um ou mais estados para ver as reclamações apenas daquela região.
  * Filtro por Status: Permite escolher um ou mais status das reclamações (por exemplo, "Resolvido", "Não   Resolvido", "Em Análise") para focar sua análise.
  * Seleção de Ano (para o mapa): Um menu suspenso para escolher um ano específico e ver como as reclamações   se distribuem no mapa do Brasil naquele período.
  * Filtro de Tamanho do Texto: Um controle deslizante (slider) que permite definir um intervalo mínimo e máximo para o número de palavras nas reclamações. Isso ajuda a focar em textos mais curtos ou mais longos.

* Área Principal (Conteúdo): É onde todos os gráficos e visualizações são exibidos. Eles são organizados em uma grade para melhor aproveitamento do espaço e incluem:

  * Gráfico de Distribuição do Texto: Mostra como os tamanhos dos textos das reclamações estão distribuídos.
  * Gráfico de Série Temporal: Apresenta a quantidade de reclamações ao longo do tempo, permitindo identificar   tendências.
  * Gráfico de Frequência de Status: Um gráfico que mostra a proporção de cada tipo de status das reclamações.
  * Nuvem de Palavras: Uma imagem que destaca as palavras mais frequentes nas reclamações, dando uma ideia   rápida dos temas mais abordados.
  * Mapa de Calor do Brasil: Um mapa interativo que usa cores para indicar a concentração de reclamações em   cada estado brasileiro.
  * Gráfico de Frequência por Estado: Detalha a quantidade de reclamações por cada estado.

Todos os gráficos nesta área principal possuem um indicador de carregamento, o que significa que enquanto os dados são processados e os gráficos são gerados, você verá um sinal de que algo está acontecendo, melhorando a experiência do usuário.

Estrutura do Código
---


O código que você forneceu é responsável por montar o layout visual do dashboard. Vamos entender as partes principais:

* Importações: No início do código, são importadas as bibliotecas necessárias:

  * os: Para lidar com caminhos de arquivos.
  * dash_mantine_components as dmc: Componentes visuais bonitos e modernos para o Dash.
  * pandas as pd: Para trabalhar com os dados (tabelas).
  * dash (dcc, html): Componentes básicos do Dash para criar o layout.
  * dash_iconify: Para usar ícones no dashboard.
  * DataProcessing de components.processamento: Uma classe que (presumimos) faz o tratamento inicial dos dados.

* Carregamento e Preparação dos Dados:

  * BASE_DIR = os.getcwd(): Descobre onde o seu código está rodando.
  * FILE_PATH_DATASET: Monta o caminho completo para o arquivo RECLAMEAQUI_HAPVIDA.csv, que deve estar dentro   da pasta components/datasets.
  * df = DataProcessing(...).data_texto(): Carrega o arquivo CSV e, em seguida, usa a classe DataProcessing para fazer algum tipo de pré-processamento nos dados, especificamente para textos.

* Informações "About":
  * A variável about guarda o texto que aparece quando você passa o mouse sobre o botão "About" no cabeçalho. É um texto formatado em Markdown.

* Função body():

  * Esta função é a "receita" de como o seu dashboard será montado.
  * Ela retorna um dmc.AppShell, que é como uma "concha" para sua aplicação, definindo as áreas   do cabeçalho, menu lateral e conteúdo principal.
  * Dentro dela, são configurados todos os filtros e os espaços onde os gráficos serão exibidos.

