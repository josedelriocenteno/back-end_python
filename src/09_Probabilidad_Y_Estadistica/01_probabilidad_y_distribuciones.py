# ===========================================================================
# 01_probabilidad_y_distribuciones.py
# ===========================================================================
# MODULO 09: PROBABILIDAD Y ESTADISTICA
# ARCHIVO 01: Probabilidad Fundamental y Distribuciones
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Dominar probabilidad desde axiomas hasta distribuciones usadas en ML:
# Bernoulli, Binomial, Poisson, Normal, Exponencial, Uniforme, Beta.
#
# CONTENIDO:
#   1. Axiomas de probabilidad.
#   2. Probabilidad condicional y Bayes.
#   3. Variables aleatorias discretas.
#   4. Variables aleatorias continuas.
#   5. Distribuciones: Bernoulli, Binomial, Poisson.
#   6. Normal (Gaussiana): la reina de las distribuciones.
#   7. Otras: Exponencial, Uniforme, Beta, Gamma.
#   8. Teorema del limite central.
#   9. Momentos: media, varianza, skewness, kurtosis.
#   10. Ejercicio: simulacion Monte Carlo.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
from collections import Counter
import time


# =====================================================================
#   PARTE 1: AXIOMAS DE PROBABILIDAD
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: AXIOMAS DE PROBABILIDAD ===")
print("=" * 80)

"""
Axiomas de Kolmogorov:
1. P(A) >= 0 para todo evento A.
2. P(Ω) = 1 (probabilidad total = 1).
3. P(A ∪ B) = P(A) + P(B) si A y B son disjuntos.

Reglas derivadas:
- P(A^c) = 1 - P(A)
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- P(A|B) = P(A ∩ B) / P(B)

EN ML:
- P(y|x) es lo que predice un clasificador.
- P(data|params) es el likelihood.
- P(params|data) es el posterior (Bayes).
"""

print("\n--- Probabilidad empirica ---")

np.random.seed(42)
n_trials = 100000

# Dado justo
dado = np.random.randint(1, 7, size=n_trials)
counts = Counter(dado)

print("  Dado justo (100K lanzamientos):")
for face in sorted(counts.keys()):
    empirical = counts[face] / n_trials
    theoretical = 1/6
    print(f"    Cara {face}: P={empirical:.4f} (teorico: {theoretical:.4f})")

# Union e interseccion
A = dado <= 3     # {1,2,3}
B = dado % 2 == 0  # {2,4,6}

P_A = A.mean()
P_B = B.mean()
P_A_and_B = (A & B).mean()
P_A_or_B = (A | B).mean()

print(f"\n  P(A={'{1,2,3}'}) = {P_A:.4f} (teorico: 0.5)")
print(f"  P(B={'{2,4,6}'}) = {P_B:.4f} (teorico: 0.5)")
print(f"  P(A ∩ B) = {P_A_and_B:.4f} (teorico: {1/6:.4f})")
print(f"  P(A ∪ B) = {P_A_or_B:.4f} (teorico: {5/6:.4f})")
print(f"  P(A)+P(B)-P(A∩B) = {P_A + P_B - P_A_and_B:.4f}")


# =====================================================================
#   PARTE 2: PROBABILIDAD CONDICIONAL Y BAYES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: PROBABILIDAD CONDICIONAL Y BAYES ===")
print("=" * 80)

"""
P(A|B) = P(A ∩ B) / P(B)

Teorema de Bayes:
P(A|B) = P(B|A) * P(A) / P(B)

EN ML:
P(clase|features) = P(features|clase) * P(clase) / P(features)
  posterior        =  likelihood      *  prior    / evidence
"""

print("\n--- Bayes: test medico ---")

# Enfermedad rara: 1% prevalencia
# Test: 99% sensitividad, 95% especificidad
prevalence = 0.01
sensitivity = 0.99  # P(test+|enfermo)
specificity = 0.95  # P(test-|sano)

# P(enfermo|test+) = P(test+|enfermo)*P(enfermo) / P(test+)
P_test_pos = sensitivity * prevalence + (1 - specificity) * (1 - prevalence)
P_enfermo_dado_pos = (sensitivity * prevalence) / P_test_pos

print(f"  Prevalencia: {prevalence:.1%}")
print(f"  Sensitividad: {sensitivity:.1%}")
print(f"  Especificidad: {specificity:.1%}")
print(f"  P(test+): {P_test_pos:.4f}")
print(f"  P(enfermo|test+): {P_enfermo_dado_pos:.4f}")
print(f"  !! Solo {P_enfermo_dado_pos:.1%} de los positivos estan enfermos !!")

