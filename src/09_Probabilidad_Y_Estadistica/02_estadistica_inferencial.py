# ===========================================================================
# 02_estadistica_inferencial.py
# ===========================================================================
# MODULO 09: PROBABILIDAD Y ESTADISTICA
# ARCHIVO 02: Estadistica Inferencial y Tests de Hipotesis
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar inferencia estadistica: estimacion, tests de hipotesis,
# intervalos de confianza, A/B testing, ANOVA.
#
# CONTENIDO:
#   1. Estimadores: sesgo, varianza, MSE.
#   2. Maximum Likelihood Estimation (MLE).
#   3. Intervalos de confianza.
#   4. Tests de hipotesis: z-test, t-test.
#   5. P-values y significancia.
#   6. Chi-squared test.
#   7. A/B testing.
#   8. Multiple testing correction.
#   9. ANOVA.
#   10. Nonparametric tests.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
from collections import Counter
import time


# =====================================================================
#   PARTE 1: ESTIMADORES
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: PROPIEDADES DE ESTIMADORES ===")
print("=" * 80)

"""
Un estimador θ̂ es una funcion de los datos para estimar un parametro θ.

Propiedades deseables:
1. Insesgado: E[θ̂] = θ
2. Consistente: θ̂ -> θ cuando n -> ∞
3. Eficiente: menor varianza posible

MSE(θ̂) = Bias² + Varianza (bias-variance tradeoff!)
"""

print("\n--- Sesgo de estimadores de varianza ---")

np.random.seed(42)
true_mu = 5.0
true_var = 4.0  # σ² = 4

n_experiments = 10000
n_samples = 10

biased_vars = []
unbiased_vars = []

for _ in range(n_experiments):
    sample = np.random.normal(true_mu, np.sqrt(true_var), n_samples)
    biased_vars.append(sample.var())          # dividir por n
    unbiased_vars.append(sample.var(ddof=1))  # dividir por n-1

print(f"  True variance: {true_var:.4f}")
print(f"  Biased (1/n):   E[S²] = {np.mean(biased_vars):.4f} (sesgo: {np.mean(biased_vars) - true_var:.4f})")
print(f"  Unbiased (1/(n-1)): E[S²] = {np.mean(unbiased_vars):.4f} (sesgo: {np.mean(unbiased_vars) - true_var:.4f})")


# =====================================================================
#   PARTE 2: MAXIMUM LIKELIHOOD ESTIMATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: MAXIMUM LIKELIHOOD ESTIMATION ===")
print("=" * 80)

"""
MLE: encontrar parametros que maximizan la probabilidad de los datos.
θ_MLE = argmax_θ P(data|θ) = argmax_θ Σ log P(x_i|θ)

EN ML: training = MLE del loss function.
- Regresion con MSE = MLE asumiendo errores gaussianos.
- Clasificacion con CE = MLE de Bernoulli/Categorical.
"""

print("\n--- MLE para Normal ---")

# Datos
np.random.seed(42)
true_mu = 3.0
true_sigma = 2.0
data = np.random.normal(true_mu, true_sigma, size=100)

# MLE analitico para Normal: μ_MLE = x̄, σ²_MLE = (1/n)Σ(x-x̄)²
mu_mle = data.mean()
sigma2_mle = data.var()  # biased version IS the MLE

print(f"  True: μ={true_mu}, σ={true_sigma}")
print(f"  MLE:  μ={mu_mle:.4f}, σ={np.sqrt(sigma2_mle):.4f}")


print("\n--- MLE para Bernoulli ---")

# Datos binarios
data_bin = np.array([1, 1, 0, 1, 1, 0, 1, 0, 1, 1])
p_mle = data_bin.mean()
print(f"  Datos: {data_bin}")
print(f"  MLE de p: {p_mle:.4f}")


print("\n--- MLE con gradient descent ---")

def neg_log_likelihood_normal(params, data):
    """Negative log-likelihood para Normal."""
    mu, log_sigma = params
    sigma = np.exp(log_sigma)
    n = len(data)
    nll = 0.5 * n * np.log(2 * np.pi * sigma**2) + np.sum((data - mu)**2) / (2 * sigma**2)
    return nll

