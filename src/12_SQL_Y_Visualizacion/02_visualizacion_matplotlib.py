# ===========================================================================
# 02_visualizacion_matplotlib.py
# ===========================================================================
# MODULO 12: SQL Y VISUALIZACION
# ARCHIVO 02: Matplotlib Deep Dive
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar Matplotlib para visualizacion profesional.
# Desde basico hasta publicacion-ready.
#
# CONTENIDO:
#   1. Arquitectura: Figure, Axes, Artist.
#   2. Line plots, scatter, bar, histogram.
#   3. Subplots y layouts.
#   4. Estilos y temas.
#   5. Anotaciones y texto.
#   6. Colormaps.
#   7. 3D plots.
#   8. Animaciones (concepto).
#   9. Guardar figuras (png, pdf, svg).
#   10. Visualizacion para ML.
#
# NOTA: Este archivo usa el backend 'Agg' (no-GUI) para generar
# figuras programaticamente sin necesidad de display.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd


# =====================================================================
#   PARTE 1: ARQUITECTURA MATPLOTLIB
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: ARQUITECTURA ===")
print("=" * 80)

"""
Jerarquia de objetos:
1. Figure: contenedor top-level (la "pagina").
2. Axes: un plot individual (NO es plural de axis).
3. Axis: el eje X o Y.
4. Artist: todo lo que se dibuja (lines, text, patches).

Dos interfaces:
- pyplot (stateful): plt.plot(), plt.show() -> rapido para explorar.
- OO (object-oriented): fig, ax = plt.subplots() -> produccion.

REGLA: SIEMPRE usar OO para codigo de produccion.
"""

print("\n--- Figure y Axes ---")

fig, ax = plt.subplots(figsize=(8, 5))
print(f"  Figure: {type(fig).__name__}")
print(f"  Axes: {type(ax).__name__}")
print(f"  Figure size: {fig.get_size_inches()}")
print(f"  DPI: {fig.get_dpi()}")
plt.close(fig)


print("\n--- Anatomia de un plot ---")

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 2 * np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)', color='#2196F3', linewidth=2)
ax.plot(x, np.cos(x), label='cos(x)', color='#FF5722', linewidth=2, linestyle='--')

ax.set_title('Trigonometric Functions', fontsize=16, fontweight='bold')
ax.set_xlabel('x (radians)', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linewidth=0.5)

fig.tight_layout()
plt.close(fig)
print(f"  Plot anatomy: title, xlabel, ylabel, legend, grid, axhline")


# =====================================================================
#   PARTE 2: TIPOS DE PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: TIPOS DE PLOTS ===")
print("=" * 80)

print("\n--- Line plot ---")

fig, ax = plt.subplots(figsize=(10, 5))

np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=90, freq='D')
stock_a = 100 + np.random.randn(90).cumsum()
stock_b = 100 + np.random.randn(90).cumsum() * 1.5