# Simular
n_people = 1000000
enfermo = np.random.random(n_people) < prevalence
test_pos = np.where(enfermo,
                     np.random.random(n_people) < sensitivity,
                     np.random.random(n_people) < (1 - specificity))

true_pos = (enfermo & test_pos).sum()
all_pos = test_pos.sum()
print(f"\n  Simulacion (1M personas):")
print(f"    P(enfermo|test+) = {true_pos/all_pos:.4f}")


print("\n--- Naive Bayes simplificado ---")

"""
P(clase|x1,x2,...) ∝ P(clase) * ∏ P(xi|clase)
Asume independencia condicional (naive).
"""

class NaiveBayesGaussian:
    """Naive Bayes con features gaussianas."""
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = {}
        self.means = {}
        self.vars = {}
        
        for c in self.classes:
            X_c = X[y == c]
            self.priors[c] = len(X_c) / len(X)
            self.means[c] = X_c.mean(axis=0)
            self.vars[c] = X_c.var(axis=0) + 1e-6
    
    def predict(self, X):
        preds = []
        for x in X:
            posteriors = {}
            for c in self.classes:
                log_prior = np.log(self.priors[c])
                log_likelihood = -0.5 * np.sum(
                    np.log(2 * np.pi * self.vars[c]) +
                    (x - self.means[c])**2 / self.vars[c]
                )
                posteriors[c] = log_prior + log_likelihood
            preds.append(max(posteriors, key=posteriors.get))
        return np.array(preds)

np.random.seed(42)
X_nb = np.vstack([
    np.random.randn(100, 2) + [2, 0],
    np.random.randn(100, 2) + [0, 2],
])
y_nb = np.array([0]*100 + [1]*100)

nb = NaiveBayesGaussian()
nb.fit(X_nb, y_nb)
y_pred = nb.predict(X_nb)
print(f"  Naive Bayes accuracy: {np.mean(y_pred == y_nb):.4f}")


# =====================================================================
#   PARTE 3: VARIABLES ALEATORIAS DISCRETAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: DISTRIBUCIONES DISCRETAS ===")
print("=" * 80)

print("\n--- Bernoulli ---")

"""
X ~ Bernoulli(p): X ∈ {0, 1}
P(X=1) = p, P(X=0) = 1-p
E[X] = p, Var(X) = p(1-p)

EN ML: clasificacion binaria, cada prediccion es Bernoulli.
"""

p = 0.7
bernoulli_samples = (np.random.random(10000) < p).astype(int)

print(f"  Bernoulli(p={p})")
print(f"    E[X] teorico: {p:.4f}, empirico: {bernoulli_samples.mean():.4f}")
print(f"    Var[X] teorico: {p*(1-p):.4f}, empirico: {bernoulli_samples.var():.4f}")


print("\n--- Binomial ---")

"""
X ~ Binomial(n, p): numero de exitos en n intentos.
P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
E[X] = np, Var(X) = np(1-p)
"""

n, p = 20, 0.3
binomial_samples = np.random.binomial(n, p, size=10000)

print(f"  Binomial(n={n}, p={p})")
print(f"    E[X] teorico: {n*p:.4f}, empirico: {binomial_samples.mean():.4f}")
print(f"    Var[X] teorico: {n*p*(1-p):.4f}, empirico: {binomial_samples.var():.4f}")


print("\n--- Poisson ---")

"""
X ~ Poisson(λ): numero de eventos en un intervalo.
P(X=k) = e^(-λ) * λ^k / k!
E[X] = λ, Var(X) = λ

EN ML: count data, eventos raros.
"""

lam = 5.0
poisson_samples = np.random.poisson(lam, size=10000)

print(f"  Poisson(λ={lam})")
print(f"    E[X] teorico: {lam:.4f}, empirico: {poisson_samples.mean():.4f}")
print(f"    Var[X] teorico: {lam:.4f}, empirico: {poisson_samples.var():.4f}")


print("\n--- Categorical ---")

"""
X ~ Categorical(p1, p2, ..., pk): extension de Bernoulli a k clases.
EN ML: softmax output -> Categorical distribution.
"""

probs = np.array([0.5, 0.3, 0.15, 0.05])
categorical_samples = np.random.choice(len(probs), size=10000, p=probs)

