# Documentação MoniSat - Web Scraper para Sistema de Monitoramento

## Visão Geral

O MoniSat é um sistema automatizado para extração de dados de motoristas, veículos, reboques, iscas, pontos e rotogramas. Utiliza a biblioteca Playwright para automação de navegação web e captura de dados do sistema MoniSat. Os dados extraídos são exportados em arquivos CSV e enviados por email conforme agendamento.

## Estrutura do Projeto

```
MoniSat/
├── .vscode/               # Configurações do VSCode
├── data/                  # Arquivos CSV gerados
│   ├── cars.csv          # Dados de veículos
│   ├── checklist.csv     # Dados de checklist
│   ├── drivers.csv       # Dados de motoristas
│   ├── grids.csv         # Dados de grids/posições
│   ├── iscas.csv         # Dados de rastreadores redundantes
│   ├── phones.csv        # Dados de telefones
│   ├── pontos.csv        # Dados de pontos/locais
│   ├── reboques.csv      # Dados de reboques/semi-reboques
│   └── retrogramas.csv   # Dados de rotogramas
├── docs/                  # Documentação do projeto
│   └── DOCUMENTATION.MD  # Arquivo principal de documentação
├── cards/                 # Capturas de tela do sistema (screenshots)
├── main/                  # Código-fonte principal
│   ├── emails/           # Módulos para envio de emails
│   │   └── email_sender.py
│   ├── pages/            # Módulos de scraping para diferentes páginas
│   │   ├── checklist/    # Extração de checklists
│   │   ├── fillers/      # Extratores de dados
│   │   │   ├── car.py    # Extração de veículos
│   │   │   ├── driver.py # Extração de motoristas
│   │   │   ├── filler.py # Controlador central
│   │   │   ├── iscas.py  # Extração de iscas
│   │   │   ├── logistica.py # Extração de logística
│   │   │   ├── phones.py # Extração de telefones
│   │   │   ├── pontos.py # Extração de pontos
│   │   │   ├── reboque.py # Extração de reboques
│   │   │   └── retrograma.py # Extração de rotogramas
│   │   ├── grid/         # Extração de dados de grade
│   │   │   └── gridSat.py
│   │   └── home/         # Extração de dados da página inicial
│   │       └── scrapper.py
│   ├── SuperClassMoni.py # Classe base com funcionalidades comuns
│   └── uteis.py         # Funções utilitárias
├── .env                  # Variáveis de ambiente (credenciais)
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Instruções básicas
├── requirements.txt      # Dependências do projeto
└── runner.py             # Script principal para agendar execuções
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
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente no arquivo .env:

   ```properties
   GERAL=BMG               # Empresa no sistema MoniSat
   LOGIN=USUARIO           # Usuário de acesso
   SENHA=SENHA_ACESSO      # Senha de acesso
   EMAIL=email@origem.com  # Email para envio dos dados
   PASSWD=senha_email      # Senha do email
   ADDRESS=email@destino.com # Email de destino dos dados
   ```

## Uso

### Executando o Runner

O arquivo runner.py é responsável por agendar e executar os scripts de extração de dados em horários predefinidos.

```sh
python runner.py
```

O runner contém agendamentos para:

- Extrair dados de grid a cada 30 minutos
- Extrair telefones de motoristas às 11:56 e 16:45 diariamente
- Extrair dados de veículos, motoristas e reboques às 08:01 e 17:00 diariamente
- Extrair dados de checklist às 08:06 diariamente

### Dados Extraídos

Os dados são armazenados em arquivos CSV na pasta data:

- **cars.csv**: Dados de veículos (placa, situação, tipo, categoria, rastreador, etc.)
- **drivers.csv**: Dados de motoristas (nome, RG, CPF, CNH, validade, etc.)
- **grids.csv**: Dados de posicionamento e status (placa, motorista, localização, situação)
- **iscas.csv**: Dados de rastreadores redundantes (nome, marca, site, telefone)
- **phones.csv**: Dados de telefones de motoristas (números, identificadores, nomes)
- **pontos.csv**: Dados de pontos/locais (nome, cidade, tipo, raio)
- **reboques.csv**: Dados de reboques (placa, chassi, renavam, marca, etc.)
- **retrogramas.csv**: Dados de rotogramas (id, descrição, distância, autor)
- **checklist.csv**: Dados de checklist de veículos (placa, status, validade, resultado)

### Principais Funcionalidades

#### Extração de Dados de Grid

A função `extrator_to_grid()` no arquivo gridSat.py permite extrair dados da grade de posicionamento:

```python
from main.pages.grid.gridSat import GridMoniSAT