ax.plot(dates, stock_a, label='Stock A', color='#1976D2', linewidth=1.5)
ax.plot(dates, stock_b, label='Stock B', color='#D32F2F', linewidth=1.5)
ax.fill_between(dates, stock_a, stock_b, alpha=0.1, color='gray')
ax.set_title('Stock Prices', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
fig.autofmt_xdate()
plt.close(fig)
print(f"  Line plot: 2 series, fill_between, date axis")


print("\n--- Scatter plot ---")

fig, ax = plt.subplots(figsize=(8, 6))

n = 200
x = np.random.randn(n)
y = 0.5 * x + np.random.randn(n) * 0.5
colors = np.random.randn(n)
sizes = np.abs(np.random.randn(n)) * 100

scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis', edgecolors='white', linewidth=0.5)
ax.set_title('Scatter Plot with Color & Size', fontsize=14)
ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
fig.colorbar(scatter, ax=ax, label='Color Value')
plt.close(fig)
print(f"  Scatter: {n} points, color-mapped, size-mapped")


print("\n--- Bar plot ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

categories = ['Engineering', 'Marketing', 'Sales', 'Design']
values = [45, 30, 38, 22]
colors_bar = ['#1976D2', '#D32F2F', '#388E3C', '#FFA000']

# Vertical
axes[0].bar(categories, values, color=colors_bar, edgecolor='white', linewidth=1.5)
axes[0].set_title('Vertical Bar', fontsize=13)
axes[0].set_ylabel('Headcount')
for i, v in enumerate(values):
    axes[0].text(i, v + 1, str(v), ha='center', fontweight='bold')

# Horizontal
axes[1].barh(categories, values, color=colors_bar, edgecolor='white', linewidth=1.5)
axes[1].set_title('Horizontal Bar', fontsize=13)
axes[1].set_xlabel('Headcount')

fig.tight_layout()
plt.close(fig)
print(f"  Bar plots: vertical + horizontal, with labels")


print("\n--- Histogram ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

data = np.random.randn(10000)

axes[0].hist(data, bins=50, color='#1976D2', alpha=0.7, edgecolor='white')
axes[0].set_title('Histogram (50 bins)')
axes[0].axvline(data.mean(), color='red', linestyle='--', label=f'Mean={data.mean():.2f}')
axes[0].legend()

# KDE-like
axes[1].hist(data, bins=50, density=True, alpha=0.7, color='#1976D2', edgecolor='white')
x_kde = np.linspace(-4, 4, 100)
axes[1].plot(x_kde, (1/np.sqrt(2*np.pi)) * np.exp(-x_kde**2/2), 'r-', linewidth=2, label='Normal PDF')
axes[1].set_title('Histogram + PDF')
axes[1].legend()

fig.tight_layout()
plt.close(fig)
print(f"  Histogram: 10k samples, with mean line and PDF overlay")


print("\n--- Pie chart ---")

fig, ax = plt.subplots(figsize=(8, 6))

sizes = [35, 25, 20, 15, 5]
labels = ['Python', 'JavaScript', 'Java', 'C++', 'Other']
explode = (0.05, 0, 0, 0, 0)
colors_pie = ['#1976D2', '#FFA000', '#D32F2F', '#388E3C', '#757575']

ax.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
       shadow=False, startangle=90, textprops={'fontsize': 11})
ax.set_title('Programming Languages', fontsize=14)
plt.close(fig)
print(f"  Pie chart: 5 categories")


# =====================================================================
#   PARTE 3: SUBPLOTS Y LAYOUTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: SUBPLOTS ===")
print("=" * 80)

print("\n--- Grid regular ---")

fig, axes = plt.subplots(2, 3, figsize=(15, 8))

for i, ax in enumerate(axes.flat):
    ax.set_title(f'Plot {i+1}')
    ax.plot(np.random.randn(50).cumsum())

fig.suptitle('2x3 Grid', fontsize=16, fontweight='bold')
fig.tight_layout()
plt.close(fig)
print(f"  2x3 grid: 6 subplots")


print("\n--- GridSpec (layout irregular) ---")

fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(2, 3, figure=fig)

ax1 = fig.add_subplot(gs[0, :2])  # Top-left, 2 columns
ax2 = fig.add_subplot(gs[0, 2])   # Top-right
ax3 = fig.add_subplot(gs[1, 0])   # Bottom-left
ax4 = fig.add_subplot(gs[1, 1:])  # Bottom-right, 2 columns

ax1.set_title('Wide top')
ax2.set_title('Narrow top')
ax3.set_title('Narrow bottom')
ax4.set_title('Wide bottom')

for ax in [ax1, ax2, ax3, ax4]:
    ax.plot(np.random.randn(30).cumsum())

fig.tight_layout()
plt.close(fig)
print(f"  GridSpec: irregular layout (2+1 top, 1+2 bottom)")


# =====================================================================
#   PARTE 4: ESTILOS Y TEMAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: ESTILOS ===")
print("=" * 80)

print("\n--- Estilos disponibles ---")

styles = plt.style.available
print(f"  Available styles ({len(styles)}): {styles[:8]}...")


print("\n--- Custom style ---")

custom_style = {
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#e94560',
    'axes.labelcolor': 'white',
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'grid.color': '#333333',
    'font.size': 12,
}

with plt.rc_context(custom_style):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.random.randn(100).cumsum(), color='#e94560', linewidth=2)
    ax.set_title('Dark Theme Custom')
    ax.grid(True, alpha=0.3)
    plt.close(fig)
print(f"  Custom dark theme applied")


# =====================================================================
#   PARTE 5: ANOTACIONES Y TEXTO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: ANOTACIONES ===")
print("=" * 80)

print("\n--- Annotate ---")

fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/5)
ax.plot(x, y, 'b-', linewidth=2)

