# ===========================================================================
# 03_visualizacion_avanzada.py
# ===========================================================================
# MODULO 12: SQL Y VISUALIZACION
# ARCHIVO 03: Seaborn, Plotly Concepts, y Dashboards
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar visualizacion estadistica avanzada con Seaborn,
# conceptos de visualizacion interactiva, y patrones de dashboards.
#
# CONTENIDO:
#   1. Seaborn: API de alto nivel.
#   2. Distribuciones: kde, ecdf, rug.
#   3. Categorical plots.
#   4. Relational plots.
#   5. Regression plots.
#   6. Matrix plots (heatmaps, clustermaps).
#   7. FacetGrid y PairGrid.
#   8. Themes y paletas.
#   9. Plotly concepts (sin dependencia).
#   10. Dashboard patterns.
#   11. Visualizacion de datos temporales.
#   12. Best practices.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    print("  (seaborn no disponible, demos con matplotlib puro)")


# =====================================================================
#   PARTE 1: SEABORN FUNDAMENTOS
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: SEABORN FUNDAMENTOS ===")
print("=" * 80)

"""
Seaborn: API de alto nivel sobre Matplotlib.
- Integrado con Pandas DataFrames.
- Paletas de colores profesionales.
- Plots estadisticos automaticos.
- Temas elegantes por defecto.

3 niveles de API:
1. Figure-level: relplot, displot, catplot (crean su propia Figure).
2. Axes-level: scatterplot, histplot, boxplot (trabajan sobre un Axes).
3. sns.set_theme(): configurar estilos globales.
"""

print("\n--- Crear datos de ejemplo ---")

np.random.seed(42)
n = 500
df = pd.DataFrame({
    'age': np.random.randint(18, 65, n),
    'income': np.random.lognormal(10.5, 0.8, n).astype(int),
    'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n, p=[0.3, 0.35, 0.25, 0.1]),
    'department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'Design'], n),
    'satisfaction': np.clip(np.random.randn(n) * 1.5 + 7, 1, 10).round(1),
    'performance': np.clip(np.random.randn(n) * 15 + 70, 30, 100).round(1),
    'years_exp': np.random.randint(0, 30, n),
    'is_promoted': np.random.binomial(1, 0.2, n),
})
df['income'] = np.clip(df['income'], 20000, 300000)

print(f"  DataFrame: {df.shape}")
print(f"  Columns: {df.columns.tolist()}")


if HAS_SEABORN:
    print("\n--- Seaborn themes ---")
    
    themes = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
    print(f"  Available themes: {themes}")
    
    sns.set_theme(style='whitegrid', palette='deep', font_scale=1.1)
    print(f"  Theme set: whitegrid + deep palette")


# =====================================================================
#   PARTE 2: DISTRIBUTION PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DISTRIBUTION PLOTS ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- histplot ---")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    sns.histplot(data=df, x='income', bins=40, kde=True, ax=axes[0, 0], color='#1976D2')
    axes[0, 0].set_title('Income Distribution (hist + KDE)')
    
    sns.histplot(data=df, x='income', hue='department', multiple='stack', bins=30, ax=axes[0, 1])
    axes[0, 1].set_title('Income by Department (stacked)')
    
    sns.kdeplot(data=df, x='income', hue='education', fill=True, alpha=0.3, ax=axes[1, 0])
    axes[1, 0].set_title('Income KDE by Education')
    
    sns.ecdfplot(data=df, x='income', hue='department', ax=axes[1, 1])
    axes[1, 1].set_title('Income ECDF by Department')
    
    fig.tight_layout()
    plt.close(fig)
    print(f"  4 distribution plots: hist+KDE, stacked, KDE by group, ECDF")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df['income'], bins=40, color='#1976D2', alpha=0.7, edgecolor='white')
    ax.set_title('Income Distribution')
    plt.close(fig)
    print(f"  Basic histogram (seaborn not available)")