print(f"  Categorical({probs})")
for i, p_i in enumerate(probs):
    empirical = (categorical_samples == i).mean()
    print(f"    P(X={i}) teorico: {p_i:.4f}, empirico: {empirical:.4f}")


# =====================================================================
#   PARTE 4: DISTRIBUCION NORMAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: LA DISTRIBUCION NORMAL ===")
print("=" * 80)

"""
X ~ N(μ, σ²)
PDF: f(x) = (1/√(2πσ²)) * exp(-(x-μ)²/(2σ²))

La distribucion MAS IMPORTANTE en ML:
- Errores de modelos (asumidos normales).
- Inicializacion de pesos.
- Regularizacion L2 = prior gaussiano.
- VAE latent space.
- GAN generadores.
"""

print("\n--- Normal properties ---")

mu, sigma = 2.0, 1.5
normal_samples = np.random.normal(mu, sigma, size=100000)

print(f"  N(μ={mu}, σ={sigma})")
print(f"    E[X] teorico: {mu:.4f}, empirico: {normal_samples.mean():.4f}")
print(f"    Std[X] teorico: {sigma:.4f}, empirico: {normal_samples.std():.4f}")

# Regla empirica (68-95-99.7)
for k, pct in [(1, 68.27), (2, 95.45), (3, 99.73)]:
    within = np.mean(np.abs(normal_samples - mu) < k * sigma)
    print(f"    Dentro de {k}σ: {within:.2%} (teorico: {pct:.2f}%)")


print("\n--- PDF implementada ---")

def normal_pdf(x, mu=0, sigma=1):
    """PDF de la normal."""
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

def normal_log_pdf(x, mu=0, sigma=1):
    """Log PDF de la normal (mas estable)."""
    return -0.5 * np.log(2 * np.pi * sigma**2) - 0.5 * ((x - mu) / sigma)**2

x_vals = np.linspace(-3, 7, 11)
print(f"\n  x      PDF(N(2,1.5))  LogPDF")
for x in x_vals:
    print(f"  {x:5.1f}  {normal_pdf(x, mu, sigma):.6f}      {normal_log_pdf(x, mu, sigma):.4f}")


print("\n--- Multivariante Normal ---")

"""
X ~ N(μ, Σ) donde μ es vector, Σ es matriz de covarianza.
PDF: f(x) = (2π)^(-d/2) |Σ|^(-1/2) exp(-0.5 (x-μ)^T Σ^{-1} (x-μ))

EN ML: distribuciones multi-dimensionales de features.
"""

mu_2d = np.array([1.0, 2.0])
cov_2d = np.array([[1.0, 0.5], [0.5, 2.0]])

samples_2d = np.random.multivariate_normal(mu_2d, cov_2d, size=10000)

print(f"  N(μ={mu_2d}, Σ=[[1, 0.5], [0.5, 2]])")
print(f"    Mean empirico: {samples_2d.mean(axis=0)}")
print(f"    Cov empirica:\n{np.cov(samples_2d.T)}")


# =====================================================================
#   PARTE 5: OTRAS DISTRIBUCIONES CONTINUAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: OTRAS DISTRIBUCIONES CONTINUAS ===")
print("=" * 80)

print("\n--- Uniforme ---")

"""
X ~ Uniform(a, b)
PDF: f(x) = 1/(b-a) para a <= x <= b
E[X] = (a+b)/2, Var(X) = (b-a)²/12
"""

a, b = 2.0, 8.0
uniform_samples = np.random.uniform(a, b, size=10000)
print(f"  Uniform({a}, {b})")
print(f"    E[X] teorico: {(a+b)/2:.4f}, empirico: {uniform_samples.mean():.4f}")
print(f"    Var: teorico: {(b-a)**2/12:.4f}, empirico: {uniform_samples.var():.4f}")


print("\n--- Exponencial ---")

"""
X ~ Exponential(λ)
PDF: f(x) = λ * e^(-λx) para x >= 0
E[X] = 1/λ, Var(X) = 1/λ²

EN ML: tiempo entre eventos, modelos de supervivencia.
"""

lam = 2.0
exp_samples = np.random.exponential(1/lam, size=10000)
print(f"  Exponential(λ={lam})")
print(f"    E[X] teorico: {1/lam:.4f}, empirico: {exp_samples.mean():.4f}")
print(f"    Var: teorico: {1/lam**2:.4f}, empirico: {exp_samples.var():.4f}")


print("\n--- Beta ---")