# Encontrar maximo
max_idx = np.argmax(y)
ax.annotate(f'Max: {y[max_idx]:.2f}',
            xy=(x[max_idx], y[max_idx]),
            xytext=(x[max_idx] + 2, y[max_idx] + 0.2),
            fontsize=12,
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))

ax.set_title('Damped Sine Wave with Annotation')
plt.close(fig)
print(f"  Annotation: arrow, bbox, custom text")


# =====================================================================
#   PARTE 6: COLORMAPS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: COLORMAPS ===")
print("=" * 80)

"""
Colormaps:
- Sequential: viridis, plasma, inferno, magma (para datos ordenados).
- Diverging: coolwarm, RdBu, seismic (para datos con centro).
- Qualitative: tab10, Set1 (para categorias).
"""

print("\n--- Heatmap ---")

fig, ax = plt.subplots(figsize=(8, 6))

data = np.random.randn(10, 10)
im = ax.imshow(data, cmap='coolwarm', aspect='auto', interpolation='nearest')
ax.set_title('Heatmap (coolwarm)')
fig.colorbar(im, ax=ax)

# Agregar valores en celdas
for i in range(10):
    for j in range(10):
        ax.text(j, i, f'{data[i, j]:.1f}', ha='center', va='center', fontsize=7)

plt.close(fig)
print(f"  Heatmap: 10x10, coolwarm, with cell values")


print("\n--- Colormaps disponibles ---")

cmaps = {
    'Sequential': ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
    'Diverging': ['coolwarm', 'RdBu', 'seismic', 'PiYG'],
    'Qualitative': ['tab10', 'Set1', 'Set2', 'Paired'],
}

for category, names in cmaps.items():
    print(f"  {category}: {names}")


# =====================================================================
#   PARTE 7: VISUALIZACION PARA ML
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: PLOTS PARA ML ===")
print("=" * 80)

print("\n--- Confusion Matrix ---")

fig, ax = plt.subplots(figsize=(6, 5))

cm = np.array([[85, 15], [10, 90]])
im = ax.imshow(cm, cmap='Blues')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Predicted 0', 'Predicted 1'])
ax.set_yticklabels(['Actual 0', 'Actual 1'])
ax.set_title('Confusion Matrix')

for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i, j]), ha='center', va='center', fontsize=20,
                color='white' if cm[i, j] > 50 else 'black')

fig.colorbar(im, ax=ax)
plt.close(fig)
print(f"  Confusion matrix: 2x2")


print("\n--- Learning Curves ---")

fig, ax = plt.subplots(figsize=(10, 5))

epochs = np.arange(1, 51)
train_loss = 2.0 * np.exp(-epochs/10) + 0.2 + np.random.randn(50) * 0.05
val_loss = 2.0 * np.exp(-epochs/12) + 0.3 + np.random.randn(50) * 0.08

ax.plot(epochs, train_loss, label='Train Loss', color='#1976D2', linewidth=2)
ax.plot(epochs, val_loss, label='Val Loss', color='#D32F2F', linewidth=2)
ax.fill_between(epochs, train_loss, val_loss, alpha=0.1, color='gray')
ax.axhline(y=0.3, color='green', linestyle=':', label='Target')
ax.set_title('Learning Curves', fontsize=14)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.legend()
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  Learning curves: train + val loss")