def grad_nll_normal(params, data):
    """Gradiente de la NLL."""
    mu, log_sigma = params
    sigma = np.exp(log_sigma)
    n = len(data)
    
    dmu = -np.sum(data - mu) / sigma**2
    dsigma = n - np.sum((data - mu)**2) / sigma**2
    dlog_sigma = dsigma * sigma  # chain rule: d/d(log_σ) = d/dσ * σ
    
    return np.array([dmu, -dlog_sigma])

# Optimizar
params = np.array([0.0, 0.0])  # mu=0, log_sigma=0 -> sigma=1
lr = 0.01

for i in range(500):
    grad = grad_nll_normal(params, data)
    params -= lr * grad

mu_gd = params[0]
sigma_gd = np.exp(params[1])

print(f"\n  MLE via GD:")
print(f"    μ = {mu_gd:.4f} (analitico: {mu_mle:.4f})")
print(f"    σ = {sigma_gd:.4f} (analitico: {np.sqrt(sigma2_mle):.4f})")


# =====================================================================
#   PARTE 3: INTERVALOS DE CONFIANZA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: INTERVALOS DE CONFIANZA ===")
print("=" * 80)

"""
CI: rango donde esperamos que este el parametro con cierta confianza.
95% CI para la media: x̄ ± 1.96 * σ/√n (si σ conocida)
                      x̄ ± t_{0.025,n-1} * s/√n (si σ desconocida)
"""

print("\n--- CI para la media ---")

def confidence_interval(data, confidence=0.95):
    """CI usando t-distribution."""
    n = len(data)
    mean = data.mean()
    se = data.std(ddof=1) / np.sqrt(n)
    
    # Aproximacion: z para n grande
    z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[confidence]
    
    return mean - z * se, mean + z * se

for n in [10, 30, 100, 1000]:
    sample = np.random.normal(true_mu, true_sigma, n)
    ci_low, ci_high = confidence_interval(sample)
    contains = ci_low <= true_mu <= ci_high
    print(f"  n={n:4d}: CI=[{ci_low:.4f}, {ci_high:.4f}], "
          f"width={ci_high-ci_low:.4f}, contains_true={'SI' if contains else 'NO'}")


print("\n--- Cobertura del CI ---")

np.random.seed(42)
n_experiments = 10000
n_samples = 30
coverage_count = 0

for _ in range(n_experiments):
    sample = np.random.normal(true_mu, true_sigma, n_samples)
    ci_low, ci_high = confidence_interval(sample)
    if ci_low <= true_mu <= ci_high:
        coverage_count += 1

coverage = coverage_count / n_experiments
print(f"  Cobertura real del 95% CI: {coverage:.4f} (esperado: 0.95)")


# =====================================================================
#   PARTE 4: TESTS DE HIPOTESIS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: TESTS DE HIPOTESIS ===")
print("=" * 80)

"""
H0: hipotesis nula (no hay efecto).
H1: hipotesis alternativa (hay efecto).

Procedimiento:
1. Formular H0 y H1.
2. Elegir estadistico de test.
3. Calcular p-value.
4. Comparar con α (tipicamente 0.05).
5. Rechazar H0 si p < α.

Errores:
- Tipo I (falso positivo): rechazar H0 cuando es verdadera. P = α.
- Tipo II (falso negativo): no rechazar H0 cuando es falsa. P = β.
- Power = 1 - β.
"""

print("\n--- z-test para la media ---")

def z_test(sample, mu_0, sigma_known):
    """z-test de una muestra."""
    n = len(sample)
    z = (sample.mean() - mu_0) / (sigma_known / np.sqrt(n))
    
    # p-value (bilateral)
    p_value = 2 * (1 - 0.5 * (1 + np.math.erf(abs(z) / np.sqrt(2))))
    
    return z, p_value

# Test: ¿la media es 5?
np.random.seed(42)
sample1 = np.random.normal(5.3, 2, 50)  # media real = 5.3, H0: μ=5

z_stat, p_val = z_test(sample1, mu_0=5.0, sigma_known=2.0)
print(f"  H0: μ = 5.0")
print(f"  Sample mean: {sample1.mean():.4f}")
print(f"  z = {z_stat:.4f}")
print(f"  p-value = {p_val:.4f}")
print(f"  Resultado: {'Rechazar H0' if p_val < 0.05 else 'No rechazar H0'} (α=0.05)")