"""
X ~ Beta(α, β): distribucion en [0, 1].
E[X] = α/(α+β)

EN ML: prior para probabilidades. Conjugada de Bernoulli.
Bayesian A/B testing usa Beta.
"""

for alpha, beta_param in [(1, 1), (2, 5), (5, 2), (10, 10), (0.5, 0.5)]:
    samples = np.random.beta(alpha, beta_param, size=10000)
    E_teorico = alpha / (alpha + beta_param)
    print(f"  Beta(α={alpha}, β={beta_param}): "
          f"E teorico={E_teorico:.4f}, empirico={samples.mean():.4f}")


print("\n--- Gamma ---")

"""
X ~ Gamma(α, β)
E[X] = α/β

Generaliza Exponencial (Gamma(1, λ) = Exp(λ)).
Prior para parametros de precision.
"""

alpha, beta = 5.0, 2.0
gamma_samples = np.random.gamma(alpha, 1/beta, size=10000)
print(f"\n  Gamma(α={alpha}, β={beta})")
print(f"    E[X] teorico: {alpha/beta:.4f}, empirico: {gamma_samples.mean():.4f}")


# =====================================================================
#   PARTE 6: TEOREMA DEL LIMITE CENTRAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: TEOREMA DEL LIMITE CENTRAL ===")
print("=" * 80)

"""
CLT: La media de N variables iid converge a una Normal.
X̄_n ~ N(μ, σ²/n) cuando n -> ∞

Funciona para CUALQUIER distribucion con varianza finita.
Mas n -> mas normal.
"""

print("\n--- CLT con diferentes distribuciones ---")

distributions = {
    "Uniform(0,1)": lambda n: np.random.uniform(0, 1, n),
    "Exponential(1)": lambda n: np.random.exponential(1, n),
    "Bernoulli(0.3)": lambda n: (np.random.random(n) < 0.3).astype(float),
    "Poisson(3)": lambda n: np.random.poisson(3, n).astype(float),
}

for dist_name, sampler in distributions.items():
    means = []
    for _ in range(10000):
        sample = sampler(30)
        means.append(sample.mean())
    means = np.array(means)
    
    # Test de normalidad: skewness y kurtosis
    skew = np.mean(((means - means.mean()) / means.std())**3)
    kurt = np.mean(((means - means.mean()) / means.std())**4) - 3
    
    print(f"  {dist_name:18s}: skew={skew:+.3f}, excess_kurt={kurt:+.3f} "
          f"(normal: 0, 0)")


# =====================================================================
#   PARTE 7: MOMENTOS E INFORMACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: MOMENTOS ESTADISTICOS ===")
print("=" * 80)

"""
Momentos de una distribucion:
1. Media (1er momento): E[X]
2. Varianza (2do momento central): E[(X - μ)²]
3. Skewness (3er momento): E[(X - μ)³] / σ³
4. Kurtosis (4to momento): E[(X - μ)⁴] / σ⁴ - 3
"""

print("\n--- Calculando momentos ---")

def compute_moments(x):
    """Calcular los 4 momentos estadisticos."""
    n = len(x)
    mean = np.mean(x)
    var = np.var(x, ddof=1)
    std = np.sqrt(var)
    
    skewness = np.mean(((x - mean) / std)**3)
    kurtosis = np.mean(((x - mean) / std)**4) - 3
    
    return {
        'mean': mean,
        'variance': var,
        'skewness': skewness,
        'kurtosis': kurtosis,
    }

# Comparar momentos de diferentes distribuciones
dists = {
    "Normal(0,1)":     np.random.normal(0, 1, 100000),
    "Uniform(0,1)":    np.random.uniform(0, 1, 100000),
    "Exponential(1)":  np.random.exponential(1, 100000),
    "t(df=3)":         np.random.standard_t(3, 100000),
}

print(f"  {'Dist':>18s}  {'Mean':>8s}  {'Var':>8s}  {'Skew':>8s}  {'Kurt':>8s}")
for name, samples in dists.items():
    m = compute_moments(samples)
    print(f"  {name:>18s}  {m['mean']:8.4f}  {m['variance']:8.4f}  "
          f"{m['skewness']:8.4f}  {m['kurtosis']:8.4f}")


# =====================================================================
#   PARTE 8: SAMPLING Y TRANSFORMACIONES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: SAMPLING Y TRANSFORMACIONES ===")
print("=" * 80)

"""
Generar samples de distribuciones complejas:
1. Inverse transform sampling.
2. Box-Muller transform (Uniform -> Normal).
3. Reparameterization trick (VAE).
"""