print("\n--- Feature Importance ---")

fig, ax = plt.subplots(figsize=(8, 5))

features = ['age', 'income', 'education', 'tenure', 'region', 'score', 'visits']
importance = np.array([0.25, 0.20, 0.18, 0.15, 0.10, 0.08, 0.04])
sorted_idx = np.argsort(importance)

ax.barh(np.array(features)[sorted_idx], importance[sorted_idx], color='#1976D2', edgecolor='white')
ax.set_title('Feature Importance', fontsize=14)
ax.set_xlabel('Importance')
plt.close(fig)
print(f"  Feature importance: horizontal bar chart")


print("\n--- ROC Curve ---")

fig, ax = plt.subplots(figsize=(7, 7))

# Simular ROC
fpr = np.array([0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0])
tpr = np.array([0, 0.3, 0.5, 0.7, 0.8, 0.85, 0.92, 0.97, 1.0])
auc = np.trapz(tpr, fpr)

ax.plot(fpr, tpr, 'b-', linewidth=2, label=f'Model (AUC={auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random (AUC=0.5)')
ax.fill_between(fpr, tpr, alpha=0.1, color='blue')
ax.set_title('ROC Curve', fontsize=14)
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.legend(loc='lower right')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  ROC curve: AUC={auc:.3f}")


print("\n--- Distribution comparison ---")

fig, ax = plt.subplots(figsize=(10, 5))

class_0 = np.random.randn(500) * 0.8 + 1
class_1 = np.random.randn(500) * 1.0 + 3

ax.hist(class_0, bins=30, alpha=0.6, color='#1976D2', label='Class 0', density=True)
ax.hist(class_1, bins=30, alpha=0.6, color='#D32F2F', label='Class 1', density=True)
ax.axvline(x=2.0, color='green', linestyle='--', label='Threshold')
ax.set_title('Class Distribution', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  Distribution comparison: 2 classes with threshold")


# =====================================================================
#   PARTE 8: GUARDAR FIGURAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: GUARDAR FIGURAS ===")
print("=" * 80)

"""
Formatos:
- PNG: raster, web, documentos.
- PDF: vector, papers, reportes.
- SVG: vector, web interactivo.
- EPS: vector, publicaciones cientificas.
"""

print("\n--- savefig ---")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title('Test Save')

# Parametros importantes de savefig:
# dpi: resolucion (300 para publicacion)
# bbox_inches='tight': eliminar whitespace
# transparent: fondo transparente
# facecolor: color de fondo

print(f"  savefig params: dpi, bbox_inches, transparent, facecolor")
print(f"  Recommended: fig.savefig('plot.png', dpi=300, bbox_inches='tight')")
plt.close(fig)


# =====================================================================
#   PARTE 9: TWIN AXES Y SECONDARY Y
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: TWIN AXES ===")
print("=" * 80)

fig, ax1 = plt.subplots(figsize=(10, 5))

months = np.arange(1, 13)
revenue = [100, 120, 150, 180, 200, 220, 250, 240, 230, 210, 190, 300]
users = [1000, 1200, 1500, 2000, 2500, 3000, 3200, 3100, 2800, 2500, 2200, 4000]

ax1.bar(months, revenue, color='#1976D2', alpha=0.7, label='Revenue ($k)')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue ($k)', color='#1976D2')

ax2 = ax1.twinx()
ax2.plot(months, users, color='#D32F2F', linewidth=2, marker='o', label='Users')
ax2.set_ylabel('Users', color='#D32F2F')

fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.95))
ax1.set_title('Revenue & Users', fontsize=14)
plt.close(fig)
print(f"  Twin axes: bar (left) + line (right)")


# =====================================================================
#   PARTE 10: BOX PLOTS Y VIOLIN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: BOX Y VIOLIN ===")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

