Trabalho para disciplina Introdução a python - Ciencia de Dados.
===

Projeto de T1 - Contratos de Energia.
===

Atividade
===

Dado um arquivo de entrada, implemente um algoritmo que inicialize uma matriz tridimensional
que armazene os valores dos contratos de energia. A matriz deve ter as dimensões n × (m + 1) ×
(m + 1), onde cada elemento contratos[fornecedor][inicio][fim] representa o valor do contrato
oferecido pelo fornecedor para o período do mês inicial ao mês final. Se não houver contrato
específico para esse período, o valor deve ser ∞ (infinito).

Tabela de conteúdos
---
<!--ts-->   
   * [Tecnologias](#🛠-tecnologias-utilizadas)
   * [Criação Virtualenv](#criação-virtualenv)
   * [Instalação Pacotes](#instalação-de-pacotes)
   * [Acessando Virtualenv](#acessando-virtualenv---wsl-linux)
   * [Executando Aplicação](#execução-da-aplicação)
   * [Codigo](#código)     
   * [Referências](#referências)
   * [Contribuição](#contribuição)
   * [Autor](#autor)
   * [Licença](#licença)
<!--te-->

🛠 Tecnologias Utilizadas
---
As seguintes ferramentas foram usadas na construção do projeto:

- [Python 3.13.0](https://docs.python.org/pt-br/3/)
- [dash==2.18.2](https://dash.plotly.com/)
- [dash_mantine_components==0.15.3](https://www.dash-mantine-components.com/)

Criação Virtualenv
---


~~~bash
python3 -m venv .venv
~~~


Acessando Virtualenv - WSL, Linux
---


~~~bash
source .venv/bin/activate
~~~


Acessando Virtualenv - Windows
---


~~~bash
.venv/Scripts/activate.bat
~~~


Instalação de Pacotes
---


~~~bash
python -m pip install -r requirements.txt
~~~

Execução da Aplicação
---

~~~python
cd dash-t2
python app.py
~~~

Código
---

Trabalhando nisso !!!

### Referências
---

- [Python Documentação](https://docs.python.org/pt-br/3/)
- [Dash Bootstrap](https://dash.plotly.com/)
- [Dash Mantine](https://www.dash-mantine-components.com/)


### Contribuições

- Emerson da Silva Maciel
- Victor Lamark Costa Brasil
- Wagner da Costa Oliveira

### Autores

- Emerson da Silva Maciel
- Victor Lamark Costa Brasil
- Wagner da Costa Oliveira

### Licença

- [GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.html)