# =====================================================================
#   PARTE 3: CATEGORICAL PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: CATEGORICAL PLOTS ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- catplot family ---")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    sns.boxplot(data=df, x='department', y='income', ax=axes[0, 0], palette='Set2')
    axes[0, 0].set_title('Box Plot')
    
    sns.violinplot(data=df, x='department', y='income', ax=axes[0, 1], palette='Set2', inner='box')
    axes[0, 1].set_title('Violin Plot')
    
    sns.stripplot(data=df, x='department', y='income', ax=axes[0, 2], alpha=0.3, jitter=True)
    axes[0, 2].set_title('Strip Plot')
    
    sns.swarmplot(data=df.sample(100), x='department', y='satisfaction', ax=axes[1, 0], size=3)
    axes[1, 0].set_title('Swarm Plot (sample)')
    
    sns.barplot(data=df, x='department', y='income', estimator=np.mean, ax=axes[1, 1], palette='Set2')
    axes[1, 1].set_title('Bar Plot (mean + CI)')
    
    sns.countplot(data=df, x='department', hue='education', ax=axes[1, 2])
    axes[1, 2].set_title('Count Plot')
    
    fig.tight_layout()
    plt.close(fig)
    print(f"  6 categorical plots: box, violin, strip, swarm, bar, count")
else:
    print(f"  (categorical plots require seaborn)")


# =====================================================================
#   PARTE 4: RELATIONAL PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: RELATIONAL PLOTS ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- scatterplot ---")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.scatterplot(data=df, x='age', y='income', hue='department',
                    size='performance', sizes=(20, 200), alpha=0.6, ax=axes[0])
    axes[0].set_title('Age vs Income (color=dept, size=perf)')
    
    sns.scatterplot(data=df, x='years_exp', y='income', hue='education',
                    style='is_promoted', alpha=0.6, ax=axes[1])
    axes[1].set_title('Experience vs Income')
    
    fig.tight_layout()
    plt.close(fig)
    print(f"  Scatter: multi-dimensional (x, y, color, size, style)")
    
    
    print("\n--- lineplot ---")
    
    # Time series with CI
    df_ts = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=365, freq='D').tolist() * 3,
        'product': (['A'] * 365 + ['B'] * 365 + ['C'] * 365),
        'sales': np.concatenate([
            100 + np.random.randn(365).cumsum() * 2,
            80 + np.random.randn(365).cumsum() * 3,
            120 + np.random.randn(365).cumsum() * 1.5,
        ]),
    })
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df_ts, x='date', y='sales', hue='product', ax=ax)
    ax.set_title('Sales Trends with CI')
    fig.autofmt_xdate()
    plt.close(fig)
    print(f"  Line plot: 3 products with confidence intervals")
else:
    print(f"  (relational plots require seaborn)")


# =====================================================================
#   PARTE 5: REGRESSION PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: REGRESSION PLOTS ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- regplot / lmplot ---")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.regplot(data=df, x='age', y='income', scatter_kws={'alpha': 0.3}, ax=axes[0])
    axes[0].set_title('Linear Regression')
    
    sns.regplot(data=df, x='age', y='income', order=2, scatter_kws={'alpha': 0.3}, ax=axes[1])
    axes[1].set_title('Polynomial (order=2)')
    
    sns.regplot(data=df, x='years_exp', y='is_promoted', logistic=True,
                scatter_kws={'alpha': 0.1}, ax=axes[2], y_jitter=0.05)
    axes[2].set_title('Logistic Regression')
    
    fig.tight_layout()
    plt.close(fig)
    print(f"  Regression plots: linear, polynomial, logistic")
else:
    print(f"  (regression plots require seaborn)")


# =====================================================================
#   PARTE 6: MATRIX PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: MATRIX PLOTS ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- Correlation heatmap ---")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, ax=ax,
                cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Matrix (lower triangle)', fontsize=14)
    plt.close(fig)
    print(f"  Correlation heatmap: {len(numeric_cols)} features, lower triangle")
else:
    fig, ax = plt.subplots(figsize=(8, 6))
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    im = ax.imshow(corr, cmap='coolwarm', aspect='auto')
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45, ha='right')
    ax.set_yticklabels(numeric_cols)
    fig.colorbar(im)
    ax.set_title('Correlation Matrix')
    plt.close(fig)
    print(f"  Correlation heatmap (matplotlib)")


# =====================================================================
#   PARTE 7: FACETGRID Y PAIRGRID
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: FACETGRID ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- PairGrid / pairplot ---")
    
    sample = df[['age', 'income', 'satisfaction', 'performance', 'department']].sample(200)
    
    g = sns.pairplot(sample, hue='department', diag_kind='kde',
                     plot_kws={'alpha': 0.5, 's': 20})
    g.figure.suptitle('Pair Plot', y=1.02)
    plt.close(g.figure)
    print(f"  Pair plot: 4 numeric features by department")
    
    
    print("\n--- FacetGrid ---")
    
    g = sns.FacetGrid(df, col='department', row='education',
                      height=3, aspect=1.2, margin_titles=True)
    g.map_dataframe(sns.histplot, x='income', bins=20, kde=True)
    g.set_titles(col_template='{col_name}', row_template='{row_name}')
    plt.close(g.figure)
    print(f"  FacetGrid: income by dept (cols) x education (rows)")