data_box = [np.random.randn(100) * s + m for s, m in [(1, 0), (1.5, 2), (0.8, 1), (2, -1)]]
labels_box = ['Group A', 'Group B', 'Group C', 'Group D']

bp = axes[0].boxplot(data_box, labels=labels_box, patch_artist=True)
colors_box = ['#1976D2', '#D32F2F', '#388E3C', '#FFA000']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0].set_title('Box Plot', fontsize=13)
axes[0].grid(True, alpha=0.3, axis='y')

vp = axes[1].violinplot(data_box, positions=range(1, 5), showmeans=True, showmedians=True)
axes[1].set_xticks(range(1, 5))
axes[1].set_xticklabels(labels_box)
axes[1].set_title('Violin Plot', fontsize=13)
axes[1].grid(True, alpha=0.3, axis='y')

fig.tight_layout()
plt.close(fig)
print(f"  Box plot + Violin plot: 4 groups")


# =====================================================================
#   PARTE 11: ERROR BARS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: ERROR BARS ===")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

x = np.arange(5)
means = [3.2, 4.1, 3.8, 4.5, 3.9]
errors = [0.3, 0.5, 0.2, 0.4, 0.3]

axes[0].errorbar(x, means, yerr=errors, fmt='o-', capsize=5, color='#1976D2',
                 ecolor='#D32F2F', elinewidth=1.5, capthick=1.5)
axes[0].set_title('Symmetric Error Bars')
axes[0].set_xticks(x)
axes[0].set_xticklabels(['A', 'B', 'C', 'D', 'E'])

# Asymmetric errors
lower_err = [0.2, 0.3, 0.1, 0.2, 0.15]
upper_err = [0.5, 0.4, 0.3, 0.6, 0.4]
axes[1].errorbar(x, means, yerr=[lower_err, upper_err], fmt='s--', capsize=5,
                 color='#388E3C', ecolor='gray')
axes[1].set_title('Asymmetric Error Bars')
axes[1].set_xticks(x)
axes[1].set_xticklabels(['A', 'B', 'C', 'D', 'E'])

fig.tight_layout()
plt.close(fig)
print(f"  Error bars: symmetric + asymmetric")


# =====================================================================
#   PARTE 12: STACKED AREA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: STACKED AREA ===")
print("=" * 80)

fig, ax = plt.subplots(figsize=(12, 6))

days = np.arange(1, 31)
mobile = np.random.randint(200, 400, 30)
desktop = np.random.randint(300, 500, 30)
tablet = np.random.randint(50, 150, 30)

ax.stackplot(days, mobile, desktop, tablet,
             labels=['Mobile', 'Desktop', 'Tablet'],
             colors=['#1976D2', '#D32F2F', '#FFA000'], alpha=0.8)
ax.legend(loc='upper left')
ax.set_title('Traffic by Device', fontsize=14)
ax.set_xlabel('Day')
ax.set_ylabel('Visits')
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  Stacked area chart: 3 categories, 30 days")


# =====================================================================
#   PARTE 13: POLAR PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: POLAR PLOTS ===")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={'projection': 'polar'})

# Radar chart
categories_radar = ['Speed', 'Power', 'Accuracy', 'Endurance', 'Agility', 'Intelligence']
n_cats = len(categories_radar)
angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
angles += angles[:1]

values1 = [85, 70, 90, 60, 75, 95]
values2 = [70, 85, 75, 80, 90, 65]
values1 += values1[:1]
values2 += values2[:1]

axes[0].plot(angles, values1, 'o-', linewidth=2, label='Model A', color='#1976D2')
axes[0].fill(angles, values1, alpha=0.15, color='#1976D2')
axes[0].plot(angles, values2, 'o-', linewidth=2, label='Model B', color='#D32F2F')
axes[0].fill(angles, values2, alpha=0.15, color='#D32F2F')
axes[0].set_xticks(angles[:-1])
axes[0].set_xticklabels(categories_radar)
axes[0].set_title('Radar Chart', pad=20)
axes[0].legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# Polar scatter
theta = np.random.uniform(0, 2*np.pi, 100)
r = np.random.uniform(0, 1, 100)
axes[1].scatter(theta, r, c=r, cmap='viridis', alpha=0.7, s=30)
axes[1].set_title('Polar Scatter', pad=20)

