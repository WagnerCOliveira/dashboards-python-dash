Documentação do Código Python
===

Visão Geral
---


Este documento descreve o código Python fornecido, que é composto por duas classes: GeoJsonSingleton e DataProcessing. O objetivo principal deste código é carregar dados geográficos e processar um DataFrame (tabela de dados) relacionado a reclamações, provavelmente do site Reclame Aqui sobre a Hapvida.


Dependências e Instalação:
---

Você vai precisar das seguintes bibliotecas Python. Se não as tiver, pode instalá-las usando o pip:

~~~python
pip install nltk wordcloud
~~~

GeoJsonSingleton
---

Esta classe garante que o arquivo GeoJSON (um formato para armazenar dados geográficos) seja carregado apenas uma vez, mesmo que você tente acessá-lo várias vezes. Isso é útil para economizar memória e tempo, especialmente em aplicações onde o mesmo dado é necessário em diferentes partes do código.

Como funciona?

* _instance = None: Uma variável interna da classe que guarda a única instância do GeoJSON carregado. Ela começa como None (vazia).
* __new__(cls): Este método especial é chamado antes de criar uma nova instância da classe.
  * Ele verifica se _instance ainda é None.
  * Se for None, significa que o GeoJSON ainda não foi carregado. Então, ele:
    * Define BASE_DIR como o diretório atual do seu projeto.
    * Cria o caminho completo para o arquivo brasil_estados.json, que se espera estar em components/datasets/brasil_estados.json em relação ao seu diretório base.
    * Abre e carrega o conteúdo do arquivo brasil_estados.json usando json.load().
    * Armazena o GeoJSON carregado em _instance.
  * Finalmente, ele retorna a única instância do GeoJSON (_instance), seja ela recém-carregada ou já existente.


DataProcessing
---

Esta classe é responsável por limpar, transformar e preparar os dados de um DataFrame para análise e visualização. Ela foi projetada para trabalhar com dados de reclamações do Reclame Aqui, especificamente da Hapvida.

1. __init__(self, df)

O construtor da classe é o primeiro método a ser executado quando você cria um objeto DataProcessing. Ele realiza as seguintes operações no DataFrame fornecido (df):

* Divide a coluna 'LOCAL': A coluna LOCAL, que contém dados no formato "Cidade - UF" (ex: "Fortaleza - CE"), é dividida em duas novas colunas: CIDADE e ESTADO.
* Calcula o tamanho do texto: Uma nova coluna chamada TAMANHO_TEXTO é criada, contendo o número de caracteres na coluna DESCRICAO (descrição da reclamação).
* Remove linhas sem estado: Linhas onde a coluna ESTADO é -- (indicando um estado inválido ou ausente) são removidas do DataFrame.
* Converte a coluna 'ANO' para texto: A coluna ANO é convertida para o tipo texto (str).

Métodos de Geração de Dados para Gráficos

A classe DataProcessing possui vários métodos que preparam os dados para diferentes tipos de visualizações:

2. series_temporal(self)

* Finalidade: Gera dados para criar um gráfico de série temporal.
* O que faz: Agrupa os dados pela coluna MES (mês) e conta quantas reclamações existem para cada mês, retornando um DataFrame com MES e CONTAGEM.

3. data_estado(self)

* Finalidade: Gera dados para um gráfico de reclamações por estado.
* O que faz: Conta a frequência de cada estado na coluna ESTADO e retorna um DataFrame com a contagem de reclamações por estado.

4. data_status(self)

* Finalidade: Gera dados para um gráfico de distribuição por status da reclamação.
* O que faz: Conta a frequência de cada STATUS (status da reclamação) e retorna um DataFrame com a contagem de reclamações por status.

5. data_texto(self)

* Finalidade: Retorna o DataFrame completo, que já contém a coluna TAMANHO_TEXTO, para um gráfico de distribuição do tamanho do texto das reclamações.

6. data_mapa(self, ano_mapa: str | None)

* Finalidade: Prepara os dados para um gráfico de mapa do Brasil, exibindo a contagem de reclamações por estado.

* ano_mapa: Um parâmetro opcional que permite filtrar os dados por ano. Se for fornecido, apenas as reclamações daquele ano serão consideradas.

* O que faz:

  * Define um dicionário dict_estados com as siglas e nomes completos de todos os estados brasileiros.
  * Filtra o DataFrame pelo ano_mapa (se fornecido) e agrupa os dados por ESTADO, contando o número de reclamações.
  * Completa estados sem dados: Se ano_mapa for fornecido, ele verifica quais estados não aparecem nos dados filtrados e adiciona-os ao DataFrame com uma contagem de 0, garantindo que todos os estados sejam exibidos no mapa.
  * Adiciona uma nova coluna NOME ao DataFrame resultante, com os nomes completos dos estados, usando o dicionário dict_estados.

7. data_wordcloud(self)

* Finalidade: Gera uma nuvem de palavras (word cloud) a partir das descrições das reclamações.

* O que faz:
  
  * Stopwords: Carrega uma lista de "stopwords" (palavras comuns que não adicionam muito significado, como "e", "o", "de") em português do pacote nltk.
  * Adiciona uma lista personalizada de stopwords relacionadas a planos de saúde e termos muito comuns em reclamações (stopwords_planos_saude) para garantir que palavras irrelevantes sejam removidas.
  * Combina todas as descrições das reclamações em um único texto grande.
  * Cria uma WordCloud com as seguintes configurações:
    * width, height, background_color: Define as dimensões e cor de fundo da imagem da nuvem.
    * stopwords: Usa as stopwords combinadas para remover palavras indesejadas.
    * colormap='viridis': Define o esquema de cores das palavras.
    * max_words=50: Limita o número de palavras exibidas na nuvem para as 50 mais frequentes.
  * Salva a imagem da WordCloud em um formato PNG na memória.
  * Converte a imagem para uma string Base64, que pode ser facilmente incorporada em páginas web ou outros documentos.