print("\n--- t-test para dos muestras ---")

def two_sample_t_test(sample1, sample2):
    """t-test de dos muestras independientes (Welch's)."""
    n1, n2 = len(sample1), len(sample2)
    m1, m2 = sample1.mean(), sample2.mean()
    v1, v2 = sample1.var(ddof=1), sample2.var(ddof=1)
    
    se = np.sqrt(v1/n1 + v2/n2)
    t = (m1 - m2) / se
    
    # Grados de libertad de Welch
    df = (v1/n1 + v2/n2)**2 / ((v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1))
    
    # p-value aproximado
    p_value = 2 * (1 - 0.5 * (1 + np.math.erf(abs(t) / np.sqrt(2))))
    
    return t, p_value, df

# Dos grupos con diferente media
group_A = np.random.normal(10, 2, 50)
group_B = np.random.normal(11, 2, 50)

t_stat, p_val, df = two_sample_t_test(group_A, group_B)
print(f"  Group A: mean={group_A.mean():.4f}, std={group_A.std():.4f}")
print(f"  Group B: mean={group_B.mean():.4f}, std={group_B.std():.4f}")
print(f"  t = {t_stat:.4f}, p = {p_val:.4f}, df = {df:.1f}")
print(f"  Resultado: {'Rechazar H0' if p_val < 0.05 else 'No rechazar H0'}")


print("\n--- Paired t-test ---")

def paired_t_test(before, after):
    """t-test pareado."""
    diff = after - before
    n = len(diff)
    t = diff.mean() / (diff.std(ddof=1) / np.sqrt(n))
    p_value = 2 * (1 - 0.5 * (1 + np.math.erf(abs(t) / np.sqrt(2))))
    return t, p_value

before = np.random.normal(100, 15, 30)
after = before + np.random.normal(5, 8, 30)  # mejora de ~5

t_paired, p_paired = paired_t_test(before, after)
print(f"  Paired: mean_diff = {(after - before).mean():.4f}")
print(f"  t = {t_paired:.4f}, p = {p_paired:.4f}")


# =====================================================================
#   PARTE 5: CHI-SQUARED TEST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: CHI-SQUARED TEST ===")
print("=" * 80)

"""
Test de bondad de ajuste: ¿los datos siguen una distribucion esperada?
χ² = Σ (O_i - E_i)² / E_i
"""

print("\n--- Chi-squared: dado justo? ---")

def chi_squared_test(observed, expected):
    """Chi-squared goodness of fit."""
    chi2 = np.sum((observed - expected)**2 / expected)
    df = len(observed) - 1
    # p-value aproximado usando tabla chi2
    # Para simplificar usamos chi2 > critical_value
    critical_values = {5: 11.07, 4: 9.49, 3: 7.81}  # df -> crit@0.05
    p_approx = "< 0.05" if chi2 > critical_values.get(df, 10) else "> 0.05"
    return chi2, df, p_approx

# Dado posiblemente cargado
np.random.seed(42)
loaded_die = np.random.choice([1,2,3,4,5,6], size=600, p=[0.1, 0.1, 0.2, 0.2, 0.2, 0.2])
counts = np.array([np.sum(loaded_die == i) for i in range(1, 7)])
expected = np.ones(6) * 100

chi2, df, p = chi_squared_test(counts, expected)
print(f"  Observed: {counts}")
print(f"  Expected: {expected.astype(int)}")
print(f"  χ² = {chi2:.4f}, df = {df}, p {p}")

# Dado justo
fair_die = np.random.choice([1,2,3,4,5,6], size=600)
counts_fair = np.array([np.sum(fair_die == i) for i in range(1, 7)])
chi2_f, df_f, p_f = chi_squared_test(counts_fair, expected)
print(f"\n  Dado justo:")
print(f"  Observed: {counts_fair}")
print(f"  χ² = {chi2_f:.4f}, p {p_f}")


# =====================================================================
#   PARTE 6: A/B TESTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: A/B TESTING ===")
print("=" * 80)

"""
A/B testing: comparar dos variantes.
1. Definir metrica (CTR, conversion, revenue).
2. Calcular sample size necesario.
3. Ejecutar experimento.
4. Analizar resultados.
"""