plt.close(fig)
print(f"  Radar chart + polar scatter")


# =====================================================================
#   PARTE 14: STEP Y STEM PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: STEP Y STEM ===")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Step plot (digital signals, discrete events)
x = np.arange(0, 10, 0.5)
y = np.random.choice([0, 1], len(x))
axes[0].step(x, y, where='post', color='#1976D2', linewidth=2)
axes[0].fill_between(x, y, step='post', alpha=0.2, color='#1976D2')
axes[0].set_title('Step Plot (digital signal)')
axes[0].set_ylim(-0.1, 1.1)

# Stem plot (discrete data)
x_stem = np.arange(20)
y_stem = np.random.randn(20)
markerline, stemlines, baseline = axes[1].stem(x_stem, y_stem)
markerline.set_color('#1976D2')
markerline.set_markersize(5)
plt.setp(stemlines, color='#1976D2', linewidth=1)
plt.setp(baseline, color='gray', linewidth=0.5)
axes[1].set_title('Stem Plot (discrete data)')

fig.tight_layout()
plt.close(fig)
print(f"  Step + stem plots")


# =====================================================================
#   PARTE 15: CONTOUR PLOTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: CONTOUR ===")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

x_c = np.linspace(-3, 3, 100)
y_c = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x_c, y_c)
Z = np.sin(X) * np.cos(Y) * np.exp(-0.1 * (X**2 + Y**2))

# Contour lines
cs = axes[0].contour(X, Y, Z, levels=15, cmap='coolwarm')
axes[0].clabel(cs, inline=True, fontsize=7)
axes[0].set_title('Contour Lines')
axes[0].set_aspect('equal')

# Filled contour
cf = axes[1].contourf(X, Y, Z, levels=15, cmap='viridis')
fig.colorbar(cf, ax=axes[1])
axes[1].set_title('Filled Contour')
axes[1].set_aspect('equal')

fig.tight_layout()
plt.close(fig)
print(f"  Contour: lines + filled")


# =====================================================================
#   PARTE 16: QUIVER (VECTOR FIELDS)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: QUIVER ===")
print("=" * 80)

fig, ax = plt.subplots(figsize=(8, 8))

x_q = np.arange(-2, 2, 0.3)
y_q = np.arange(-2, 2, 0.3)
X_q, Y_q = np.meshgrid(x_q, y_q)
U = -Y_q
V = X_q

ax.quiver(X_q, Y_q, U, V, np.sqrt(U**2 + V**2), cmap='coolwarm')
ax.set_title('Vector Field (quiver)')
ax.set_aspect('equal')
plt.close(fig)
print(f"  Quiver plot: vector field")


# =====================================================================
#   PARTE 17: WATERFALL CHART
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: WATERFALL ===")
print("=" * 80)

fig, ax = plt.subplots(figsize=(12, 6))

categories_w = ['Revenue', 'COGS', 'Gross Profit', 'OpEx', 'Tax', 'Net Income']
values_w = [500, -200, 300, -120, -50, 130]
cumulative = np.cumsum(values_w)
bottoms = np.concatenate(([0], cumulative[:-1]))

colors_w = ['#388E3C' if v > 0 else '#D32F2F' for v in values_w]
colors_w[-1] = '#1976D2'  # Net income

ax.bar(categories_w, values_w, bottom=bottoms, color=colors_w,
       edgecolor='white', linewidth=1.5)

for i, (v, b) in enumerate(zip(values_w, bottoms)):
    ax.text(i, b + v + 5, f'{v:+d}', ha='center', fontweight='bold')

