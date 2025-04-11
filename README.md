# MoniSat - Sistema de Extração de Dados

## Visão Geral

O MoniSat é um sistema automatizado para extração de dados de motoristas, veículos, reboques, iscas, pontos e rotogramas do sistema MoniSat. O projeto utiliza a biblioteca Playwright para automação web, capturando dados e exportando-os em arquivos CSV.

## Objetivos do Projeto

- Extrair dados do sistema MoniSat automaticamente
- Armazenar informações em arquivos CSV estruturados
- Enviar os resultados por email conforme agendamento
- Facilitar o acesso a informações de frotas e motoristas

## Estrutura do Projeto

```
MoniSat/
├── data/                  # Arquivos CSV gerados
│   ├── cars.csv          # Veículos
│   ├── checklist.csv     # Checklists de veículos
│   ├── drivers.csv       # Motoristas
│   ├── grids.csv         # Posicionamentos
│   ├── iscas.csv         # Rastreadores redundantes
│   ├── phones.csv        # Telefones dos motoristas
│   ├── pontos.csv        # Locais/pontos
│   ├── reboques.csv      # Reboques/semi-reboques
│   └── retrogramas.csv   # Rotogramas
├── cards/                 # Capturas de tela
├── main/                  # Código-fonte principal
│   ├── emails/           # Módulos de email
│   ├── pages/            # Módulos de scraping
│   ├── SuperClassMoni.py # Classe base
│   └── uteis.py          # Funções utilitárias
├── docs/                  # Documentação
├── .env                  # Variáveis de ambiente
└── runner.py             # Script de agendamento
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

4. Configure o arquivo .env:
   ```properties
   GERAL=EMPRESA        # Empresa no sistema MoniSat
   LOGIN=USUARIO        # Usuário de acesso
   SENHA=SENHA          # Senha de acesso
   EMAIL=origem@email.com    # Email para envio
   PASSWD=senha_email        # Senha do email
   ADDRESS=destino@email.com # Email destinatário
   ```

## Uso

### Executando o Runner

O script runner.py gerencia o agendamento das extrações:

```sh
python runner.py
```

Os dados coletados são armazenados em arquivos CSV na pasta data e enviados por email conforme programado.

### Agendamento Atual

- Dados de grid: a cada 30 minutos
- Telefones de motoristas: às 11:56 e 16:45 diariamente
- Veículos e motoristas: às 08:01 e 17:00 diariamente
- Checklists de veículos: às 08:06 diariamente

### Extração de Grid (Exemplo)

```python
from main.pages.grid.gridSat import GridMoniSAT

handler = GridMoniSAT()
handler.extrator_to_grid(map_=True, list_results=True)
```

#### Parâmetros

| Parâmetro      | Tipo          | Descrição                                             |
| -------------- | ------------- | ----------------------------------------------------- |
| `map_`         | `bool`        | Captura o mapa se `True`                              |
| `list_results` | `bool`/`dict` | `True` para lista completa, ou dicionário com filtros |

#### Exemplos de Filtros

```python
list_results = {
    "placa": "ABC1234",       # Filtra por placa
    "carreta": "XYZ5678",     # Filtra por carreta
    "moto": "NOME_MOTORISTA", # Filtra por motorista
    "loc": "São Paulo"        # Filtra por localização
}
```

## Limitações

- O sistema opera apenas em horário comercial (8h às 18h)
- Focado exclusivamente na extração de dados, não realiza cadastros
- Necessita de acesso válido ao sistema MoniSat

## Requisitos

- Python 3.8+
- Playwright
- Pandas
- Schedule
- Python-dotenv

## Observações

- Screenshots de confirmação são salvos na pasta cards
- Os dados são exportados em formato CSV para integrações
- O sistema funciona melhor com navegador Chrome instalado

---

Para detalhes completos sobre as funções e suas opções, consulte a documentação no diretório docs.