print("\n--- Box-Muller transform ---")

def box_muller(n):
    """Generar N(0,1) samples desde Uniform(0,1)."""
    u1 = np.random.uniform(0, 1, n)
    u2 = np.random.uniform(0, 1, n)
    
    z1 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    z2 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
    
    return z1, z2

z1, z2 = box_muller(100000)
print(f"  Box-Muller:")
print(f"    z1: mean={z1.mean():.4f}, std={z1.std():.4f}")
print(f"    z2: mean={z2.mean():.4f}, std={z2.std():.4f}")


print("\n--- Reparameterization trick ---")

"""
VAE: z ~ N(μ, σ²)
Problema: no podemos backpropagar a traves de sampling.
Solucion: z = μ + σ * ε, donde ε ~ N(0,1)

El gradiente fluye a traves de μ y σ.
"""

mu = np.array([1.0, 2.0, -1.0])
log_var = np.array([0.5, -0.3, 0.1])
sigma = np.exp(0.5 * log_var)

# Reparameterization
epsilon = np.random.randn(1000, 3)
z = mu + sigma * epsilon

print(f"  μ = {mu}")
print(f"  σ = {sigma}")
print(f"  z mean: {z.mean(axis=0)}")
print(f"  z std:  {z.std(axis=0)}")
print(f"  Gradiente dz/dμ = 1 (identidad)")
print(f"  Gradiente dz/dσ = ε (el ruido)")


# =====================================================================
#   PARTE 9: SIMULACION MONTE CARLO
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: SIMULACION MONTE CARLO ===")
print("=" * 80)

"""
Monte Carlo: estimar cantidades usando muestras aleatorias.
E[f(X)] ≈ (1/N) Σ f(x_i)

Usos en ML: MCMC, estimacion de integrales, dropout como Bayesian.
"""

print("\n--- Estimar pi con Monte Carlo ---")

def estimate_pi(n_samples):
    x = np.random.uniform(-1, 1, n_samples)
    y = np.random.uniform(-1, 1, n_samples)
    inside_circle = (x**2 + y**2) <= 1
    return 4 * inside_circle.mean()

for n in [100, 1000, 10000, 100000, 1000000]:
    pi_est = estimate_pi(n)
    error = abs(pi_est - np.pi)
    print(f"  n={n:>8,d}: π ≈ {pi_est:.6f}, error = {error:.6f}")


print("\n--- Monte Carlo para integrales ---")

# Estimar integral de e^(-x^2) de -inf a inf = sqrt(pi)
def mc_integral(f, a, b, n):
    x = np.random.uniform(a, b, n)
    return (b - a) * np.mean(f(x))

true_value = np.sqrt(np.pi)
for n in [1000, 10000, 100000]:
    est = mc_integral(lambda x: np.exp(-x**2), -5, 5, n)
    print(f"  n={n:>6d}: ∫e^(-x²) ≈ {est:.6f} (exacto: {true_value:.6f})")


print("\n--- Bootstrap ---")

"""
Bootstrap: re-sampling con reemplazo para estimar intervalos.
No necesita asumir distribucion.
"""

np.random.seed(42)
data = np.random.exponential(2, size=50)

n_bootstrap = 10000
bootstrap_means = []
for _ in range(n_bootstrap):
    resample = np.random.choice(data, size=len(data), replace=True)
    bootstrap_means.append(resample.mean())

bootstrap_means = np.array(bootstrap_means)
ci_lower = np.percentile(bootstrap_means, 2.5)
ci_upper = np.percentile(bootstrap_means, 97.5)