else:
    print(f"  (FacetGrid requires seaborn)")


# =====================================================================
#   PARTE 8: PALETAS Y COLORES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: PALETAS ===")
print("=" * 80)

if HAS_SEABORN:
    print("\n--- Paletas de Seaborn ---")
    
    palettes = {
        'Categorical': ['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind'],
        'Sequential': ['Blues', 'Reds', 'Greens', 'rocket', 'mako', 'flare'],
        'Diverging': ['coolwarm', 'RdBu', 'vlag', 'icefire'],
    }
    
    for ptype, names in palettes.items():
        print(f"  {ptype}: {names}")
    
    # Custom palette
    custom = sns.color_palette(['#1976D2', '#D32F2F', '#388E3C', '#FFA000', '#7B1FA2'])
    print(f"\n  Custom palette: {len(custom)} colors")
else:
    print(f"  Palettes documented (seaborn not available)")


# =====================================================================
#   PARTE 9: PLOTLY CONCEPTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: PLOTLY CONCEPTS ===")
print("=" * 80)

"""
Plotly: visualizacion interactiva (zoom, hover, tooltips).
NO lo importamos para evitar dependencias, pero documentamos la API.

Plotly Express (px): API de alto nivel (como Seaborn).
Plotly Graph Objects (go): API de bajo nivel (como Matplotlib OO).

Ejemplo conceptual:
    import plotly.express as px
    fig = px.scatter(df, x='age', y='income', color='department',
                     size='performance', hover_data=['education'])
    fig.show()
    fig.write_html('plot.html')  # Interactivo!
"""

print("\n--- Plotly vs Matplotlib ---")

comparison = pd.DataFrame({
    'Feature': ['Interactivity', 'Static quality', 'Web export', 'Jupyter', 'Production', 'Learning'],
    'Matplotlib': ['Low', 'Excellent', 'PNG/PDF', 'Good', 'Mature', 'Moderate'],
    'Seaborn': ['Low', 'Excellent', 'PNG/PDF', 'Good', 'Mature', 'Easy'],
    'Plotly': ['Excellent', 'Good', 'HTML/Dash', 'Excellent', 'Growing', 'Easy'],
})
print(f"  Comparison:\n{comparison.to_string(index=False)}")

print("""
  REGLA DE SELECCION:
  - Paper/Report: Matplotlib + Seaborn
  - Exploration/Jupyter: Plotly Express
  - Dashboard: Plotly Dash o Streamlit
  - ML Results: Matplotlib (integrado con sklearn)
""")


# =====================================================================
#   PARTE 10: DASHBOARD PATTERNS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: DASHBOARD PATTERNS ===")
print("=" * 80)

"""
Dashboards en Python:
1. Streamlit: mas facil, rapido prototyping.
2. Plotly Dash: mas flexible, produccion.
3. Panel (HoloViz): integrado con cientifico.
4. Gradio: demos de ML.
"""

print("\n--- Multi-panel dashboard con Matplotlib ---")

fig = plt.figure(figsize=(16, 10))

# Layout: 2x3
ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 2)
ax3 = fig.add_subplot(2, 3, 3)
ax4 = fig.add_subplot(2, 3, (4, 5))
ax5 = fig.add_subplot(2, 3, 6)

