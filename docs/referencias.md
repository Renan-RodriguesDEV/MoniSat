Abaixo segue exemplos de dicionários para cada parâmetro da função `process_cadastro`. Esses exemplos podem ser utilizados nas requisições da API, servindo como referência clara de como os dados devem ser formatados para cada tipo de cadastro:

---

### Exemplo de Dicionário para `params_driver` (Cadastro de Motorista)

```python
params_driver = {
    "nome": "João da Silva",
    "rg": "123456789",
    "cpf": "123.456.789-00",
    "cnh": "12345678901",
    "tipo": "A",  # Categoria da CNH
    "pussoui_pass": "Sim",
    "consulta": "2024-06-01",  # Data da consulta
    "validade": "2025-06-01",  # Validade da CNH
    "status": "Ativo",
    "referencia": "Ref_12345"
}
```

---

### Exemplo de Dicionário para `params_car` (Cadastro de Veículo)

```python
params_car = {
    "placa": "ABC-1234",
    "situacao": "Em operação",
    "tipo": "Caminhão",
    "categoria": "Pesado",
    "rastreador": "Rastreador_12345",
    "n_antena": "Antena_001",
    "semi_reboque": "XYZ-5678",
    "motorista": "João da Silva",
    "operacao": "Logística",
    "consulta": "2024-06-15",
    "validade": "2025-06-15",
    "status": "Ativo",
    "referencia": "Ref_CAR_001"
}
```

---

### Exemplo de Dicionário para `params_reboque` (Cadastro de Reboque)

```python
params_reboque = {
    "placa_reboque": "XYZ-5678",
    "chassi": "9BWZZZ377VT123456",
    "renavam": "98765432101",
    "subcategoria": "Tanque",
    "marca": "Randon",
    "consulta": "2024-06-20",
    "validade": "2026-06-20",
    "status": "Ativo",
    "referencia": "Ref_REBOQUE_002"
}
```

---

### Exemplo de Dicionário para `params_iscas` (Cadastro de Iscas/Redundantes)

```python
params_iscas = {
    "nome": "Isca Modelo X",
    "marca": "Tracker",
    "site": "https://www.iscas.com",
    "telefone": "(11) 98765-4321",
    "login": "user123",
    "senha": "pass123",
    "obs": "Instalação realizada em 2024-05-10"
}
```

---

### Exemplo de Dicionário para `params_pontos` (Cadastro de Pontos)

```python
params_pontos = {
    "ponto": "Posto de Abastecimento XPTO",
    "cidade": "São Paulo",
    "cnpj": "12.345.678/0001-90",
    "tipo": "Abastecimento",
    "raio": "500",  # Raio de atuação em metros
}
```

---

### Exemplo de Dicionário para `params_rotograma` (Cadastro de Rotograma)

```python
params_rotograma = {
    "id": "R001",
    "retrograma": "Rotograma Principal",
    "distancia": "1200",  # Distância em km
    "criado_por": "Carlos Souza",
    "data_hora": "2024-06-01T12:00:00"  # Formato ISO 8601
}
```

---

### Exemplo de Dicionário para `params_logistica` (Cadastro de Logística)

```python
params_logistica = {
    "args_viagem": "Viagem SP-RJ",
    "args_veiculo": "ABC-1234",
    "args_gestor": "Gestor Central",
    "args_reboque": "XYZ-5678"
}
```

---

### Parâmetros Booleanos de Controle

Além dos parâmetros de cadastro, os seguintes parâmetros booleanos controlam se as informações devem ser cadastradas ou não:

```python
cadastrar_driver = True           # Cadastrar motorista
cadastrar_car = True              # Cadastrar veículo
cadastrar_reboque = True          # Cadastrar reboque
cadastrar_iscas = True            # Cadastrar iscas
cadastrar_pontos = True           # Cadastrar pontos
cliente_points = False            # Indica se os pontos são do cliente
cadastrar_rotograma = True        # Cadastrar rotograma
rotas_alternativas = False        # Considerar rotas alternativas
```

---

### Exemplo Completo da Chamada da Função

```python
process_cadastro(
    params_driver=params_driver,
    params_car=params_car,
    params_reboque=params_reboque,
    params_iscas=params_iscas,
    params_pontos=params_pontos,
    params_rotograma=params_rotograma,
    params_logistica=params_logistica,
    cadastrar_driver=True,
    cadastrar_car=True,
    cadastrar_reboque=False,
    cadastrar_iscas=True,
    cadastrar_pontos=False,
    cliente_points=False,
    cadastrar_rotograma=True,
    rotas_alternativas=True
)
```

---


Aqui estão os exemplos de dicionários e descrições para os parâmetros da função  **`extrator_to_grid`** , incluindo explicações e exemplos práticos para uso nas requsições da API:

---

### Exemplo de Parâmetros

1. **`map_` (bool)**

   Define se o mapa deve ser incluído no processo de extração.

   * `True`: Tira um **screenshot** do mapa.
   * `False`: Não inclui o mapa no processo.

   **Exemplo** :

   ```python
   map_ = True
   ```

---

2. **`list_results` (bool | dict)**

   Define como a extração dos resultados será realizada:

   * `True`: Captura a **lista completa** sem filtros.
   * `dict`: Aplica filtros personalizados antes de extrair os dados.

   **Exemplo com Filtros Personalizados** :

   ```python
   list_results = {
       "filtro_nome": "Caminhão ABC-1234",  # Filtra pelo nome/identificação
       "data_inicio": "2024-06-01",         # Data inicial do período
       "data_fim": "2024-06-30",            # Data final do período
       "status": "Ativo",                   # Filtra pelo status
       "tipo_veiculo": "Caminhão"           # Tipo específico de veículo
   }
   ```

---

### Exemplo de Chamada da Função

**Caso 1: Extração do Mapa e Lista Completa**

```python
extrator_to_grid(
    map_=True,              # Captura do mapa (tira screenshot)
    list_results=True       # Extrai lista completa (sem filtros)
)
```

**Caso 2: Extração Somente da Lista com Filtros Personalizados**

```python
extrator_to_grid(
    map_=False,             # Não captura o mapa
    list_results={
        "filtro_nome": "João da Silva",
        "data_inicio": "2024-06-01",
        "data_fim": "2024-06-30",
        "status": "Ativo",
        "tipo_veiculo": "Caminhão"
    }
)
```

**Caso 3: Apenas Mapa (Sem Lista)**

```python
extrator_to_grid(
    map_=True,              # Captura o mapa
    list_results=False      # Não extrai a lista
)
```

---

### Explicação Completa dos Parâmetros:

| Parâmetro       | Tipo              | Descrição                                                                               | Valor Padrão | Exemplos                                                                                                             |
| ---------------- | ----------------- | ----------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| `map_`         | `bool`          | Define se o mapa será incluído no processo.                                             | `True`      | `True`(tira screenshot do mapa),`False`(ignora o mapa).                                                          |
| `list_results` | `bool`/`dict` | Define se a lista completa será extraída ou se filtros personalizados serão aplicados. | `True`      | `True`(lista completa),`{"filtro_nome": "ABC", "data_inicio": "2024-06-01", "status": "Ativo"}`(lista filtrada). |

---

### Uso Completo e Prático

Aqui está um exemplo prático e completo do uso dessa função:

```python
# Extração completa do mapa e lista filtrada
extrator_to_grid(
    map_=True,
    list_results={
        "filtro_nome": "Frota XPTO",
        "data_inicio": "2024-05-01",
        "data_fim": "2024-06-30",
        "status": "Inativo",
        "tipo_veiculo": "Reboque"
    }
)
```

---