ax.set_title('Waterfall Chart (P&L)', fontsize=14)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.grid(True, alpha=0.3, axis='y')
plt.close(fig)
print(f"  Waterfall chart: profit & loss")


# =====================================================================
#   PARTE 18: GANTT CHART
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: GANTT CHART ===")
print("=" * 80)

fig, ax = plt.subplots(figsize=(12, 5))

tasks = ['Research', 'Design', 'Develop', 'Testing', 'Deploy']
starts = [0, 2, 4, 8, 10]
durations = [3, 3, 5, 3, 2]
colors_g = ['#1976D2', '#D32F2F', '#388E3C', '#FFA000', '#7B1FA2']

for i, (task, start, dur, color) in enumerate(zip(tasks, starts, durations, colors_g)):
    ax.barh(i, dur, left=start, height=0.5, color=color, edgecolor='white', linewidth=1.5)
    ax.text(start + dur/2, i, f'{dur}w', ha='center', va='center', color='white', fontweight='bold')

ax.set_yticks(range(len(tasks)))
ax.set_yticklabels(tasks)
ax.set_xlabel('Weeks')
ax.set_title('Project Gantt Chart', fontsize=14)
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()
plt.close(fig)
print(f"  Gantt chart: 5 tasks")


# =====================================================================
#   PARTE 19: SPARKLINES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: SPARKLINES ===")
print("=" * 80)

"""
Sparklines: mini-graficos inline para dashboards.
"""

fig, axes = plt.subplots(4, 1, figsize=(6, 3))

metrics_names = ['Revenue', 'Users', 'Conv Rate', 'NPS']
for i, (ax, name) in enumerate(zip(axes, metrics_names)):
    data_spark = np.random.randn(30).cumsum() + 50
    ax.plot(data_spark, color='#1976D2', linewidth=1)
    ax.fill_between(range(30), data_spark, alpha=0.1, color='#1976D2')
    ax.set_xlim(0, 29)
    ax.axis('off')
    ax.text(-0.15, 0.5, name, transform=ax.transAxes, fontsize=8, va='center')
    ax.text(1.05, 0.5, f'{data_spark[-1]:.0f}', transform=ax.transAxes, fontsize=8, va='center')

fig.suptitle('KPI Sparklines', fontsize=10)
fig.tight_layout()
plt.close(fig)
print(f"  Sparklines: 4 KPI metrics")


# =====================================================================
#   PARTE 20: PRECISION-RECALL CURVE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 20: PRECISION-RECALL ===")
print("=" * 80)

fig, ax = plt.subplots(figsize=(7, 7))

