# MoniSat

## Visão Geral

O MoniSat é um sistema automatizado para cadastro e extração de dados de motoristas, veículos, reboques, iscas, pontos e rotogramas. Utiliza a biblioteca Playwright para automação de navegação web e manipulação de elementos na página.

## Estrutura do Projeto

```
MoniSat/
├── .vscode/
│   └── settings.json
├── data/
│   ├── cars.csv
│   ├── drivers.csv
│   ├── grids.csv
│   ├── iscas.csv
│   ├── pontos.csv
│   ├── reboques.csv
│   └── retrogramas.csv
├── docs/
│   └── DOCUMENTATION.MD
├── emails/
│   └── email_sender.py
├── main/
│   ├── pages/
│   │   ├── cadastro/
│   │   ├── fillers/
│   │   │   ├── car.py
│   │   │   ├── driver.py
│   │   │   ├── iscas.py
│   │   │   ├── logistica.py
│   │   │   ├── pontos.py
│   │   │   ├── reboque.py
│   │   │   ├── retrograma.py
│   │   ├── grid/
│   │   │   └── gridSat.py
│   │   ├── home/
│   │   │   └── scrapper.py
│   ├── SuperClassMoni.py
│   └── uteis.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── runner.py
```

## Instalação

1. Clone o repositório:

   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd MoniSat
   ```

2. Crie um ambiente virtual e ative-o:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente no arquivo

.env

:
`properties     GERAL=BMG     LOGIN=RENES     SENHA=OUVERNEY     EMAIL=     PASSWD=     ADDRESS=     `

## Uso

### Executando o Runner

O arquivo

runner.py

é responsável por agendar e executar os scripts de cadastro e extração de dados.

```sh
python runner.py
```

### Estrutura dos Dados

Os dados são armazenados em arquivos CSV na pasta

data

. Cada tipo de dado possui seu próprio arquivo CSV:

cars.csv

## : Dados de veículos

drivers.csv

## : Dados de motoristas

grids.csv

## : Dados de grids

iscas.csv

## : Dados de iscas

pontos.csv

## : Dados de pontos

reboques.csv

## : Dados de reboques

retrogramas.csv

: Dados de retrogramas

### Funções Principais

#### Cadastro

As funções de cadastro estão localizadas na pasta

fillers

. Cada arquivo corresponde a um tipo de cadastro:

car.py

## : Cadastro de veículos

driver.py

## : Cadastro de motoristas

iscas.py

## : Cadastro de iscas

logistica.py

## : Cadastro de logística

pontos.py

## : Cadastro de pontos

reboque.py

## : Cadastro de reboques

retrograma.py

: Cadastro de rotogramas

#### Extração

As funções de extração estão localizadas na pasta

grid

e

home

:

gridSat.py

## : Extração de dados de grids

scrapper.py

: Extração de dados gerais

### Exemplo de Uso

#### Cadastro de Motorista

```python
from main.pages.fillers.driver import fill_driver

params_driver = {
    "nome": "João da Silva",
    "rg": "123456789",
    "cpf": "123.456.789-00",
    "cnh": "12345678901",
    "tipo": "A",
    "pussoui_pass": "Sim",
    "consulta": "2024-06-01",
    "validade": "2025-06-01",
    "status": "Ativo",
    "referencia": "Ref_CAR_001"
}

fill_driver(page_monisat, **params_driver)
```

#### Extração de Dados de Grid

```python
from main.pages.grid.gridSat import GridMoniSAT

handler = GridMoniSAT()
handler.extrator_to_grid(map_=True, list_results=True)
```

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça um push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.