print(f"\n  Datos: n={len(data)}, mean={data.mean():.4f}")
print(f"  Bootstrap 95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"  Bootstrap std: {bootstrap_means.std():.4f}")


# =====================================================================
#   PARTE 10: INDEPENDENCIA Y CORRELACION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: INDEPENDENCIA Y CORRELACION ===")
print("=" * 80)

"""
Independencia: P(A,B) = P(A)*P(B)
Correlacion: mide relacion LINEAL.

Correlacion != Causalidad.
Independencia => Correlacion = 0, pero NO al reves.
"""

print("\n--- Correlacion de Pearson ---")

np.random.seed(42)

# Datos correlacionados
n = 1000
x = np.random.randn(n)

# Lineal correlacionado
y_linear = 2*x + np.random.randn(n) * 0.5
# No lineal (cuadratico)
y_quad = x**2 + np.random.randn(n) * 0.5
# Independiente
y_indep = np.random.randn(n)

def pearson_correlation(x, y):
    """Correlacion de Pearson."""
    x_centered = x - x.mean()
    y_centered = y - y.mean()
    return np.dot(x_centered, y_centered) / (
        np.linalg.norm(x_centered) * np.linalg.norm(y_centered))

print(f"  Pearson(x, 2x+noise): {pearson_correlation(x, y_linear):.4f}")
print(f"  Pearson(x, x²+noise): {pearson_correlation(x, y_quad):.4f}  ← dependiente pero Pearson≈0!")
print(f"  Pearson(x, noise):    {pearson_correlation(x, y_indep):.4f}")


print("\n--- Matriz de correlacion ---")

data_matrix = np.column_stack([x, y_linear, y_quad, y_indep])
corr_matrix = np.corrcoef(data_matrix.T)

print(f"  Matriz de correlacion:")
labels = ["x", "2x+n", "x²+n", "noise"]
print(f"  {'':>8s} {''.join(f'{l:>8s}' for l in labels)}")
for i, row in enumerate(corr_matrix):
    print(f"  {labels[i]:>8s} {''.join(f'{v:8.4f}' for v in row)}")


# =====================================================================
#   PARTE 11: LEY DE GRANDES NUMEROS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: LEY DE GRANDES NUMEROS ===")
print("=" * 80)

"""
LLN: La media muestral converge al valor esperado cuando n -> inf.
X̄_n -> E[X] con probabilidad 1.

Diferencia con CLT:
- LLN: la media CONVERGE.
- CLT: la distribucion de la media es NORMAL.
"""

print("\n--- Convergencia de la media ---")

np.random.seed(42)
true_mean = 3.5  # E[dado] = 3.5
max_n = 10000
running_mean = np.cumsum(np.random.randint(1, 7, max_n)) / np.arange(1, max_n + 1)

for n in [10, 100, 1000, 5000, 10000]:
    print(f"  n={n:5d}: media = {running_mean[n-1]:.4f} (true: {true_mean})")


# =====================================================================
#   PARTE 12: CDF Y QUANTILE FUNCTIONS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: CDF Y QUANTILES ===")
print("=" * 80)

"""
CDF: F(x) = P(X <= x). Siempre creciente de 0 a 1.
Quantile (inversa de CDF): Q(p) = inf{x : F(x) >= p}

EN ML: percentiles, normalidad, transformaciones.
"""

print("\n--- CDF empirica ---")

def empirical_cdf(data, x):
    """CDF empirica."""
    return np.mean(data <= x)

# Normal CDF vs empirica
normal_data = np.random.normal(0, 1, 10000)

print(f"  CDF de N(0,1):")
print(f"  {'x':>6s}  {'Empirica':>10s}  {'Teorica':>10s}")
for x in [-2, -1, -0.5, 0, 0.5, 1, 2]:
    emp = empirical_cdf(normal_data, x)
    # Teorica: Φ(x)
    teorica = 0.5 * (1 + np.math.erf(x / np.sqrt(2)))
    print(f"  {x:6.1f}  {emp:10.4f}  {teorica:10.4f}")


print("\n--- Quantiles ---")

quantiles = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
print(f"  Quantiles de N(0,1):")
for q in quantiles:
    val = np.percentile(normal_data, q * 100)
    print(f"    Q({q:.2f}) = {val:+.4f}")


# =====================================================================
#   PARTE 13: INVERSE CDF SAMPLING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: INVERSE CDF SAMPLING ===")
print("=" * 80)

"""
Si conocemos la CDF inversa F^{-1}, podemos generar samples:
X = F^{-1}(U), donde U ~ Uniform(0,1)

Ejemplo: Exponencial. CDF: F(x) = 1 - e^{-λx}
Inversa: F^{-1}(u) = -ln(1-u)/λ
"""

print("\n--- Inverse CDF para Exponencial ---")

def sample_exponential_icdf(lam, n):
    """Sampling via inverse CDF."""
    u = np.random.uniform(0, 1, n)
    return -np.log(1 - u) / lam

lam = 2.0
samples_icdf = sample_exponential_icdf(lam, 100000)
samples_numpy = np.random.exponential(1/lam, 100000)

print(f"  Exponential(λ={lam}):")
print(f"    ICDF:  mean={samples_icdf.mean():.4f}, std={samples_icdf.std():.4f}")
print(f"    NumPy: mean={samples_numpy.mean():.4f}, std={samples_numpy.std():.4f}")


print("\n--- Inverse CDF para Pareto ---")

"""
Pareto: P(X > x) = (x_m/x)^α para x >= x_m
CDF: F(x) = 1 - (x_m/x)^α
Inversa: F^{-1}(u) = x_m / (1-u)^{1/α}
"""

def sample_pareto_icdf(x_m, alpha, n):
    u = np.random.uniform(0, 1, n)
    return x_m / (1 - u)**(1/alpha)

pareto_samples = sample_pareto_icdf(1, 2, 100000)
print(f"  Pareto(x_m=1, α=2):")
print(f"    Mean: {pareto_samples.mean():.4f} (teorico: {2/(2-1):.4f})")
print(f"    Mediana: {np.median(pareto_samples):.4f} (teorico: {2**(1/2):.4f})")


# =====================================================================
#   PARTE 14: MIXTURE MODELS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: MIXTURE MODELS ===")
print("=" * 80)

"""
Gaussian Mixture Model (GMM):
P(x) = Σ π_k * N(x | μ_k, σ_k²)

EN ML: clustering probabilistico, generacion de datos,
density estimation.
"""

print("\n--- GMM sampling ---")

def sample_gmm(weights, means, stds, n):
    """Muestrear de un GMM."""
    k = len(weights)
    components = np.random.choice(k, size=n, p=weights)
    samples = np.array([np.random.normal(means[c], stds[c]) for c in components])
    return samples, components

weights = [0.3, 0.5, 0.2]
means = [-2.0, 1.0, 5.0]
stds = [0.5, 1.0, 0.3]

samples_gmm, components = sample_gmm(weights, means, stds, 10000)

print(f"  GMM con 3 componentes:")
print(f"    Pesos: {weights}")
print(f"    Medias: {means}")
print(f"    Overall mean: {samples_gmm.mean():.4f}")
print(f"    Overall std: {samples_gmm.std():.4f}")

# Verificar proporciones
for k in range(3):
    prop = (components == k).mean()
    print(f"    Componente {k}: {prop:.4f} (esperado: {weights[k]})")


print("\n--- EM simplificado para GMM 1D ---")

def em_gmm_1d(data, k=2, max_iter=50):
    """EM para GMM en 1D."""
    n = len(data)
    np.random.seed(42)
    
    # Inicializar
    mu = np.random.choice(data, k)
    sigma = np.ones(k)
    pi = np.ones(k) / k
    
    for iteration in range(max_iter):
        # E-step: calcular responsabilidades
        resp = np.zeros((n, k))
        for j in range(k):
            resp[:, j] = pi[j] * normal_pdf(data, mu[j], sigma[j])
        resp /= resp.sum(axis=1, keepdims=True)
        
        # M-step
        for j in range(k):
            N_j = resp[:, j].sum()
            mu[j] = np.sum(resp[:, j] * data) / N_j
            sigma[j] = np.sqrt(np.sum(resp[:, j] * (data - mu[j])**2) / N_j)
            pi[j] = N_j / n
    
    return mu, sigma, pi

# Datos bimodales
data_bimodal = np.concatenate([
    np.random.normal(-2, 0.5, 300),
    np.random.normal(3, 1.0, 700)
])

mu_em, sigma_em, pi_em = em_gmm_1d(data_bimodal, k=2)
print(f"\n  EM para GMM bimodal:")
for j in range(2):
    print(f"    Comp {j}: μ={mu_em[j]:.4f}, σ={sigma_em[j]:.4f}, π={pi_em[j]:.4f}")


# =====================================================================
#   PARTE 15: CADENAS DE MARKOV
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: CADENAS DE MARKOV ===")
print("=" * 80)

"""
Cadena de Markov: proximo estado depende SOLO del actual.
P(X_{t+1} | X_1, ..., X_t) = P(X_{t+1} | X_t)

Matriz de transicion T: T[i,j] = P(X_{t+1}=j | X_t=i)
Distribucion estacionaria: π = π @ T
"""

print("\n--- Markov chain simple ---")

# Clima: Sunny=0, Rainy=1
T = np.array([
    [0.8, 0.2],  # Sunny -> Sunny/Rainy
    [0.4, 0.6],  # Rainy -> Sunny/Rainy
])

def simulate_markov(T, state0, n_steps):
    states = [state0]
    for _ in range(n_steps):
        probs = T[states[-1]]
        next_state = np.random.choice(len(probs), p=probs)
        states.append(next_state)
    return states

np.random.seed(42)
states = simulate_markov(T, 0, 10000)
state_names = ["Sunny", "Rainy"]

empirical_dist = [states.count(i)/len(states) for i in range(2)]

# Distribucion estacionaria analitica
eigenvals, eigenvecs = np.linalg.eig(T.T)
stat_dist = eigenvecs[:, np.argmin(np.abs(eigenvals - 1))]
stat_dist = np.real(stat_dist / stat_dist.sum())

print(f"  Transition matrix:")
print(f"  {T}")
print(f"  Distribucion empirica (10K pasos):")
for i, name in enumerate(state_names):
    print(f"    {name}: {empirical_dist[i]:.4f} (estacionaria: {stat_dist[i]:.4f})")


# =====================================================================
#   PARTE 16: REJECTION SAMPLING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: REJECTION SAMPLING ===")
print("=" * 80)

"""
Rejection sampling: muestrear de p(x) usando una distribucion
de propuesta q(x) tal que M*q(x) >= p(x).

1. Muestrear x ~ q(x), u ~ Uniform(0, M*q(x)).
2. Aceptar si u <= p(x).
"""

print("\n--- Rejection sampling ---")

def rejection_sampling(target_pdf, proposal_sampler, proposal_pdf, M, n_samples):
    """Rejection sampling."""
    samples = []
    total_proposals = 0
    
    while len(samples) < n_samples:
        x = proposal_sampler()
        u = np.random.uniform(0, M * proposal_pdf(x))
        total_proposals += 1
        
        if u <= target_pdf(x):
            samples.append(x)
    
    acceptance_rate = n_samples / total_proposals
    return np.array(samples), acceptance_rate

# Target: Beta(5, 2)
# Proposal: Uniform(0, 1)
def beta_pdf(x, a=5, b=2):
    if 0 < x < 1:
        return x**(a-1) * (1-x)**(b-1) * 30  # ~ Beta(5,2) sin normalizar es ok
    return 0

samples_rej, rate = rejection_sampling(
    target_pdf=lambda x: beta_pdf(x),
    proposal_sampler=lambda: np.random.uniform(0, 1),
    proposal_pdf=lambda x: 1.0,
    M=30,
    n_samples=5000
)

print(f"  Target: ~Beta(5,2)")
print(f"  Acceptance rate: {rate:.4f}")
print(f"  Mean: {samples_rej.mean():.4f} (Beta(5,2) mean: {5/7:.4f})")


print("\n" + "=" * 80)
print("=== CAPITULO 17: LOG-SUM-EXP TRICK ===")
print("=" * 80)

"""
Problema: computar log(Σ exp(x_i)) causa overflow.
Solucion: log(Σ exp(x_i)) = max(x) + log(Σ exp(x_i - max(x)))

Usado en: softmax, log-likelihood de mixtures.
"""

print("\n--- Log-Sum-Exp ---")

def log_sum_exp(x):
    """Numerically stable log-sum-exp."""
    x_max = np.max(x)
    return x_max + np.log(np.sum(np.exp(x - x_max)))

# Sin estabilidad (overflow)
big_values = np.array([1000, 1001, 1002])
try:
    naive = np.log(np.sum(np.exp(big_values)))
    print(f"  Naive: {naive}")
except:
    print(f"  Naive: OVERFLOW")

stable = log_sum_exp(big_values)
print(f"  Stable: {stable:.4f}")

# Verificar con valores normales
small_values = np.array([1.0, 2.0, 3.0])
print(f"  Naive:  {np.log(np.sum(np.exp(small_values))):.6f}")
print(f"  Stable: {log_sum_exp(small_values):.6f}")



print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE PROBABILIDAD Y DISTRIBUCIONES:

1. Axiomas: P(A)>=0, P(Ω)=1, union disjunta.

2. Bayes: posterior ∝ likelihood × prior.

3. Bernoulli/Binomial/Poisson: discretas fundamentales.

4. Normal: la reina. Pesos, errores, latent spaces.

5. Beta/Gamma/Pareto: priors y distribuciones de cola.

6. CLT + LLN: convergencia de medias.

7. CDF, quantiles, inverse CDF sampling.

8. Reparameterization trick: backprop + sampling.

9. GMM + EM: clustering probabilistico.

10. Cadenas de Markov: estados, transiciones, estacionaria.

Siguiente archivo: Estadistica inferencial.
"""

print("\n FIN DE ARCHIVO 01_probabilidad_y_distribuciones.")
print(" Probabilidad y distribuciones han sido dominadas.")
