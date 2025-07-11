Documentação do Código Python
===

Este documento explica o código Python de forma simples e direta, **callbacks.py**

Visão Geral
---

Este código Python é a "espinha dorsal" de um **painel interativo (dashboard)** feito com a biblioteca Dash. Ele serve para analisar dados de reclamações, provavelmente da Hapvida, disponíveis no site Reclame Aqui.

O principal objetivo é:

* **Carregar e Preparar Dados:** Ler os dados das reclamações (de um arquivo CSV) e informações geográficas dos estados do Brasil (de um arquivo GeoJSON).
* **Criar Gráficos e Mapas:** Gerar visualizações interativas como gráficos de linha (série temporal), barras (frequência por estado e status), histogramas (distribuição do tamanho do texto) e um mapa do Brasil com "heatmap" (mapa de calor) para mostrar a concentração de reclamações.
* **Permitir Interação:** Fazer com que os gráficos e o mapa se atualizem automaticamente quando o usuário selecionar filtros (como ano, estado, status ou tamanho do texto da reclamação) no painel. Isso é feito usando a funcionalidade de "callbacks" do Dash.
* **Gerar Nuvem de Palavras (WordCloud):** Criar uma imagem com as palavras mais frequentes nas reclamações, onde o tamanho da palavra indica sua relevância.


Como Usar
---

Este código não é um programa que você executa diretamente. Ele é parte de um aplicativo Dash maior. Para que ele funcione, você precisa ter um ambiente Python configurado e as bibliotecas necessárias instaladas.

1. **Dependências e Instalação:**

Você vai precisar das seguintes bibliotecas Python. Se não as tiver, pode instalá-las usando o pip:

~~~python
pip install pandas folium plotly geopandas dash
~~~

2. **Estrutura de Pastas (Esperada):**

Para o código funcionar corretamente, você precisa de uma estrutura de pastas específica:seu_projeto/
~~~
├── app.py (onde este código estaria integrado)
├── components/
│   ├── datasets/
│   │   ├── RECLAMEAQUI_HAPVIDA.csv
│   │   └── brasil_estados.json
│   ├── assets/
│   │   ├── mapa_brasil_none.html
│   │   └── mapa_brasil_file.html
│   ├── processamento.py
│   ├── callbacks.py
~~~

* **RECLAMEAQUI_HAPVIDA.csv:** Contém os dados brutos das reclamações. 
* **brasil_estados.json:** Contém os dados geográficos dos estados brasileiros.
* **processamento.py:** É esperado que este arquivo contenha as classes DataProcessing (para processar os dados) e GeoJsonSingleton (para gerenciar o arquivo GeoJSON). Sem essas classes, o código não funcionará.
* **mapa_brasil_none.html e mapa_brasil_file.html:** São arquivos HTML usados para exibir os mapas gerados pelo Folium dentro do aplicativo Dash. Eles são criados e atualizados pelo próprio código.


Funções e Callbacks (Callbacks são funções que respondem a interações do usuário)
---


Este código organiza suas funcionalidades através de callbacks, que são blocos de código que o Dash executa em resposta a uma ação do usuário (como selecionar um filtro).

1. **toggle_navbar**

* O que faz: Controla a exibição de um menu de navegação (navbar) em telas de celular. Quando o ícone de "hambúrguer" (geralmente três linhas) é clicado, ele expande ou recolhe o menu.
* Parâmetros:
  * opened (booleano): Indica se o menu foi "aberto" (clicado).
  * navbar (dicionário): O estado atual do componente navbar no Dash.
* Retorno: O estado atualizado do navbar para o Dash.

2. **update_value_slider**

* O que faz: Atualiza um texto na interface do usuário para mostrar qual faixa de valores foi selecionada em um "slider" (controle deslizante) usado para filtrar o tamanho do texto das reclamações.
* Parâmetros:
  * value (lista de números): Os dois valores (mínimo e máximo) selecionados no slider.
* Retorno: Uma string (texto) formatada que exibe os valores selecionados.

3. **atualizar_mapa**

* O que faz: É a função responsável por gerar e atualizar o mapa do Brasil com o "heatmap" das reclamações, baseado no ano selecionado pelo usuário.
* Parâmetros:
  * ano_mapa (número inteiro): O ano selecionado pelo usuário para filtrar os dados do mapa.Retorno: Um componente html.Iframe que carrega o mapa gerado pelo Folium em um arquivo HTML.
* Detalhes Internos:
  * Cria uma instância da classe DataProcessing para trabalhar com os dados.
  * Se nenhum ano for selecionado, ele exibe um mapa padrão vazio.
  * Usa a biblioteca Folium para criar o mapa interativo.
  * folium.Choropleth: Adiciona a camada de "heatmap" ao mapa, colorindo os estados com base na contagem de  reclamações para o ano escolhido.
  * folium.plugins.Fullscreen: Adiciona um botão para permitir ao usuário visualizar o mapa em tela cheia.folium.LayerControl(): Adiciona um controle para ligar/desligar camadas do mapa (útil se houvesse mais camadas).
  * Salva o mapa gerado em um arquivo HTML (mapa_brasil_file.html ou mapa_brasil_none.html).
  * Exibe esse arquivo HTML dentro do aplicativo Dash usando um Iframe.

4. **atualizar_painel**

* O que faz: Esta é a função mais abrangente. Ela atualiza todos os gráficos principais (série temporal, frequência por estado, frequência por status, distribuição do tamanho do texto) e a nuvem de palavras (WordCloud) com base nos filtros selecionados pelo usuário.

* Parâmetros:

  * estados_selec (lista de strings): Uma lista dos estados selecionados pelo usuário.
  * status_selec (lista de strings): Uma lista dos status de reclamação selecionados pelo usuário.
  * faixa_tamanho (lista de números): Uma lista com o valor mínimo e máximo do tamanho do texto selecionado.

* Retorno: Os objetos figure (para os gráficos Plotly) e src (para a imagem da WordCloud) que o Dash usará para atualizar a interface.

  * Detalhes Internos:

    * Cria uma instância da classe DataProcessing.
    * Filtra os Dados: Aplica os filtros de estado, status e tamanho do texto selecionados pelo usuário nos dados das reclamações.
    * Geração dos Gráficos Plotly:
      * Série Temporal: Gera um gráfico de linha mostrando a contagem de reclamações por mês.
      * Frequência por Estado: Gera um gráfico de barras mostrando o número de reclamações por estado.
      * Frequência por Status: Gera um gráfico de pizza mostrando a distribuição das reclamações por status (ex: "Resolvida", "Não Resolvida").
      * Distribuição do Tamanho do Texto: Gera um histograma mostrando a frequência dos diferentes tamanhos de texto das reclamações.
    * WordCloud: Chama o método data_wordcloud() da classe DataProcessing para gerar a imagem da nuvem de palavras.


Observações Adicionais
---


* Dependência Externa: É crucial que as classes DataProcessing e GeoJsonSingleton estejam definidas no arquivo components/processamento.py. Sem elas, este código não funcionará, pois são elas que fazem o trabalho pesado de carregar e manipular os dados.
* Caminhos de Arquivo: O código usa os.path.join(BASE_DIR, ...) para construir os caminhos dos arquivos. Isso garante que o código funcione em diferentes sistemas operacionais.Dash callback: A @callback é uma característica central do framework 
* Dash. Ela permite criar a interatividade do painel, conectando as entradas do usuário (Inputs) às saídas (Outputs) dos gráficos e elementos da interface.