handler = GridMoniSAT()
handler.extrator_to_grid(map_=True, list_results=True)
```

Parâmetros:

- **map\_** (`bool`): Se `True`, captura screenshot do mapa. Default: `True`
- **list_results** (`bool` | `dict`): Se `True`, extrai a lista completa. Se um dicionário, aplica filtros. Default: `True`

Exemplos de uso:

**Extração do Mapa e Lista Completa**

```python
extrator_to_grid(map_=True, list_results=True)
```

**Extração Somente da Lista com Filtros**

```python
extrator_to_grid(
    map_=False,
    list_results={
        "placa": "ABC1234",
        "carreta": "XYZ5678",
        "moto": "NOME_MOTORISTA",
        "loc": "São Paulo",
    }
)
```

**Apenas Mapa (Sem Lista)**

```python
extrator_to_grid(map_=True, list_results=False)
```

#### Extração de Motoristas

A função `fill_driver()` em driver.py extrai dados de motoristas:

```python
from main.pages.fillers.driver import fill_driver

# Exemplo de uso básico - extrai todos os motoristas
fill_driver(page_monisat)

# Exemplo com filtros
fill_driver(
    page_monisat,
    nome="João",
    cpf="123.456.789-00",
    status="VIGENTE"
)
```

#### Extração de Veículos

A função `fill_car()` em car.py extrai dados de veículos:

```python
from main.pages.fillers.car import fill_car

# Extração básica
fill_car(page_monisat)

# Extração com filtros
fill_car(
    page_monisat,
    placa="ABC1234",
    situacao="Ativo",
    tipo="Frota"
)
```

#### Extração de Reboques

A função `fill_reboque()` em reboque.py extrai dados de reboques:

```python
from main.pages.fillers.reboque import fill_reboque

# Extração básica
fill_reboque(page_monisat)

# Extração com filtros
fill_reboque(
    page_monisat,
    placa_reboque="XYZ5678",
    status="VIGENTE"
)
```

#### Extração de Pontos

A função `fill_pontos()` em pontos.py extrai dados de pontos/locais:

```python
from main.pages.fillers.pontos import fill_pontos

# Extração básica com mapa
fill_pontos(page_monisat, mapa=True)

# Extração filtrada
fill_pontos(
    page_monisat,
    ponto="POSTO",
    tipo="ABASTECIMENTO",
    mapa=False
)
```

#### Extração de Telefones

A função `get_all_phones()` em phones.py extrai números de telefone dos motoristas:

```python
from main.pages.fillers.phones import get_all_phones

get_all_phones()  # Extrairá todos os telefones para phones.csv
```

#### Extração de Checklist

A classe `Checklist` em checklist.py extrai dados de checklist de veículos:

```python
from main.pages.checklist.checklist import Checklist

checklist = Checklist()
checklist.extract_checklist()  # Exporta para checklist.csv
```

## Agendamento e Envio de Emails

O script runner.py agenda a execução das extrações e o envio dos resultados por email.

Função para envio de email:

```python
sender_emails_for(
    tittle="Grid",           # Título do email
    to_address="destino@email.com",
    files=["grids.csv"]      # Arquivos a serem anexados
)
```

O script está configurado para extrair e enviar emails em horários predefinidos, e somente funciona entre 8:00 e 18:00.

## Observações Importantes

1. O sistema não realiza cadastros, apenas extrações de dados.
2. Os dados são salvos em CSVs na pasta data.
3. Screenshots de confirmação são salvos na pasta cards.
4. O agendamento é feito via biblioteca `schedule` no arquivo runner.py.
5. As extrações funcionam somente em horário comercial (8h às 18h).

## Requisitos do Sistema

- Python 3.8+
- Playwright
- Pandas
- Schedule
- Python-dotenv

Estas dependências estão listadas no arquivo requirements.txt.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça um push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.
