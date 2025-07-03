📌 PROJETO – DASHBOARD COM DADOS DO RECLAME AQUI
===

MBA em Ciência de Dados – Disciplina: Dashboards em Python
---
Prof. Túlio Ribeiro


**Descrição**
---

* O objetivo é criar um painel interativo com **Dash** ou **Streamlit** utilizando dados de reclamações do Reclame Aqui.
* Cada equipe deverá escolher **uma** das seguintes empresas para análise: **Hapvida**, **Nagem** ou **Ibyte**.
* Será permitido o uso de outro dataset similar aos disponibilizados, a critério da equipe.
* A equipe deverá ser composta por no máximo 4 integrantes.
* A entrega do trabalho consiste em:

  * O **deploy da aplicação** (ver seção abaixo);
  * Um **vídeo de até 5 minutos** explicando o funcionamento do dashboard e os principais insights obtidos.

    > **Obs:** Não é obrigatório que todos os membros da equipe falem no vídeo — isso fica a critério do grupo.

### **O painel deve conter**

* **Série temporal** do número de reclamações.
* **Frequência de reclamações por estado.**
* **Frequência por tipo de** `STATUS`.
* **Distribuição do tamanho dos textos** das reclamações (coluna `DESCRIÇÃO`).
* **WordCloud** com as palavras mais frequentes nos textos das descrições.
* **Mapa do Brasil com heatmap** mostrando a quantidade de reclamações por **ano**, com granularidade por **estado ou município**.

  > O mapa **deve conter um seletor para o ano** que será visualizado.

### **Os gráficos devem ser interativos e filtráveis com seletores de:**

* Estado
* Status
* Faixa de tamanho do texto da reclamação

### **Deploy da aplicação**

**Tutoriais para deploy com Streamlit:**

* [https://youtu.be/vw0I8i7QJRk?si=LthbxLEMj3d\_TXZC](https://youtu.be/vw0I8i7QJRk?si=LthbxLEMj3d_TXZC)
* [https://youtu.be/HKoOBiAaHGg?si=euvQ709gIg3mnjWG](https://youtu.be/HKoOBiAaHGg?si=euvQ709gIg3mnjWG)

**Tutorial para deploy com Dash:**

* [https://youtu.be/H16dZMYmvqo?si=jLhcetE8YxJnTO9x](https://youtu.be/H16dZMYmvqo?si=jLhcetE8YxJnTO9x)



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

Referências
---

- [Python Documentação](https://docs.python.org/pt-br/3/)
- [Dash Bootstrap](https://dash.plotly.com/)
- [Dash Mantine](https://www.dash-mantine-components.com/)


Contribuições
---

- Emerson da Silva Maciel
- Victor Lamark Costa Brasil
- Wagner da Costa Oliveira

Autores
---

- Emerson da Silva Maciel
- Victor Lamark Costa Brasil
- Wagner da Costa Oliveira

Licença
---

- [GNU General Public License (GPL)](https://www.gnu.org/licenses/gpl-3.0.html)