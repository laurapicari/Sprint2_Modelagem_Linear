import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


df = pd.read_excel("baseDados01.xlsx")
df['electricity_price'] = pd.to_numeric(df['electricity_price'], errors='coerce')


contagem_veiculos = df['vehicle_type'].value_counts()
cores_pizza = ['#2196F3', '#4CAF50', '#FF9800']

fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    contagem_veiculos,
    labels=None,
    autopct='%1.1f%%',
    colors=cores_pizza,
    startangle=90,
    pctdistance=0.72,
    wedgeprops=dict(edgecolor='white', linewidth=1.8)
)
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight('bold')
    at.set_color('white')

ax.set_title('Distribuição por Tipo de Veículo nas Estações de Recarga',
             fontsize=13, fontweight='bold', pad=18)
ax.legend(wedges, contagem_veiculos.index,
          title='Tipo de Veículo', loc='lower center',
          bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=True)
plt.tight_layout()
plt.savefig('grafico_setores_vehicle_type.png', dpi=150, bbox_inches='tight')
plt.show()
print("Gráfico de Setores salvo.")


contagem_prioridade = df['charging_priority'].value_counts().reindex(['High', 'Medium', 'Low'])
cores_barras = ['#E53935', '#FB8C00', '#43A047']

fig, ax = plt.subplots(figsize=(7, 5))
barras = ax.bar(contagem_prioridade.index, contagem_prioridade.values,
                color=cores_barras, edgecolor='white', linewidth=1.2, width=0.5)

for barra in barras:
    altura = barra.get_height()
    ax.text(barra.get_x() + barra.get_width() / 2, altura + 30,
            f'{int(altura):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title('Quantidade de Recargas por Prioridade de Carregamento',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Prioridade de Carregamento', fontsize=11)
ax.set_ylabel('Número de Registros', fontsize=11)
ax.set_ylim(0, contagem_prioridade.max() * 1.15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
legendas = [mpatches.Patch(color=cores_barras[i], label=lbl)
            for i, lbl in enumerate(contagem_prioridade.index)]
ax.legend(handles=legendas, title='Prioridade', loc='upper right', frameon=True)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('grafico_barras_charging_priority.png', dpi=150, bbox_inches='tight')
plt.show()
print("Gráfico de Barras salvo.")


fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df['electricity_price'].dropna(), bins=12,
        color='#7B1FA2', edgecolor='white', linewidth=0.8)

ax.set_title('Distribuição do Preço da Energia Elétrica nas Sessões de Recarga',
             fontsize=12, fontweight='bold')
ax.set_xlabel('Preço da Energia Elétrica ($/MWh)', fontsize=11)
ax.set_ylabel('Frequência', fontsize=11)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('grafico_histograma_electricity_price.png', dpi=150, bbox_inches='tight')
plt.show()
print("Histograma salvo.")


fig, ax = plt.subplots(figsize=(7, 6))
ax.boxplot(df['waiting_time'].dropna(),
           patch_artist=True, notch=False, vert=True,
           widths=0.45,
           boxprops=dict(facecolor='#26A69A', color='#00695C', linewidth=1.5),
           medianprops=dict(color='white', linewidth=2.5),
           whiskerprops=dict(color='#00695C', linewidth=1.5),
           capprops=dict(color='#00695C', linewidth=1.5),
           flierprops=dict(marker='o', markerfacecolor='#80CBC4',
                           markeredgecolor='#00695C', markersize=4, alpha=0.5))

ax.set_title('Boxplot – Tempo de Espera nas Estações de Recarga',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Tempo de Espera', fontsize=11)
ax.set_ylabel('Unidades de Tempo', fontsize=11)
ax.set_xticks([1])
ax.set_xticklabels(['waiting_time'])
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('grafico_boxplot_waiting_time.png', dpi=150, bbox_inches='tight')
plt.show()
print("Boxplot salvo.")


variaveis = {
    'waiting_time': 'Tempo de Espera (waiting_time)',
    'electricity_price': 'Preço da Energia Elétrica (electricity_price)'
}

for col, descricao in variaveis.items():
    serie = df[col].dropna()

    # a) Medidas de Tendência Central
    media   = serie.mean()
    mediana = serie.median()
    moda    = serie.mode()[0]

    # b) Medidas de Dispersão
    desvio_padrao = serie.std()
    variancia     = serie.var()
    coef_var      = (desvio_padrao / media) * 100
    amplitude     = serie.max() - serie.min()

    # c) Medidas Separatrizes
    q1  = serie.quantile(0.25)
    q2  = serie.quantile(0.50)
    q3  = serie.quantile(0.75)
    iqr = q3 - q1
    p10 = serie.quantile(0.10)
    p90 = serie.quantile(0.90)

    print("=" * 58)
    print(f"  ANÁLISE UNIVARIADA – {descricao}")
    print("=" * 58)
    print(f"  Observações     : {len(serie):,}")
    print()
    print("  [a] MEDIDAS DE TENDÊNCIA CENTRAL")
    print(f"      Média         : {media:.4f}")
    print(f"      Mediana       : {mediana:.4f}")
    print(f"      Moda          : {moda:.4f}")
    print()
    print("  [b] MEDIDAS DE DISPERSÃO")
    print(f"      Desvio Padrão : {desvio_padrao:.4f}")
    print(f"      Variância     : {variancia:.4f}")
    print(f"      Coef. Variação: {coef_var:.2f}%")
    print(f"      Amplitude     : {amplitude:.4f}")
    print(f"      Mínimo        : {serie.min():.4f}")
    print(f"      Máximo        : {serie.max():.4f}")
    print()
    print("  [c] MEDIDAS SEPARATRIZES")
    print(f"      P10 (Decil 1) : {p10:.4f}")
    print(f"      Q1  (25%)     : {q1:.4f}")
    print(f"      Q2  (50%)     : {q2:.4f}")
    print(f"      Q3  (75%)     : {q3:.4f}")
    print(f"      P90 (Decil 9) : {p90:.4f}")
    print(f"      IIQ (Q3 - Q1) : {iqr:.4f}")
    print()

print("=" * 58)
print("  Análises Sprint 02 concluídas com sucesso.")
print("=" * 58)