# KPI cards (simulated)
metrics = {'Revenue': '$2.4M', 'Users': '15.2K', 'Conversion': '3.8%'}
for i, (name, value) in enumerate(metrics.items()):
    ax = [ax1, ax2, ax3][i]
    ax.text(0.5, 0.6, value, transform=ax.transAxes, fontsize=28,
            fontweight='bold', ha='center', va='center', color='#1976D2')
    ax.text(0.5, 0.3, name, transform=ax.transAxes, fontsize=14,
            ha='center', va='center', color='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.patch.set_facecolor('#f5f5f5')

# Revenue trend
months = range(1, 13)
revenue = [180, 195, 210, 225, 200, 215, 240, 260, 245, 230, 250, 280]
ax4.plot(months, revenue, 'o-', color='#1976D2', linewidth=2, markersize=6)
ax4.fill_between(months, revenue, alpha=0.1, color='#1976D2')
ax4.set_title('Monthly Revenue ($K)')
ax4.set_xlabel('Month')
ax4.grid(True, alpha=0.3)

# Department distribution
depts = df['department'].value_counts()
ax5.pie(depts.values, labels=depts.index, autopct='%1.0f%%',
        colors=['#1976D2', '#D32F2F', '#388E3C', '#FFA000'])
ax5.set_title('By Department')

fig.suptitle('Executive Dashboard', fontsize=18, fontweight='bold', y=1.02)
fig.tight_layout()
plt.close(fig)
print(f"  Dashboard: 3 KPIs + trend + distribution")


# =====================================================================
#   PARTE 11: TIME SERIES VISUALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: TIME SERIES VIZ ===")
print("=" * 80)

print("\n--- Candlestick-like chart ---")

np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=60, freq='D')
prices = 100 + np.random.randn(60).cumsum()

fig, ax = plt.subplots(figsize=(14, 6))

# OHLC simulation
for i in range(len(dates)):
    open_p = prices[i] + np.random.randn() * 0.5
    close_p = prices[i] + np.random.randn() * 0.5
    high_p = max(open_p, close_p) + abs(np.random.randn()) * 0.5
    low_p = min(open_p, close_p) - abs(np.random.randn()) * 0.5
    
    color = '#388E3C' if close_p >= open_p else '#D32F2F'
    ax.plot([i, i], [low_p, high_p], color=color, linewidth=0.8)
    ax.plot([i, i], [open_p, close_p], color=color, linewidth=3)

ax.set_title('Price Chart (OHLC-style)', fontsize=14)
ax.set_xlabel('Trading Day')
ax.set_ylabel('Price')
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  OHLC chart: 60 days")


print("\n--- Decomposition-style ---")

fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

t = np.arange(365)
trend = 100 + t * 0.1
seasonal = 10 * np.sin(2 * np.pi * t / 30)
noise = np.random.randn(365) * 3
observed = trend + seasonal + noise

axes[0].plot(t, observed, color='#1976D2', linewidth=0.8)
axes[0].set_title('Observed')
axes[1].plot(t, trend, color='#D32F2F', linewidth=1.5)
axes[1].set_title('Trend')
axes[2].plot(t, seasonal, color='#388E3C', linewidth=1)
axes[2].set_title('Seasonal')
axes[3].plot(t, noise, color='#757575', linewidth=0.5)
axes[3].set_title('Residual')

for ax in axes:
    ax.grid(True, alpha=0.3)

fig.suptitle('Time Series Decomposition', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.close(fig)
print(f"  Decomposition: observed + trend + seasonal + residual")


# =====================================================================
#   PARTE 12: BEST PRACTICES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: BEST PRACTICES ===")
print("=" * 80)

"""
REGLAS DE VISUALIZACION:

1. SIEMPRE title, labels, y legend.
2. NUNCA 3D cuando 2D es suficiente.
3. NUNCA pie chart con > 5 categorias.
4. Usar color con proposito (no decoracion).
5. Colores accesibles (colorblind-friendly: viridis, colorblind palette).
6. Aspect ratio importa (no distorsionar datos).
7. Minimal ink: eliminar todo lo que no comunique.
8. fig.tight_layout() o constrained_layout=True.
9. plt.close(fig) para liberar memoria.
10. DPI >= 300 para publicacion.

ANTI-PATTERNS:
- Grafico de barras 3D
- Doble eje Y con escalas muy diferentes
- Colores rainbow (no perceptualmente uniforme)
- Truncar eje Y para exagerar diferencias
- Demasiados elementos en un solo plot
"""

print("\n--- Checklist de calidad ---")

checklist = [
    ("Title descriptivo", True),
    ("Axis labels con unidades", True),
    ("Legend si hay multiples series", True),
    ("Grid sutil (alpha=0.3)", True),
    ("Colores colorblind-safe", True),
    ("tight_layout()", True),
    ("DPI >= 300 para export", True),
    ("plt.close() despues de savefig", True),
    ("Pie charts con <= 5 cats", True),
    ("No 3D innecesario", True),
]

for item, status in checklist:
    icon = "✓" if status else "✗"
    print(f"  {icon} {item}")


# =====================================================================
#   PARTE 13: EDA AUTOMATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: EDA AUTOMATION ===")
print("=" * 80)

"""
Automated EDA: generar plots para TODOS los features automaticamente.
"""

def auto_eda(df, max_plots=8):
    """Generar EDA automatico."""
    numeric = df.select_dtypes(include=[np.number]).columns[:max_plots]
    categorical = df.select_dtypes(include=['object', 'category']).columns[:4]
    
    n_num = len(numeric)
    n_cat = len(categorical)
    
    # Numeric distributions
    if n_num > 0:
        cols = min(4, n_num)
        rows = (n_num + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 3*rows))
        axes_flat = axes.flat if hasattr(axes, 'flat') else [axes]
        
        for i, col in enumerate(numeric):
            if i < len(list(axes_flat)):
                ax = list(axes_flat)[i]
                ax.hist(df[col].dropna(), bins=30, color='#1976D2', alpha=0.7, edgecolor='white')
                ax.set_title(col, fontsize=10)
                ax.axvline(df[col].mean(), color='red', linestyle='--', linewidth=1)
        
        fig.suptitle('Numeric Distributions', fontsize=14)
        fig.tight_layout()
        plt.close(fig)
    
    # Categorical counts
    if n_cat > 0:
        fig, axes = plt.subplots(1, min(4, n_cat), figsize=(4*min(4, n_cat), 4))
        if n_cat == 1:
            axes = [axes]
        
        for i, col in enumerate(categorical[:4]):
            counts = df[col].value_counts().head(10)
            axes[i].barh(counts.index, counts.values, color='#1976D2')
            axes[i].set_title(col, fontsize=10)
        
        fig.tight_layout()
        plt.close(fig)
    
    return n_num, n_cat