print("\n--- A/B test de conversion ---")

def ab_test(conversions_a, total_a, conversions_b, total_b):
    """Test de proporciones para A/B testing."""
    p_a = conversions_a / total_a
    p_b = conversions_b / total_b
    
    # Pooled proportion
    p_pool = (conversions_a + conversions_b) / (total_a + total_b)
    
    se = np.sqrt(p_pool * (1 - p_pool) * (1/total_a + 1/total_b))
    z = (p_b - p_a) / se
    
    p_value = 2 * (1 - 0.5 * (1 + np.math.erf(abs(z) / np.sqrt(2))))
    
    lift = (p_b - p_a) / p_a
    
    return {
        'p_a': p_a, 'p_b': p_b,
        'z': z, 'p_value': p_value,
        'lift': lift,
        'significant': p_value < 0.05
    }

# Simular A/B test
np.random.seed(42)
n_a, n_b = 5000, 5000
true_rate_a, true_rate_b = 0.10, 0.12

clicks_a = np.random.binomial(1, true_rate_a, n_a).sum()
clicks_b = np.random.binomial(1, true_rate_b, n_b).sum()

result = ab_test(clicks_a, n_a, clicks_b, n_b)

print(f"  Control (A): {result['p_a']:.4f} ({clicks_a}/{n_a})")
print(f"  Treatment (B): {result['p_b']:.4f} ({clicks_b}/{n_b})")
print(f"  Lift: {result['lift']:.2%}")
print(f"  z = {result['z']:.4f}")
print(f"  p-value = {result['p_value']:.4f}")
print(f"  Significativo: {'SI' if result['significant'] else 'NO'}")


print("\n--- Sample size calculation ---")

def required_sample_size(p1, mde, alpha=0.05, power=0.8):
    """Calcular tamaño de muestra necesario."""
    p2 = p1 * (1 + mde)
    z_alpha = 1.96  # two-sided 0.05
    z_beta = 0.84   # power 0.8
    
    p_avg = (p1 + p2) / 2
    n = ((z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) +
          z_beta * np.sqrt(p1*(1-p1) + p2*(1-p2)))**2) / (p2 - p1)**2
    
    return int(np.ceil(n))

baseline = 0.10
for mde in [0.05, 0.10, 0.15, 0.20, 0.30]:
    n_required = required_sample_size(baseline, mde)
    print(f"  MDE={mde:.0%}: n={n_required:,d} por grupo")


# =====================================================================
#   PARTE 7: MULTIPLE TESTING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: MULTIPLE TESTING CORRECTION ===")
print("=" * 80)

"""
Si haces M tests con α=0.05:
P(al menos 1 falso positivo) = 1 - (1-α)^M

Con M=20, P(falso positivo) = 0.64!

Correcciones:
1. Bonferroni: α_adj = α/M (conservador).
2. Holm: escalon (menos conservador).
3. FDR (Benjamini-Hochberg): controla false discovery rate.
"""

print("\n--- Problema de multiple testing ---")

np.random.seed(42)
n_tests = 20
p_values = []

for i in range(n_tests):
    # Todos son H0 verdadera (no hay efecto)
    sample = np.random.normal(0, 1, 30)
    t = sample.mean() / (sample.std(ddof=1) / np.sqrt(30))
    p = 2 * (1 - 0.5 * (1 + np.math.erf(abs(t) / np.sqrt(2))))
    p_values.append(p)

p_values = np.array(p_values)
false_positives = (p_values < 0.05).sum()
print(f"  {n_tests} tests (todos H0 verdadera):")
print(f"  Falsos positivos sin correccion: {false_positives}/{n_tests}")


print("\n--- Bonferroni correction ---")

alpha_bonf = 0.05 / n_tests
fp_bonf = (p_values < alpha_bonf).sum()
print(f"  α ajustado: {alpha_bonf:.4f}")
print(f"  Falsos positivos: {fp_bonf}/{n_tests}")


print("\n--- Benjamini-Hochberg (FDR) ---")

def benjamini_hochberg(p_values, alpha=0.05):
    """FDR correction."""
    n = len(p_values)
    sorted_idx = np.argsort(p_values)
    sorted_p = p_values[sorted_idx]
    
    rejected = np.zeros(n, dtype=bool)
    for i in range(n-1, -1, -1):
        threshold = alpha * (i + 1) / n
        if sorted_p[i] <= threshold:
            rejected[sorted_idx[:i+1]] = True
            break
    
    return rejected

