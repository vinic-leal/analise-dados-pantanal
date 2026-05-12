# Análise Ambiental — Pantanal (Maio/2026)

Projeto de análise exploratória de dados ambientais do Pantanal, cobrindo temperatura do ar, nível do rio e índice de vegetação NDVI ao longo de 10 dias.

---

## Estrutura do projeto

```
pantanal_project/
├── analise_pantanal.py        # Script principal
├── dados_pantanal.csv         # Dados brutos originais
├── requirements.txt           # Dependências
└── README.md
```

Após a execução, são gerados:
- `dados_pantanal_tratados.csv` — dados com valores ausentes interpolados
- `pantanal_graficos.png` — visualização das três séries temporais

---

## Como executar

**Pré-requisito:** Python 3.9+

```bash
# 1. (Opcional) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 2. Instale as dependências com o comando:
pip install -r requirements.txt

# 3. Execute o script (python3 se estiver no linux):
python analise_pantanal.py
```

---

## Decisões técnicas

### Leitura dos dados
Os dados são lidos com `pandas.read_csv`, convertendo a coluna `data` para o tipo `datetime` via `parse_dates`. O índice temporal facilita operações subsequentes baseadas em tempo.

### Tratamento de valores ausentes
Optou-se por `DataFrame.interpolate(method="time")` no lugar de estratégias como `fillna(mean)` ou remoção de linhas. A razão é que as três variáveis analisadas (temperatura, nível do rio e NDVI) são séries temporais contínuas: o valor ausente em um dia está naturalmente relacionado aos dias adjacentes. A interpolação linear ponderada pelo tempo estima esses valores preservando a tendência local, o que é mais fiel à realidade do fenômeno do que substituí-los pela média global da série.

Os pontos interpolados são explicitamente marcados nos gráficos (símbolo "×" cinza) para garantir transparência na visualização.

### Visualização
Cada variável é exibida em um subgráfico independente com eixo X compartilhado (`sharex=True`), o que facilita a comparação visual entre as séries ao longo do mesmo período. Uma linha tracejada indica a média de cada variável. A distinção visual entre dados originais e interpolados permite avaliar a qualidade do preenchimento sem mascarar as lacunas existentes nos dados brutos.

### Dependências
Apenas `pandas` e `matplotlib` foram utilizados — bibliotecas consolidadas e suficientes para o escopo da análise, sem necessidade de dependências adicionais como `seaborn` ou `scipy`.