n_num, n_cat = auto_eda(df)
print(f"  Auto EDA: {n_num} numeric + {n_cat} categorical plots generated")


# =====================================================================
#   PARTE 14: GEOGRAPHIC VIZ CONCEPTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: GEOGRAPHIC VIZ ===")
print("=" * 80)

"""
Herramientas para mapas:
1. Folium: mapas interactivos con Leaflet.
2. Geopandas: DataFrames con geometria.
3. Plotly: choropleth maps.
4. Cartopy: mapas cientificos.

Ejemplo (conceptual):
    import folium
    m = folium.Map(location=[40.4, -3.7], zoom_start=6)
    folium.Marker([40.4, -3.7], popup='Madrid').add_to(m)
    m.save('map.html')
"""

print("\n--- Scatter map simulation ---")

fig, ax = plt.subplots(figsize=(10, 8))

np.random.seed(42)
n_cities = 20
lats = np.random.uniform(36, 44, n_cities)
lons = np.random.uniform(-10, 4, n_cities)
populations = np.random.randint(50, 500, n_cities)

scatter = ax.scatter(lons, lats, s=populations, c=populations, cmap='YlOrRd',
                     alpha=0.7, edgecolors='black', linewidth=0.5)
ax.set_title('City Populations (simulated)', fontsize=14)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
fig.colorbar(scatter, label='Population (K)')
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  Scatter map: {n_cities} cities")


# =====================================================================
#   PARTE 15: A/B TEST VISUALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: A/B TEST VIZ ===")
print("=" * 80)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Conversion rates
np.random.seed(42)
control = np.random.binomial(1, 0.05, 10000)
variant = np.random.binomial(1, 0.062, 10000)

# Daily rates
days = 30
ctrl_daily = [control[i*333:(i+1)*333].mean() for i in range(days)]
var_daily = [variant[i*333:(i+1)*333].mean() for i in range(days)]

axes[0].plot(range(days), ctrl_daily, 'o-', label='Control', color='#1976D2', markersize=4)
axes[0].plot(range(days), var_daily, 'o-', label='Variant', color='#D32F2F', markersize=4)
axes[0].set_title('Daily Conversion Rate')
axes[0].set_xlabel('Day')
axes[0].set_ylabel('Conversion Rate')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Distribution comparison
axes[1].hist(ctrl_daily, bins=15, alpha=0.6, color='#1976D2', label='Control')
axes[1].hist(var_daily, bins=15, alpha=0.6, color='#D32F2F', label='Variant')
axes[1].axvline(np.mean(ctrl_daily), color='#1976D2', linestyle='--')
axes[1].axvline(np.mean(var_daily), color='#D32F2F', linestyle='--')
axes[1].set_title('Rate Distribution')
axes[1].legend()

