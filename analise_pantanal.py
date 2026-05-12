"""
Análise Ambiental - Pantanal (jan/2025) 
Monitoramento de temperatura, nível do rio e índice NDVI.
Autor: Vinicius dos Reis Leal
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# 1. Leitura dos dados
df = pd.read_csv("dados_pantanal.csv", parse_dates=["data"])
df.set_index("data", inplace=True)

print("=== Dados brutos ===")
print(df)
print(f"\nValores ausentes por coluna:\n{df.isnull().sum()}")


# 2.Tratamento de valores ausentes
# Interpolação linear ponderada pelo tempo.
# Mais adequada que fillna(mean) para séries temporais,
# pois preserva a tendência entre os pontos adjacentes.
missing_mask = df.isnull()   # guarda posições antes de interpolar
df_clean = df.interpolate(method="time")

print("\n=== Dados após interpolação ===")
print(df_clean.round(3))

df_clean.round(3).to_csv("dados_pantanal_tratados.csv")
print("\nArquivo 'dados_pantanal_tratados.csv' salvo.")

# 3. Estatísticas Básicas
print("\n=== Estatísticas descritivas ===")
stats = df_clean.agg(["mean", "min", "max"]).round(3)
print(stats)


# 4. Visualização
COLUNAS = {
    "temperatura_c": {"label": "Temperatura (°C)", "unidade": "°C",     "cor": "#e05c2a"},
    "nivel_rio_m":   {"label": "Nível do Rio (m)",  "unidade": "metros", "cor": "#2a7ae0"},
    "ndvi":          {"label": "NDVI",              "unidade": "índice", "cor": "#2aae5c"},
}

fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
fig.suptitle(
    "Monitoramento Ambiental — Pantanal (Jan/2025)",
    fontsize=14, fontweight="bold", y=0.98
)

for ax, (col, cfg) in zip(axes, COLUNAS.items()):
    cor = cfg["cor"]

    # Linha principal (dados interpolados)
    ax.plot(df_clean.index, df_clean[col], color=cor, linewidth=2)

    # Pontos com dados originais
    originais = df[col].dropna()
    ax.scatter(originais.index, originais.values,
               color=cor, zorder=5, s=50, label="Dado original")

    # Pontos interpolados (eram ausentes)
    ausentes_idx = df[missing_mask[col]].index
    ax.scatter(ausentes_idx, df_clean.loc[ausentes_idx, col],
               color="gray", zorder=5, s=50, marker="x", label="Interpolado")

    # Linha de média
    media = df_clean[col].mean()
    ax.axhline(media, color=cor, linestyle="--", alpha=0.5, linewidth=1)
    ax.text(df_clean.index[-1], media,
            f"  média: {media:.2f}", va="center", fontsize=8, color=cor)

    ax.set_ylabel(cfg["unidade"])
    ax.set_title(cfg["label"], fontsize=11)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

plt.tight_layout()
plt.savefig("pantanal_graficos.png", dpi=150, bbox_inches="tight")
print("Gráfico 'pantanal_graficos.png' salvo.")