rejected_bh = benjamini_hochberg(p_values)
print(f"  FDR rechazados: {rejected_bh.sum()}/{n_tests}")


# =====================================================================
#   PARTE 8: ANOVA
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: ANOVA ===")
print("=" * 80)

"""
ANOVA: comparar medias de 3+ grupos.
H0: μ_1 = μ_2 = ... = μ_k
F = varianza_entre / varianza_dentro
"""

print("\n--- One-way ANOVA ---")

def one_way_anova(*groups):
    """ANOVA de un factor."""
    k = len(groups)
    N = sum(len(g) for g in groups)
    grand_mean = np.concatenate(groups).mean()
    
    # Sum of squares between
    ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
    
    # Sum of squares within
    ss_within = sum(np.sum((g - g.mean())**2) for g in groups)
    
    df_between = k - 1
    df_within = N - k
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    f_stat = ms_between / ms_within
    
    return {
        'f_stat': f_stat,
        'ss_between': ss_between,
        'ss_within': ss_within,
        'df_between': df_between,
        'df_within': df_within,
    }

# 3 grupos con diferentes medias
np.random.seed(42)
group1 = np.random.normal(10, 2, 30)
group2 = np.random.normal(12, 2, 30)
group3 = np.random.normal(11, 2, 30)

anova_result = one_way_anova(group1, group2, group3)
print(f"  Group means: {group1.mean():.2f}, {group2.mean():.2f}, {group3.mean():.2f}")
print(f"  F = {anova_result['f_stat']:.4f}")
print(f"  df = ({anova_result['df_between']}, {anova_result['df_within']})")

# 3 grupos con misma media
group4 = np.random.normal(10, 2, 30)
group5 = np.random.normal(10, 2, 30)
group6 = np.random.normal(10, 2, 30)

anova_null = one_way_anova(group4, group5, group6)
print(f"\n  Null groups: F = {anova_null['f_stat']:.4f} (deberia ser ~1)")


# =====================================================================
#   PARTE 9: EFFECT SIZE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: EFFECT SIZE Y POWER ===")
print("=" * 80)

"""
P-value solo dice si el efecto es SIGNIFICATIVO, no si es GRANDE.
Effect size mide la MAGNITUD del efecto.

Cohen's d = (μ₁ - μ₂) / s_pooled
d < 0.2: pequeño
d ~ 0.5: mediano
d > 0.8: grande
"""