# Cumulative lift
cumulative_ctrl = np.cumsum(control) / np.arange(1, len(control)+1)
cumulative_var = np.cumsum(variant) / np.arange(1, len(variant)+1)
lift = (cumulative_var - cumulative_ctrl) / cumulative_ctrl * 100

axes[2].plot(lift[100:], color='#388E3C', linewidth=1)
axes[2].axhline(y=0, color='red', linestyle='--')
axes[2].set_title('Cumulative Lift (%)')
axes[2].set_xlabel('Sample Size')
axes[2].set_ylabel('Lift (%)')
axes[2].grid(True, alpha=0.3)

fig.suptitle('A/B Test Analysis', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.close(fig)
print(f"  A/B test: daily rates + distribution + cumulative lift")


# =====================================================================
#   PARTE 16: MODEL COMPARISON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: MODEL COMPARISON ===")
print("=" * 80)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

models = ['LogReg', 'RF', 'XGBoost', 'SVM', 'KNN']
accuracy = [0.82, 0.88, 0.91, 0.85, 0.79]
f1_scores = [0.80, 0.87, 0.90, 0.83, 0.77]
train_time = [0.5, 2.1, 3.5, 4.2, 0.3]

# Accuracy comparison
colors_m = ['#1976D2' if a == max(accuracy) else '#90CAF9' for a in accuracy]
axes[0].bar(models, accuracy, color=colors_m, edgecolor='white')
axes[0].set_title('Accuracy')
axes[0].set_ylim(0.7, 1.0)
for i, v in enumerate(accuracy):
    axes[0].text(i, v + 0.005, f'{v:.2f}', ha='center', fontsize=10)

# Accuracy vs F1
axes[1].scatter(accuracy, f1_scores, s=100, c='#1976D2', zorder=5)
for i, model in enumerate(models):
    axes[1].annotate(model, (accuracy[i], f1_scores[i]), textcoords="offset points",
                     xytext=(5, 5), fontsize=9)
axes[1].plot([0.7, 1], [0.7, 1], 'k--', alpha=0.3)
axes[1].set_title('Accuracy vs F1')
axes[1].set_xlabel('Accuracy')
axes[1].set_ylabel('F1 Score')
axes[1].grid(True, alpha=0.3)

# Speed vs Accuracy tradeoff
axes[2].scatter(train_time, accuracy, s=150, c='#D32F2F', zorder=5)
for i, model in enumerate(models):
    axes[2].annotate(model, (train_time[i], accuracy[i]), textcoords="offset points",
                     xytext=(5, 5), fontsize=9)
axes[2].set_title('Speed-Accuracy Tradeoff')
axes[2].set_xlabel('Training Time (s)')
axes[2].set_ylabel('Accuracy')
axes[2].grid(True, alpha=0.3)

fig.suptitle('Model Comparison Dashboard', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.close(fig)
print(f"  Model comparison: accuracy + F1 + speed tradeoff")


# =====================================================================
#   PARTE 17: DATA STORYTELLING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: DATA STORYTELLING ===")
print("=" * 80)

"""
Data storytelling: narrative + data + visuals.

Estructura de una data story:
1. Contexto (por que importa)
2. Insight clave (que descubrimos)
3. Evidencia visual (el plot)
4. Accion recomendada (que hacer)

Tecnicas:
- Highlight: resaltar el dato clave con color.
- Annotation: explicar el "por que" visualmente.
- Simplify: eliminar todo lo que no apoye la historia.
- Progressive: revelar informacion gradualmente.
"""

fig, ax = plt.subplots(figsize=(12, 6))

quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024']
revenue = [2.1, 2.3, 2.0, 2.5, 2.8, 3.4]

colors_story = ['#BBDEFB'] * 4 + ['#1976D2', '#1976D2']
ax.bar(quarters, revenue, color=colors_story, edgecolor='white', linewidth=2)

ax.annotate('New strategy\nlaunched here',
            xy=(4, 2.8), xytext=(2.5, 3.2),
            fontsize=11, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=2),
            color='#D32F2F')

ax.set_title('Revenue Growth Accelerated After New Strategy', fontsize=14, fontweight='bold')
ax.set_ylabel('Revenue ($M)')
ax.grid(True, alpha=0.2, axis='y')

for i, v in enumerate(revenue):
    ax.text(i, v + 0.05, f'${v}M', ha='center', fontsize=10, fontweight='bold')

plt.close(fig)
print(f"  Data storytelling: annotated bar chart with narrative")


# =====================================================================
#   PARTE 18: ACCESSIBILITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: ACCESSIBILITY ===")
print("=" * 80)

"""
Accesibilidad en visualizacion:

1. Color:
   - 8% de hombres son daltonicos.
   - Usar paletas colorblind-safe (viridis, colorblind).
   - NUNCA usar rojo+verde como unico diferenciador.
   - Complementar color con shape/pattern.

2. Contraste:
   - WCAG 2.0: ratio minimo 4.5:1.
   - Texto oscuro sobre fondo claro (o viceversa).

3. Alternativas:
   - Alt text para figuras en web.
   - Tablas de datos como complemento.

4. Tamaño:
   - Font size >= 10pt.
   - Line width >= 1.5 para plots impresos.
"""

print("  Accessibility checklist:")
access_items = [
    "Use colorblind-safe palettes",
    "Add patterns/markers as redundant encoding",
    "Ensure 4.5:1 contrast ratio",
    "Font size >= 10pt",
    "Provide alt text for web figures",
    "Include data tables as fallback",
    "Test with color blindness simulators",
]
for item in access_items:
    print(f"    ✓ {item}")


# =====================================================================
#   PARTE 19: ANIMATION CONCEPTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: ANIMATION ===")
print("=" * 80)

"""
Matplotlib animations:
    from matplotlib.animation import FuncAnimation
    
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    
    def update(frame):
        line.set_data(x[:frame], y[:frame])
        return line,
    
    ani = FuncAnimation(fig, update, frames=100, interval=50)
    ani.save('animation.gif', writer='pillow')

Alternativas:
- Plotly: animaciones interactivas con slider.
- Manim: animaciones matematicas (3Blue1Brown).
"""

print("  Animation patterns documented")
print("  Key: FuncAnimation + save to gif/mp4")


# =====================================================================
#   PARTE 20: STREAMLIT PATTERN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: STREAMLIT PATTERN ===")
print("=" * 80)

"""
Streamlit: dashboard rapido.

Ejemplo conceptual:
    import streamlit as st
    import pandas as pd
    
    st.title('ML Dashboard')
    
    # Sidebar
    model = st.sidebar.selectbox('Model', ['RF', 'XGBoost', 'LogReg'])
    threshold = st.sidebar.slider('Threshold', 0.0, 1.0, 0.5)
    
    # Main
    df = pd.read_csv('results.csv')
    st.dataframe(df)
    
    fig, ax = plt.subplots()
    ax.hist(df['predictions'])
    st.pyplot(fig)
    
    col1, col2, col3 = st.columns(3)
    col1.metric('Accuracy', '0.91', '+0.03')
    col2.metric('F1 Score', '0.89', '+0.02')
    col3.metric('Latency', '45ms', '-5ms')

Run: streamlit run app.py
"""

print("  Streamlit pattern: sidebar + metrics + plots")
print("  Deploy: streamlit run app.py")


# =====================================================================
#   PARTE 21: MULTI-PAGE REPORT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: MULTI-PAGE REPORT ===")
print("=" * 80)

"""
Generar PDF multi-pagina con matplotlib.backends.backend_pdf.
"""

print("\n--- Report generation pattern ---")

def generate_report(df, filename='report.pdf'):
    """Generar PDF con multiples paginas de plots."""
    from matplotlib.backends.backend_pdf import PdfPages
    
    # Solo documentar patron, no crear archivo
    print(f"  Pattern: PdfPages('{filename}')")
    print(f"  Page 1: Executive Summary (KPIs)")
    print(f"  Page 2: Distribution Analysis")
    print(f"  Page 3: Correlation Matrix")
    print(f"  Page 4: Time Series Trends")
    print(f"  Page 5: Model Performance")

generate_report(df)


# =====================================================================
#   PARTE 22: STATISTICAL PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: STATISTICAL PLOTS ===")
print("=" * 80)

print("\n--- QQ Plot ---")

fig, ax = plt.subplots(figsize=(7, 7))

np.random.seed(42)
data_qq = np.random.randn(200)
data_qq_sorted = np.sort(data_qq)
theoretical = np.sort(np.random.randn(200))

ax.scatter(theoretical, data_qq_sorted, alpha=0.6, s=20, color='#1976D2')
lims = [min(theoretical.min(), data_qq_sorted.min()), max(theoretical.max(), data_qq_sorted.max())]
ax.plot(lims, lims, 'r--', linewidth=1.5)
ax.set_title('Q-Q Plot (Normal)')
ax.set_xlabel('Theoretical Quantiles')
ax.set_ylabel('Sample Quantiles')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  QQ plot: normality check")


print("\n--- Bootstrap CI visualization ---")

fig, ax = plt.subplots(figsize=(10, 5))

np.random.seed(42)
sample = np.random.randn(100) + 5
boot_means = [np.random.choice(sample, len(sample)).mean() for _ in range(1000)]

ax.hist(boot_means, bins=30, color='#1976D2', alpha=0.7, edgecolor='white')
ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
ax.axvline(ci_low, color='#D32F2F', linestyle='--', label=f'95% CI: [{ci_low:.3f}, {ci_high:.3f}]')
ax.axvline(ci_high, color='#D32F2F', linestyle='--')
ax.axvline(np.mean(sample), color='#388E3C', linestyle='-', linewidth=2, label=f'Sample Mean: {np.mean(sample):.3f}')
ax.set_title('Bootstrap Confidence Interval')
ax.legend()
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  Bootstrap CI: {ci_low:.3f} to {ci_high:.3f}")


# =====================================================================
#   PARTE 23: FUNNEL CHART
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: FUNNEL CHART ===")
print("=" * 80)

fig, ax = plt.subplots(figsize=(10, 6))

stages = ['Visitors', 'Sign-ups', 'Trials', 'Purchases', 'Retained']
values_f = [10000, 5000, 2000, 800, 500]
pcts = [v/values_f[0]*100 for v in values_f]

for i, (stage, val, pct) in enumerate(zip(stages, values_f, pcts)):
    width = pct / 100
    left = (1 - width) / 2
    ax.barh(len(stages) - i - 1, width, left=left, height=0.6,
            color=plt.cm.Blues(0.3 + pct/200), edgecolor='white', linewidth=2)
    ax.text(0.5, len(stages) - i - 1, f'{stage}\n{val:,} ({pct:.0f}%)',
            ha='center', va='center', fontsize=11, fontweight='bold')

ax.set_xlim(0, 1)
ax.axis('off')
ax.set_title('Conversion Funnel', fontsize=14, fontweight='bold')
plt.close(fig)
print(f"  Funnel chart: 5 stages")


# =====================================================================
#   PARTE 24: NETWORK GRAPH VISUALIZATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: NETWORK GRAPH ===")
print("=" * 80)

"""
Visualizacion de grafos/redes:
- networkx: la libreria standard.
- pyvis: grafos interactivos.
"""

fig, ax = plt.subplots(figsize=(8, 8))

np.random.seed(42)
n_nodes = 15
positions = np.random.rand(n_nodes, 2)

# Random edges
for i in range(n_nodes):
    for j in range(i+1, n_nodes):
        if np.random.random() < 0.2:
            ax.plot([positions[i, 0], positions[j, 0]],
                    [positions[i, 1], positions[j, 1]],
                    'gray', alpha=0.3, linewidth=0.8)

sizes = np.random.randint(100, 500, n_nodes)
ax.scatter(positions[:, 0], positions[:, 1], s=sizes, c=range(n_nodes),
           cmap='tab10', zorder=5, edgecolors='white', linewidth=1.5)

for i in range(n_nodes):
    ax.text(positions[i, 0], positions[i, 1], str(i),
            ha='center', va='center', fontsize=8, fontweight='bold')

ax.set_title('Network Graph', fontsize=14)
ax.axis('off')
plt.close(fig)
print(f"  Network graph: {n_nodes} nodes")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE VISUALIZACION AVANZADA:

1. Seaborn = Matplotlib + Pandas + estadistica.
2. Figure-level (relplot, displot) vs Axes-level (scatterplot, histplot).
3. hue, size, style para multiples dimensiones.
4. FacetGrid para small multiples.
5. Correlation heatmap con mask triangular.
6. Plotly para interactividad, Matplotlib para publicacion.
7. Dashboards: KPI cards + trends + distributions.
8. Time series: decomposition, candlestick.
9. SIEMPRE: title, labels, legend, tight_layout.
10. NUNCA: 3D innecesario, rainbow colors, truncated axes.

FIN DEL MODULO 12: SQL Y VISUALIZACION.
"""

print("\n FIN DE ARCHIVO 03_visualizacion_avanzada.")
print(" Visualizacion avanzada ha sido dominada.")
print(" Siguiente modulo: ML FUNDAMENTOS.")