recall = np.array([0, 0.1, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
precision = np.array([1.0, 0.98, 0.95, 0.92, 0.88, 0.82, 0.75, 0.65, 0.50, 0.30])

ax.plot(recall, precision, 'b-', linewidth=2, label='Model')
ax.fill_between(recall, precision, alpha=0.1, color='blue')
ax.set_title('Precision-Recall Curve', fontsize=14)
ax.set_xlabel('Recall')
ax.set_ylabel('Precision')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend()
ax.grid(True, alpha=0.3)
plt.close(fig)
print(f"  Precision-Recall curve")


# =====================================================================
#   PARTE 21: RESIDUAL PLOT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 21: RESIDUAL PLOT ===")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

np.random.seed(42)
predictions = np.linspace(0, 10, 100)
residuals = np.random.randn(100) * 0.5

axes[0].scatter(predictions, residuals, alpha=0.5, color='#1976D2', s=20)
axes[0].axhline(y=0, color='red', linestyle='--')
axes[0].set_title('Residuals vs Predicted')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Residual')
axes[0].grid(True, alpha=0.3)

axes[1].hist(residuals, bins=20, color='#1976D2', alpha=0.7, edgecolor='white', orientation='horizontal')
axes[1].axhline(y=0, color='red', linestyle='--')
axes[1].set_title('Residual Distribution')
axes[1].set_xlabel('Count')

fig.tight_layout()
plt.close(fig)
print(f"  Residual plot: scatter + distribution")


# =====================================================================
#   PARTE 22: PUBLICATION-READY PANEL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 22: PUBLICATION-READY ===")
print("=" * 80)

"""
Para papers: usar rcParams optimizados.
"""

pub_style = {
    'font.family': 'serif',
    'font.size': 11,
    'axes.linewidth': 1.2,
    'axes.labelsize': 12,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'legend.fontsize': 10,
    'figure.dpi': 150,
}

with plt.rc_context(pub_style):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    x = np.linspace(0, 5, 50)
    axes[0].plot(x, np.exp(-x), 'k-', linewidth=1.5)
    axes[0].set_xlabel(r'$\tau$ (s)')
    axes[0].set_ylabel(r'$e^{-\tau}$')
    axes[0].set_title('(a) Exponential Decay')
    
    axes[1].plot(x, np.sin(2*np.pi*x), 'k-', linewidth=1.5)
    axes[1].set_xlabel(r'$t$ (s)')
    axes[1].set_ylabel(r'$\sin(2\pi t)$')
    axes[1].set_title('(b) Sinusoidal')
    
    axes[2].plot(x, x**2, 'k-', linewidth=1.5)
    axes[2].set_xlabel(r'$x$')
    axes[2].set_ylabel(r'$x^2$')
    axes[2].set_title('(c) Quadratic')
    
    for ax in axes:
        ax.grid(True, alpha=0.2)
    
    fig.tight_layout()
    plt.close(fig)

print(f"  Publication panel: 3 subplots with LaTeX labels")


# =====================================================================
#   PARTE 23: HEXBIN Y DENSITY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 23: HEXBIN ===")
print("=" * 80)

"""
Hexbin: alternativa a scatter para datos densos.
Agrupa puntos en hexagonos y colorea por densidad.
"""

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

np.random.seed(42)
x_hex = np.random.randn(10000)
y_hex = x_hex * 0.5 + np.random.randn(10000) * 0.8

axes[0].hexbin(x_hex, y_hex, gridsize=30, cmap='YlOrRd', mincnt=1)
axes[0].set_title('Hexbin (density)')
fig.colorbar(axes[0].collections[0], ax=axes[0], label='Count')

# 2D histogram
axes[1].hist2d(x_hex, y_hex, bins=40, cmap='viridis')
axes[1].set_title('2D Histogram')
fig.colorbar(axes[1].collections[0], ax=axes[1], label='Count')

fig.tight_layout()
plt.close(fig)
print(f"  Hexbin + 2D histogram: 10k points")


# =====================================================================
#   PARTE 24: MEMORY MANAGEMENT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 24: MEMORY ===")
print("=" * 80)

"""
Matplotlib consume mucha memoria con muchos plots.
REGLAS:
1. plt.close(fig) despues de cada plot.
2. plt.close('all') para cerrar todo.
3. Usar backend Agg para scripts (no GUI).
4. gc.collect() si es necesario.
"""

import gc

# Crear y cerrar 100 figuras
for i in range(100):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    plt.close(fig)

gc.collect()
print(f"  Created and closed 100 figures")
print(f"  Rule: ALWAYS plt.close(fig) after savefig/processing")
print(f"  Rule: Use Agg backend for non-interactive scripts")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE MATPLOTLIB:

1. SIEMPRE usar OO interface (fig, ax = plt.subplots()).
2. Figure > Axes > Artists (jerarquia).
3. GridSpec para layouts complejos.
4. plt.rc_context() para temas custom.
5. annotate() para señalar puntos importantes.
6. Colormaps: viridis (sequential), coolwarm (diverging), tab10 (qualitative).
7. savefig(dpi=300, bbox_inches='tight') para publicacion.
8. twinx() para doble eje Y.
9. plt.close(fig) para liberar memoria.

Siguiente archivo: Visualizacion avanzada.
"""

print("\n FIN DE ARCHIVO 02_visualizacion_matplotlib.")
print(" Matplotlib ha sido dominado.")