print("\n--- Cohen's d ---")

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    s_pooled = np.sqrt(((n1-1)*group1.var(ddof=1) + (n2-1)*group2.var(ddof=1)) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / s_pooled

# Efecto grande con p significativo
g1 = np.random.normal(10, 2, 100)
g2 = np.random.normal(12, 2, 100)
d = cohens_d(g2, g1)
_, p = two_sample_t_test(g1, g2)
print(f"  Grande:  d={d:.4f}, p={p:.4f}")

# Efecto pequeño con p significativo (muestra grande)
g3 = np.random.normal(10, 2, 10000)
g4 = np.random.normal(10.1, 2, 10000)
d2 = cohens_d(g4, g3)
_, p2 = two_sample_t_test(g3, g4)
print(f"  Pequeño: d={d2:.4f}, p={p2:.4f}")
print(f"  (p significativo pero efecto trivial!)")


print("\n--- Statistical Power ---")

"""
Power = 1 - β = P(rechazar H0 | H0 es falsa)
Mas power = menos falsos negativos.
"""

def simulate_power(true_diff, n, sigma=2, alpha=0.05, n_sim=5000):
    rejections = 0
    for _ in range(n_sim):
        g1 = np.random.normal(0, sigma, n)
        g2 = np.random.normal(true_diff, sigma, n)
        _, p = two_sample_t_test(g1, g2)
        if p < alpha:
            rejections += 1
    return rejections / n_sim

print(f"\n  Power para diferentes n y effect sizes:")
print(f"  {'n':>6s}  {'d=0.2':>8s}  {'d=0.5':>8s}  {'d=0.8':>8s}")
for n in [20, 50, 100, 200]:
    powers = []
    for d in [0.2, 0.5, 0.8]:
        true_diff = d * 2  # sigma=2
        pwr = simulate_power(true_diff, n, sigma=2, n_sim=1000)
        powers.append(pwr)
    print(f"  {n:6d}  {powers[0]:8.3f}  {powers[1]:8.3f}  {powers[2]:8.3f}")


# =====================================================================
#   PARTE 10: NONPARAMETRIC TESTS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: TESTS NO PARAMETRICOS ===")
print("=" * 80)

"""
Cuando los datos NO son normales:
- Mann-Whitney U: alternativa a t-test.
- Wilcoxon signed-rank: alternativa a paired t-test.
- Kruskal-Wallis: alternativa a ANOVA.
- Permutation test: no asume nada.
"""

print("\n--- Permutation test ---")

def permutation_test(group1, group2, n_permutations=10000):
    """Test de permutaciones."""
    observed_diff = group1.mean() - group2.mean()
    combined = np.concatenate([group1, group2])
    n1 = len(group1)
    
    count = 0
    for _ in range(n_permutations):
        np.random.shuffle(combined)
        perm_diff = combined[:n1].mean() - combined[n1:].mean()
        if abs(perm_diff) >= abs(observed_diff):
            count += 1
    
    p_value = count / n_permutations
    return observed_diff, p_value

# Test con datos no normales (exponencial)
np.random.seed(42)
g_exp1 = np.random.exponential(2, 30)
g_exp2 = np.random.exponential(3, 30)

diff, p_perm = permutation_test(g_exp1, g_exp2)
print(f"  Datos exponenciales:")
print(f"    Mean diff: {diff:.4f}")
print(f"    Permutation p-value: {p_perm:.4f}")

# Comparar con t-test
_, p_t = two_sample_t_test(g_exp1, g_exp2)
print(f"    t-test p-value: {p_t:.4f}")


print("\n--- Mann-Whitney U test ---")

"""
Mann-Whitney U: compara distribuciones sin asumir normalidad.
Basado en rankings.
"""

def mann_whitney_u(group1, group2):
    """Mann-Whitney U test simplificado."""
    combined = np.concatenate([group1, group2])
    ranks = np.argsort(np.argsort(combined)) + 1  # Ranking
    
    n1 = len(group1)
    n2 = len(group2)
    
    R1 = ranks[:n1].sum()
    U1 = R1 - n1 * (n1 + 1) / 2
    U2 = n1 * n2 - U1
    
    U = min(U1, U2)
    
    # Normal approximation for large samples
    mu_U = n1 * n2 / 2
    sigma_U = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (U - mu_U) / sigma_U
    p_value = 2 * (1 - 0.5 * (1 + np.math.erf(abs(z) / np.sqrt(2))))
    
    return U, z, p_value

U, z_mw, p_mw = mann_whitney_u(g_exp1, g_exp2)
print(f"  Mann-Whitney U = {U:.0f}")
print(f"  z = {z_mw:.4f}, p = {p_mw:.4f}")


# =====================================================================
#   PARTE 11: KOLMOGOROV-SMIRNOV TEST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: KOLMOGOROV-SMIRNOV TEST ===")
print("=" * 80)

"""
KS test: comparar si dos distribuciones son iguales.
D = max |F_1(x) - F_2(x)| (distancia maxima entre CDFs).
"""

print("\n--- KS test ---")

def ks_test_two_sample(sample1, sample2):
    """Two-sample KS test."""
    n1, n2 = len(sample1), len(sample2)
    combined = np.sort(np.concatenate([sample1, sample2]))
    
    cdf1 = np.searchsorted(np.sort(sample1), combined, side='right') / n1
    cdf2 = np.searchsorted(np.sort(sample2), combined, side='right') / n2
    
    D = np.max(np.abs(cdf1 - cdf2))
    
    # Aproximacion de p-value
    n_eff = np.sqrt(n1 * n2 / (n1 + n2))
    return D, n_eff

# Mismo distribucion
np.random.seed(42)
s1 = np.random.normal(0, 1, 200)
s2 = np.random.normal(0, 1, 200)
D_same, n_eff = ks_test_two_sample(s1, s2)
print(f"  Misma dist: D = {D_same:.4f}")

# Diferente distribucion
s3 = np.random.normal(0.5, 1, 200)
D_diff, _ = ks_test_two_sample(s1, s3)
print(f"  Diff (shift=0.5): D = {D_diff:.4f}")

# Muy diferente
s4 = np.random.exponential(1, 200)
D_very, _ = ks_test_two_sample(s1, s4)
print(f"  Normal vs Exp: D = {D_very:.4f}")


# =====================================================================
#   PARTE 12: BOOTSTRAP AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: BOOTSTRAP AVANZADO ===")
print("=" * 80)

"""
Bootstrap para cualquier estadistico, no solo la media.
Util para: mediana, correlacion, coeficientes de regresion.
"""

print("\n--- Bootstrap para mediana ---")

np.random.seed(42)
data_skewed = np.random.exponential(2, 100)

n_boot = 5000
boot_medians = []
for _ in range(n_boot):
    resample = np.random.choice(data_skewed, len(data_skewed), replace=True)
    boot_medians.append(np.median(resample))

boot_medians = np.array(boot_medians)
print(f"  Mediana de datos: {np.median(data_skewed):.4f}")
print(f"  Bootstrap 95% CI: [{np.percentile(boot_medians, 2.5):.4f}, "
      f"{np.percentile(boot_medians, 97.5):.4f}]")


print("\n--- Bootstrap para coeficiente de regresion ---")

np.random.seed(42)
n = 50
X_boot = np.random.randn(n)
y_boot = 2.5 * X_boot + np.random.randn(n)

boot_slopes = []
for _ in range(n_boot):
    idx = np.random.choice(n, n, replace=True)
    X_b = X_boot[idx]
    y_b = y_boot[idx]
    slope = np.sum(X_b * y_b) / np.sum(X_b**2)
    boot_slopes.append(slope)

boot_slopes = np.array(boot_slopes)
print(f"  Slope OLS: {np.sum(X_boot * y_boot) / np.sum(X_boot**2):.4f}")
print(f"  Bootstrap 95% CI: [{np.percentile(boot_slopes, 2.5):.4f}, "
      f"{np.percentile(boot_slopes, 97.5):.4f}]")


# =====================================================================
#   PARTE 13: MLE AVANZADO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: MLE PARA OTRAS DISTRIBUCIONES ===")
print("=" * 80)

print("\n--- MLE para Poisson ---")

"""
Poisson: P(X=k) = e^{-λ} λ^k / k!
Log-likelihood: L(λ) = Σ (k_i log(λ) - λ - log(k_i!))
dL/dλ = Σ k_i / λ - n = 0
λ_MLE = x̄
"""

np.random.seed(42)
true_lambda = 4.5
poisson_data = np.random.poisson(true_lambda, 200)

lambda_mle = poisson_data.mean()
print(f"  True λ = {true_lambda}")
print(f"  MLE λ = {lambda_mle:.4f}")

# NLL via GD
param = np.array([1.0])  # log(lambda)
for _ in range(200):
    lam = np.exp(param[0])
    grad = -(poisson_data.mean() / lam - 1) * lam  # chain rule
    param -= 0.01 * grad

print(f"  MLE via GD: λ = {np.exp(param[0]):.4f}")


print("\n--- MLE para Regression (MSE = Normal MLE) ---")

"""
MSE loss ≡ Negative log-likelihood de Normal:
-log P(y|X,w,σ²) = n/2 log(2πσ²) + ||y - Xw||² / (2σ²)

Minimizar NLL w.r.t w = minimizar MSE.
"""

np.random.seed(42)
n, d = 100, 3
X_reg = np.random.randn(n, d)
w_true = np.array([2.0, -1.0, 0.5])
sigma_noise = 1.5
y_reg = X_reg @ w_true + np.random.randn(n) * sigma_noise

# OLS = MLE
w_mle = np.linalg.lstsq(X_reg, y_reg, rcond=None)[0]
residuals = y_reg - X_reg @ w_mle
sigma_mle = np.sqrt(np.mean(residuals**2))

print(f"\n  True:  w = {w_true}, σ = {sigma_noise}")
print(f"  MLE:   w = [{w_mle[0]:.4f}, {w_mle[1]:.4f}, {w_mle[2]:.4f}], σ = {sigma_mle:.4f}")


# =====================================================================
#   PARTE 14: SUMMARY STATISTICS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: SUMMARY STATISTICS COMPLETAS ===")
print("=" * 80)

"""
Resumen estadistico completo de un dataset.
"""

print("\n--- Summary statistics ---")

def full_summary(data, name="Data"):
    """Resumen estadistico completo."""
    print(f"\n  {name} (n={len(data)}):")
    print(f"    Mean:     {np.mean(data):.4f}")
    print(f"    Median:   {np.median(data):.4f}")
    print(f"    Std:      {np.std(data, ddof=1):.4f}")
    print(f"    Min:      {np.min(data):.4f}")
    print(f"    Max:      {np.max(data):.4f}")
    print(f"    Q1 (25%): {np.percentile(data, 25):.4f}")
    print(f"    Q3 (75%): {np.percentile(data, 75):.4f}")
    print(f"    IQR:      {np.percentile(data, 75) - np.percentile(data, 25):.4f}")
    
    # Outliers (IQR method)
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    outliers = np.sum((data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr))
    print(f"    Outliers: {outliers}")

np.random.seed(42)
full_summary(np.random.normal(100, 15, 500), "Normal(100,15)")
full_summary(np.random.exponential(10, 500), "Exponential(10)")


# =====================================================================
#   PARTE 15: FISHER INFORMATION Y CRAMER-RAO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: FISHER INFORMATION ===")
print("=" * 80)

"""
Fisher Information: cuanta informacion sobre θ contienen los datos.
I(θ) = E[(d/dθ log p(x|θ))²]

Cramer-Rao bound: Var(θ̂) >= 1/I(θ)
El MLE alcanza el CRB asintoticamente.

EN ML: geometria del espacio de parametros (Natural Gradient).
"""

print("\n--- Fisher Information para Normal ---")

"""
Normal N(μ, σ²):
I(μ) = n/σ² (mas datos o menos ruido = mas informacion)
I(σ²) = n/(2σ⁴)

Cramer-Rao: Var(μ̂) >= σ²/n
"""

for n in [10, 50, 100, 500, 1000]:
    for sigma in [1.0, 2.0]:
        fisher_mu = n / sigma**2
        crb = 1.0 / fisher_mu
        
        # Verificar empiricamente
        variances = []
        for _ in range(1000):
            sample = np.random.normal(0, sigma, n)
            variances.append(sample.mean())
        empirical_var = np.var(variances)
        
        print(f"  n={n:4d}, σ={sigma}: CRB={crb:.6f}, Var(x̄)={empirical_var:.6f}")


print("\n--- Fisher Information para Bernoulli ---")

"""
Bernoulli(p): I(p) = n/(p(1-p))
CRB: Var(p̂) >= p(1-p)/n
"""

for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
    n = 100
    fi = n / (p * (1-p))
    crb = 1.0 / fi
    
    # Empirico
    ests = [np.random.binomial(n, p) / n for _ in range(5000)]
    emp_var = np.var(ests)
    
    print(f"  p={p:.1f}: I={fi:8.2f}, CRB={crb:.6f}, Var(p̂)={emp_var:.6f}")

print("""
  NOTA: Estadistico suficiente
  T(X) es suficiente para θ si P(X|T, θ) = P(X|T).
  Para Normal: (x̄, s²) es suficiente para (μ, σ²).
  Para Bernoulli: Σx_i es suficiente para p.
  En ML: features son "estadisticos suficientes" de los datos crudos.
""")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE ESTADISTICA INFERENCIAL:

1. Estimadores: sesgo, varianza, MSE = bias² + varianza.

2. MLE: maximizar likelihood = minimizar loss en ML.

3. Intervalos de confianza: rango del parametro.

4. t-test/z-test: comparar medias entre grupos.

5. Chi-squared: bondad de ajuste.

6. A/B testing: sample size, lift, significancia.

7. Multiple testing: Bonferroni, BH-FDR.

8. ANOVA: comparar 3+ grupos.

9. Mann-Whitney, KS: tests no parametricos.

10. Bootstrap: CI para cualquier estadistico.

Siguiente archivo: Estadistica para ML.
"""

print("\n FIN DE ARCHIVO 02_estadistica_inferencial.")
print(" Estadistica inferencial ha sido dominada.")
