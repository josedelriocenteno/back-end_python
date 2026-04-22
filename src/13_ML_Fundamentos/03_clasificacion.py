# ===========================================================================
# 03_clasificacion.py
# ===========================================================================
# MODULO 13: ML FUNDAMENTOS
# ARCHIVO 03: Clasificacion (Logistic, Decision Trees, KNN, SVM)
# ===========================================================================
#
# OBJETIVO (1000+ LINEAS):
# Implementar clasificadores desde cero y entender metricas.
#
# CONTENIDO:
#   1. Logistic Regression.
#   2. Sigmoid y softmax.
#   3. Decision Trees (ID3/CART).
#   4. KNN.
#   5. Naive Bayes.
#   6. SVM conceptual.
#   7. Metricas: confusion matrix, ROC, PR.
#   8. Multiclass strategies.
#   9. Threshold tuning.
#   10. Pipeline clasificacion.
#
# NIVEL: ARQUITECTO ML / DATA ENGINEER SENIOR.
# ===========================================================================

import numpy as np
import time
from collections import Counter


# =====================================================================
#   PARTE 1: LOGISTIC REGRESSION
# =====================================================================

print("\n" + "=" * 80)
print("=== CAPITULO 1: LOGISTIC REGRESSION ===")
print("=" * 80)

"""
Logistic Regression: clasificacion binaria.
  P(y=1|x) = sigmoid(w^T x) = 1 / (1 + exp(-w^T x))

Loss: Binary Cross-Entropy
  L = -[y*log(p) + (1-y)*log(1-p)]
"""

def sigmoid(z):
    """Sigmoid function (numerically stable)."""
    return np.where(z >= 0,
                    1 / (1 + np.exp(-z)),
                    np.exp(z) / (1 + np.exp(z)))


class LogisticRegression:
    """Logistic Regression from scratch."""
    
    def __init__(self, lr=0.01, epochs=1000, reg=0.0):
        self.lr = lr
        self.epochs = epochs
        self.reg = reg
        self.weights = None
        self.loss_history = []
    
    def fit(self, X, y):
        n, d = X.shape
        self.weights = np.zeros(d)
        
        for epoch in range(self.epochs):
            z = X @ self.weights
            p = sigmoid(z)
            
            # Gradient
            gradient = (1/n) * X.T @ (p - y)
            gradient[1:] += (self.reg / n) * self.weights[1:]  # L2
            
            self.weights -= self.lr * gradient
            
            # Loss
            eps = 1e-15
            p_clipped = np.clip(p, eps, 1 - eps)
            loss = -np.mean(y * np.log(p_clipped) + (1-y) * np.log(1-p_clipped))
            
            if epoch % 200 == 0:
                self.loss_history.append((epoch, loss))
        
        return self
    
    def predict_proba(self, X):
        return sigmoid(X @ self.weights)
    
    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)


print("\n--- Datos sinteticos ---")

np.random.seed(42)
n = 300

# Clase 0: cluster around (-1, -1)
X0 = np.random.randn(n//2, 2) * 0.8 + np.array([-1, -1])
# Clase 1: cluster around (1, 1)
X1 = np.random.randn(n//2, 2) * 0.8 + np.array([1, 1])

X_cls = np.vstack([X0, X1])
y_cls = np.array([0] * (n//2) + [1] * (n//2))

# Shuffle
idx = np.random.permutation(n)
X_cls = X_cls[idx]
y_cls = y_cls[idx]

# Add bias
X_cls_b = np.column_stack([np.ones(n), X_cls])

# Split
split = int(n * 0.8)
X_train, X_test = X_cls_b[:split], X_cls_b[split:]
y_train, y_test = y_cls[:split], y_cls[split:]

print(f"  Train: {X_train.shape}, Test: {X_test.shape}")
print(f"  Class balance: {np.mean(y_cls):.2f}")


print("\n--- Fit ---")

lr = LogisticRegression(lr=0.1, epochs=1000, reg=0.01)
lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)
accuracy = np.mean(y_pred_lr == y_test)
print(f"  Weights: {lr.weights.round(4)}")
print(f"  Accuracy: {accuracy:.4f}")

for epoch, loss in lr.loss_history:
    print(f"    Epoch {epoch:4d}: loss={loss:.4f}")


# =====================================================================
#   PARTE 2: DECISION TREE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 2: DECISION TREE ===")
print("=" * 80)

"""
Decision Tree: particionar espacio recursivamente.
Criterio de split:
  - Gini impurity: 1 - sum(p_i^2)
  - Entropy: -sum(p_i * log(p_i))
  - Information Gain: entropy(parent) - weighted_avg(entropy(children))
"""

def gini_impurity(y):
    """Gini impurity."""
    if len(y) == 0:
        return 0
    counts = np.bincount(y)
    probs = counts / len(y)
    return 1 - np.sum(probs ** 2)

def entropy(y):
    """Shannon entropy."""
    if len(y) == 0:
        return 0
    counts = np.bincount(y)
    probs = counts[counts > 0] / len(y)
    return -np.sum(probs * np.log2(probs))


class DecisionTreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # Leaf prediction


class DecisionTreeClassifier:
    """CART Decision Tree from scratch."""
    
    def __init__(self, max_depth=5, min_samples=2, criterion='gini'):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.criterion = gini_impurity if criterion == 'gini' else entropy
        self.root = None
    
    def _best_split(self, X, y):
        best_gain = -1
        best_feature = None
        best_threshold = None
        
        parent_impurity = self.criterion(y)
        n = len(y)
        
        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask
                
                if left_mask.sum() < self.min_samples or right_mask.sum() < self.min_samples:
                    continue
                
                left_imp = self.criterion(y[left_mask])
                right_imp = self.criterion(y[right_mask])
                
                weighted = (left_mask.sum() * left_imp + right_mask.sum() * right_imp) / n
                gain = parent_impurity - weighted
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        
        return best_feature, best_threshold, best_gain
    
    def _build_tree(self, X, y, depth=0):
        # Stopping conditions
        if depth >= self.max_depth or len(np.unique(y)) == 1 or len(y) < self.min_samples:
            return DecisionTreeNode(value=Counter(y).most_common(1)[0][0])
        
        feature, threshold, gain = self._best_split(X, y)
        
        if feature is None or gain <= 0:
            return DecisionTreeNode(value=Counter(y).most_common(1)[0][0])
        
        left_mask = X[:, feature] <= threshold
        left = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right = self._build_tree(X[~left_mask], y[~left_mask], depth + 1)
        
        return DecisionTreeNode(feature=feature, threshold=threshold, left=left, right=right)
    
    def fit(self, X, y):
        self.root = self._build_tree(X, y)
        return self
    
    def _predict_one(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)
    
    def predict(self, X):
        return np.array([self._predict_one(x, self.root) for x in X])

print("\n--- Decision Tree fit ---")

dt = DecisionTreeClassifier(max_depth=4, min_samples=5)
dt.fit(X_cls, y_cls)

y_pred_dt = dt.predict(X_cls)
acc_dt = np.mean(y_pred_dt == y_cls)
print(f"  Tree accuracy (train): {acc_dt:.4f}")


# =====================================================================
#   PARTE 3: KNN
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 3: KNN ===")
print("=" * 80)

"""
K-Nearest Neighbors:
  - Lazy learner (no training).
  - Predict: find K nearest neighbors, vote.
  - Distance: euclidean, manhattan, cosine.
"""

class KNNClassifier:
    """KNN from scratch."""
    
    def __init__(self, k=5):
        self.k = k
        self.X_train = None
        self.y_train = None
    
    def fit(self, X, y):
        self.X_train = X.copy()
        self.y_train = y.copy()
        return self
    
    def _predict_one(self, x):
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        k_idx = np.argsort(distances)[:self.k]
        k_labels = self.y_train[k_idx]
        return Counter(k_labels).most_common(1)[0][0]
    
    def predict(self, X):
        return np.array([self._predict_one(x) for x in X])

print("\n--- KNN con diferentes K ---")

# Scale features
X_scaled = (X_cls - X_cls.mean(0)) / X_cls.std(0)
X_tr_s, X_te_s = X_scaled[:split], X_scaled[split:]

for k in [1, 3, 5, 7, 11, 21]:
    knn = KNNClassifier(k=k).fit(X_tr_s, y_train)
    y_pred_knn = knn.predict(X_te_s)
    acc = np.mean(y_pred_knn == y_test)
    print(f"  K={k:2d}: accuracy={acc:.4f}")


# =====================================================================
#   PARTE 4: NAIVE BAYES
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 4: NAIVE BAYES ===")
print("=" * 80)

"""
Naive Bayes: P(y|x) ~ P(y) * prod(P(xi|y))
Asume features independientes (naive assumption).
"""

class GaussianNB:
    """Gaussian Naive Bayes from scratch."""
    
    def __init__(self):
        self.classes = None
        self.priors = {}
        self.means = {}
        self.vars = {}
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        for c in self.classes:
            X_c = X[y == c]
            self.priors[c] = len(X_c) / len(X)
            self.means[c] = X_c.mean(axis=0)
            self.vars[c] = X_c.var(axis=0) + 1e-9
        return self
    
    def _log_likelihood(self, x, c):
        mean = self.means[c]
        var = self.vars[c]
        log_prob = -0.5 * np.sum(np.log(2 * np.pi * var))
        log_prob -= 0.5 * np.sum((x - mean) ** 2 / var)
        return log_prob + np.log(self.priors[c])
    
    def predict(self, X):
        predictions = []
        for x in X:
            posteriors = {c: self._log_likelihood(x, c) for c in self.classes}
            predictions.append(max(posteriors, key=posteriors.get))
        return np.array(predictions)

print("\n--- Gaussian NB ---")

nb = GaussianNB().fit(X_cls[:split], y_train)
y_pred_nb = nb.predict(X_cls[split:])
acc_nb = np.mean(y_pred_nb == y_test)
print(f"  NB accuracy: {acc_nb:.4f}")


# =====================================================================
#   PARTE 5: METRICAS AVANZADAS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 5: METRICAS AVANZADAS ===")
print("=" * 80)

def full_metrics(y_true, y_pred, y_proba=None):
    """All classification metrics."""
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    acc = (tp + tn) / (tp + tn + fp + fn)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    
    result = {'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1': f1}
    
    # AUC if probabilities available
    if y_proba is not None:
        thresholds = np.sort(np.unique(y_proba))[::-1]
        tprs, fprs = [0], [0]
        for t in thresholds:
            y_t = (y_proba >= t).astype(int)
            tp_t = np.sum((y_true == 1) & (y_t == 1))
            fp_t = np.sum((y_true == 0) & (y_t == 1))
            tpr = tp_t / max(np.sum(y_true == 1), 1)
            fpr = fp_t / max(np.sum(y_true == 0), 1)
            tprs.append(tpr)
            fprs.append(fpr)
        tprs.append(1)
        fprs.append(1)
        auc = np.trapz(tprs, fprs)
        result['AUC'] = abs(auc)
    
    return result

print("\n--- Model comparison ---")

# Compare all models
y_proba_lr = lr.predict_proba(X_test)

models = {
    'Logistic': (y_pred_lr, y_proba_lr),
    'NaiveBayes': (y_pred_nb, None),
}

for name, (y_p, y_prob) in models.items():
    m = full_metrics(y_test, y_p, y_prob)
    line = f"  {name:12s}:"
    for k, v in m.items():
        line += f" {k}={v:.3f}"
    print(line)


# =====================================================================
#   PARTE 6: THRESHOLD TUNING
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 6: THRESHOLD TUNING ===")
print("=" * 80)

print("\n--- Optimal threshold ---")

best_f1 = 0
best_thresh = 0.5

for t in np.arange(0.1, 0.9, 0.05):
    y_t = (y_proba_lr >= t).astype(int)
    m = full_metrics(y_test, y_t)
    if m['F1'] > best_f1:
        best_f1 = m['F1']
        best_thresh = t
    print(f"  t={t:.2f}: P={m['Precision']:.3f} R={m['Recall']:.3f} F1={m['F1']:.3f}")

print(f"\n  Best threshold: {best_thresh:.2f} (F1={best_f1:.3f})")


# =====================================================================
#   PARTE 7: SOFTMAX (MULTICLASS)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 7: SOFTMAX ===")
print("=" * 80)

"""
Softmax: extension de sigmoid a K clases.
  P(y=k|x) = exp(z_k) / sum(exp(z_j))

Loss: Categorical Cross-Entropy
  L = -sum(y_k * log(p_k))
"""

def softmax(Z):
    """Softmax (numerically stable)."""
    Z_shifted = Z - Z.max(axis=1, keepdims=True)
    exp_Z = np.exp(Z_shifted)
    return exp_Z / exp_Z.sum(axis=1, keepdims=True)


class SoftmaxClassifier:
    """Multiclass logistic regression."""
    
    def __init__(self, lr=0.01, epochs=500, reg=0.01):
        self.lr = lr
        self.epochs = epochs
        self.reg = reg
        self.weights = None
        self.classes = None
    
    def fit(self, X, y):
        self.classes = np.unique(y)
        n, d = X.shape
        k = len(self.classes)
        self.weights = np.zeros((d, k))
        
        # One-hot encode
        Y_onehot = np.zeros((n, k))
        for i, c in enumerate(self.classes):
            Y_onehot[y == c, i] = 1
        
        for epoch in range(self.epochs):
            Z = X @ self.weights
            P = softmax(Z)
            
            grad = (1/n) * X.T @ (P - Y_onehot)
            grad += (self.reg / n) * self.weights
            self.weights -= self.lr * grad
        
        return self
    
    def predict(self, X):
        Z = X @ self.weights
        P = softmax(Z)
        return self.classes[np.argmax(P, axis=1)]

print("\n--- Multiclass data ---")

np.random.seed(42)
n_mc = 300
X_mc = np.vstack([
    np.random.randn(100, 2) * 0.5 + [0, 2],
    np.random.randn(100, 2) * 0.5 + [2, -1],
    np.random.randn(100, 2) * 0.5 + [-2, -1],
])
y_mc = np.array([0]*100 + [1]*100 + [2]*100)
X_mc_b = np.column_stack([np.ones(n_mc), X_mc])

sm = SoftmaxClassifier(lr=0.1, epochs=500).fit(X_mc_b, y_mc)
y_pred_sm = sm.predict(X_mc_b)
acc_sm = np.mean(y_pred_sm == y_mc)
print(f"  Softmax accuracy: {acc_sm:.4f}")
print(f"  Per-class: {[np.mean(y_pred_sm[y_mc==c]==c) for c in [0,1,2]]}")


# =====================================================================
#   PARTE 8: ONE-VS-REST
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 8: ONE-VS-REST ===")
print("=" * 80)

"""
OvR: entrenar K clasificadores binarios.
Cada uno: clase k vs resto.
Prediccion: clase con mayor probabilidad.
"""

def one_vs_rest(X_train, y_train, X_test, classes):
    """One-vs-Rest multiclass classification."""
    scores = np.zeros((len(X_test), len(classes)))
    
    for i, c in enumerate(classes):
        y_binary = (y_train == c).astype(int)
        model = LogisticRegression(lr=0.1, epochs=500, reg=0.01)
        model.fit(X_train, y_binary)
        scores[:, i] = model.predict_proba(X_test)
    
    return classes[np.argmax(scores, axis=1)]

split_mc = 240
y_pred_ovr = one_vs_rest(X_mc_b[:split_mc], y_mc[:split_mc],
                          X_mc_b[split_mc:], np.array([0, 1, 2]))
acc_ovr = np.mean(y_pred_ovr == y_mc[split_mc:])
print(f"  OvR accuracy: {acc_ovr:.4f}")


# =====================================================================
#   PARTE 9: SVM CONCEPTUAL
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 9: SVM ===")
print("=" * 80)

"""
SVM (Support Vector Machine):
  Encontrar hiperplano con MAXIMO margen.

  max margin = 2 / ||w||
  
  Loss: Hinge Loss = max(0, 1 - y*f(x))
  
  Kernel trick:
  - Linear: K(x,z) = x^T z
  - Polynomial: K(x,z) = (x^T z + c)^d
  - RBF/Gaussian: K(x,z) = exp(-gamma * ||x-z||^2)
"""

class LinearSVM:
    """Linear SVM via subgradient descent."""
    
    def __init__(self, lr=0.001, epochs=1000, C=1.0):
        self.lr = lr
        self.epochs = epochs
        self.C = C
        self.weights = None
    
    def fit(self, X, y):
        n, d = X.shape
        # Convert to {-1, 1}
        y_svm = np.where(y == 0, -1, 1)
        self.weights = np.zeros(d)
        
        for _ in range(self.epochs):
            for i in range(n):
                if y_svm[i] * (X[i] @ self.weights) < 1:
                    self.weights -= self.lr * (self.weights - self.C * y_svm[i] * X[i])
                else:
                    self.weights -= self.lr * self.weights
        return self
    
    def predict(self, X):
        return (X @ self.weights >= 0).astype(int)

svm = LinearSVM(lr=0.001, epochs=200, C=1.0).fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
acc_svm = np.mean(y_pred_svm == y_test)
print(f"  Linear SVM accuracy: {acc_svm:.4f}")


# =====================================================================
#   PARTE 10: CLASS IMBALANCE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 10: CLASS IMBALANCE ===")
print("=" * 80)

"""
Tecnicas:
1. Oversampling (SMOTE): duplicar/sintetizar minoria.
2. Undersampling: reducir mayoria.
3. Class weights: penalizar mas errores en minoria.
4. Threshold adjustment.
5. Metricas: F1, AUC > Accuracy.
"""

print("\n--- Class weights ---")

def weighted_logistic(X, y, lr=0.01, epochs=500, class_weights=None):
    """Logistic with class weights."""
    n, d = X.shape
    w = np.zeros(d)
    
    if class_weights is None:
        weights = np.ones(n)
    else:
        weights = np.array([class_weights[int(yi)] for yi in y])
    
    for _ in range(epochs):
        p = sigmoid(X @ w)
        grad = (1/n) * X.T @ ((p - y) * weights)
        w -= lr * grad
    
    return w

# Imbalanced data
np.random.seed(42)
X_imb = np.column_stack([np.ones(110), np.random.randn(110, 2)])
y_imb = np.array([0]*100 + [1]*10)
idx_imb = np.random.permutation(110)
X_imb, y_imb = X_imb[idx_imb], y_imb[idx_imb]

# Without weights
w_no_wt = weighted_logistic(X_imb, y_imb, lr=0.1)
p_no_wt = sigmoid(X_imb @ w_no_wt)
y_no_wt = (p_no_wt >= 0.5).astype(int)
print(f"  No weights: predict_1={y_no_wt.sum()}, recall_1={np.sum((y_imb==1)&(y_no_wt==1))/max(np.sum(y_imb==1),1):.2f}")

# With weights
w_wt = weighted_logistic(X_imb, y_imb, lr=0.1, class_weights={0: 1, 1: 10})
p_wt = sigmoid(X_imb @ w_wt)
y_wt = (p_wt >= 0.5).astype(int)
print(f"  Weighted:   predict_1={y_wt.sum()}, recall_1={np.sum((y_imb==1)&(y_wt==1))/max(np.sum(y_imb==1),1):.2f}")


# =====================================================================
#   PARTE 11: PERCEPTRON
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 11: PERCEPTRON ===")
print("=" * 80)

"""
Perceptron: el clasificador lineal mas simple.
  if w^T x > 0: predict 1
  else: predict 0
  
  Update rule: if misclassified, w += y * x
"""

class Perceptron:
    def __init__(self, lr=0.01, epochs=100):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
    
    def fit(self, X, y):
        n, d = X.shape
        self.weights = np.zeros(d)
        y_signed = np.where(y == 0, -1, 1)
        
        for _ in range(self.epochs):
            errors = 0
            for i in range(n):
                if y_signed[i] * (X[i] @ self.weights) <= 0:
                    self.weights += self.lr * y_signed[i] * X[i]
                    errors += 1
            if errors == 0:
                break
        return self
    
    def predict(self, X):
        return (X @ self.weights >= 0).astype(int)

perc = Perceptron(lr=0.01, epochs=100).fit(X_train, y_train)
y_pred_perc = perc.predict(X_test)
acc_perc = np.mean(y_pred_perc == y_test)
print(f"  Perceptron accuracy: {acc_perc:.4f}")


# =====================================================================
#   PARTE 12: ROC CURVE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 12: ROC CURVE ===")
print("=" * 80)

def compute_roc(y_true, y_proba, n_thresholds=50):
    """Compute ROC curve points."""
    thresholds = np.linspace(0, 1, n_thresholds)
    tprs = []
    fprs = []
    
    for t in thresholds:
        y_pred = (y_proba >= t).astype(int)
        tp = np.sum((y_true == 1) & (y_pred == 1))
        fp = np.sum((y_true == 0) & (y_pred == 1))
        fn = np.sum((y_true == 1) & (y_pred == 0))
        tn = np.sum((y_true == 0) & (y_pred == 0))
        
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        tprs.append(tpr)
        fprs.append(fpr)
    
    auc = -np.trapz(tprs, fprs)
    return fprs, tprs, auc

fprs, tprs, auc = compute_roc(y_test, y_proba_lr)
print(f"  AUC: {auc:.4f}")
print(f"  ROC points: {len(fprs)}")


# =====================================================================
#   PARTE 13: CALIBRATION
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 13: CALIBRATION ===")
print("=" * 80)

"""
Calibracion: que P(y=1|p=0.8) sea realmente ~80%.

Metodos:
1. Platt scaling: sigmoid post-hoc.
2. Isotonic regression.
3. Reliability diagram (calibration curve).

Brier score: mean((p - y)^2). Menor = mejor calibrado.
"""

brier = np.mean((y_proba_lr - y_test) ** 2)
print(f"  Brier score: {brier:.4f} (lower is better)")

# Reliability diagram
n_bins_cal = 5
bin_edges = np.linspace(0, 1, n_bins_cal + 1)
print(f"\n  Calibration table:")
print(f"  {'Bin':>12s} {'Mean Pred':>10s} {'Mean True':>10s} {'Count':>6s}")
for i in range(n_bins_cal):
    mask = (y_proba_lr >= bin_edges[i]) & (y_proba_lr < bin_edges[i+1])
    if mask.sum() > 0:
        mean_pred = y_proba_lr[mask].mean()
        mean_true = y_test[mask].mean()
        print(f"  [{bin_edges[i]:.1f},{bin_edges[i+1]:.1f}) {mean_pred:10.3f} {mean_true:10.3f} {mask.sum():6d}")


# =====================================================================
#   PARTE 14: CONFUSION MATRIX DISPLAY
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 14: CONFUSION MATRIX ===")
print("=" * 80)

def print_confusion_matrix(y_true, y_pred, labels=None):
    """Pretty print confusion matrix."""
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    
    n = len(labels)
    matrix = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        i = labels.index(t)
        j = labels.index(p)
        matrix[i, j] += 1
    
    # Header
    header = "True\\Pred"
    for l in labels:
        header += f"  {l:>6}"
    print(f"  {header}")
    print(f"  {'─' * len(header)}")
    
    for i, l in enumerate(labels):
        row = f"  {l:>9}"
        for j in range(n):
            row += f"  {matrix[i,j]:>6}"
        print(row)
    
    return matrix

print("\n--- Binary confusion ---")
cm = print_confusion_matrix(y_test.tolist(), y_pred_lr.tolist(), [0, 1])

print("\n--- Multiclass confusion ---")
cm_mc = print_confusion_matrix(y_mc[:60].tolist(), y_pred_sm[:60].tolist(), [0, 1, 2])


# =====================================================================
#   PARTE 15: CLASSIFICATION PIPELINE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 15: CLASSIFICATION PIPELINE ===")
print("=" * 80)

def classification_pipeline(X, y, test_frac=0.2):
    """Complete classification pipeline."""
    n = len(y)
    idx = np.random.permutation(n)
    split = int(n * (1 - test_frac))
    
    X_train, X_test = X[idx[:split]], X[idx[split:]]
    y_train, y_test = y[idx[:split]], y[idx[split:]]
    
    # Scale
    mean = X_train.mean(0)
    std = X_train.std(0)
    std[std == 0] = 1
    X_train_s = (X_train - mean) / std
    X_test_s = (X_test - mean) / std
    
    # Add bias
    X_tr = np.column_stack([np.ones(len(X_train_s)), X_train_s])
    X_te = np.column_stack([np.ones(len(X_test_s)), X_test_s])
    
    results = {}
    
    # Logistic
    lg = LogisticRegression(lr=0.1, epochs=500, reg=0.01).fit(X_tr, y_train)
    results['Logistic'] = np.mean(lg.predict(X_te) == y_test)
    
    # KNN
    knn = KNNClassifier(k=5).fit(X_train_s, y_train)
    results['KNN(5)'] = np.mean(knn.predict(X_test_s) == y_test)
    
    # NB
    nb = GaussianNB().fit(X_train_s, y_train)
    results['NaiveBayes'] = np.mean(nb.predict(X_test_s) == y_test)
    
    return results

np.random.seed(42)
pipe_results = classification_pipeline(X_cls, y_cls)
print(f"  Pipeline results:")
for model, acc in sorted(pipe_results.items(), key=lambda x: -x[1]):
    print(f"    {model:>12s}: {acc:.4f}")


# =====================================================================
#   PARTE 16: MULTICLASS METRICS
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 16: MULTICLASS METRICS ===")
print("=" * 80)

"""
Multiclass metrics:
  - Macro: promedio de per-class metrics (trata todas iguales).
  - Micro: computa globalmente (favorece clases grandes).
  - Weighted: macro ponderado por support.
"""

def multiclass_metrics(y_true, y_pred, average='macro'):
    """Per-class and averaged metrics."""
    classes = sorted(set(y_true) | set(y_pred))
    per_class = {}
    
    for c in classes:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == c and p == c)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != c and p == c)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == c and p != c)
        
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        support = sum(1 for t in y_true if t == c)
        
        per_class[c] = {'P': prec, 'R': rec, 'F1': f1, 'Support': support}
    
    # Macro average
    n_classes = len(classes)
    macro_p = sum(m['P'] for m in per_class.values()) / n_classes
    macro_r = sum(m['R'] for m in per_class.values()) / n_classes
    macro_f1 = sum(m['F1'] for m in per_class.values()) / n_classes
    
    return per_class, {'Macro_P': macro_p, 'Macro_R': macro_r, 'Macro_F1': macro_f1}

per_class, macro = multiclass_metrics(y_mc.tolist(), y_pred_sm.tolist())

print(f"\n  Per-class report:")
print(f"  {'Class':>6s} {'Prec':>6s} {'Recall':>7s} {'F1':>6s} {'Support':>8s}")
for c, m in per_class.items():
    print(f"  {c:6d} {m['P']:6.3f} {m['R']:7.3f} {m['F1']:6.3f} {m['Support']:8d}")
print(f"\n  Macro: P={macro['Macro_P']:.3f} R={macro['Macro_R']:.3f} F1={macro['Macro_F1']:.3f}")


# =====================================================================
#   PARTE 17: FEATURE IMPORTANCE (TREE)
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 17: FEATURE IMPORTANCE ===")
print("=" * 80)

"""
Feature importance en decision trees:
  Suma de impurity decrease ponderada por n_samples en cada split.
"""

def tree_feature_importance(node, n_total, importances, depth=0):
    """Compute feature importance recursively."""
    if node.value is not None:
        return
    if node.feature is not None and node.feature < len(importances):
        importances[node.feature] += 1.0 / (depth + 1)
    if node.left:
        tree_feature_importance(node.left, n_total, importances, depth + 1)
    if node.right:
        tree_feature_importance(node.right, n_total, importances, depth + 1)

importances = np.zeros(X_cls.shape[1])
tree_feature_importance(dt.root, len(X_cls), importances)
if importances.sum() > 0:
    importances /= importances.sum()

print(f"  Feature importances:")
for i, imp in enumerate(importances):
    bar = "█" * int(imp * 40)
    print(f"    Feature {i}: {imp:.3f} {bar}")


# =====================================================================
#   PARTE 18: LEARNING RATE IMPACT
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 18: LR IMPACT ===")
print("=" * 80)

print("\n--- Learning rate on logistic regression ---")

for learning_rate in [0.001, 0.01, 0.1, 0.5, 1.0]:
    model = LogisticRegression(lr=learning_rate, epochs=500, reg=0.01)
    model.fit(X_train, y_train)
    y_p = model.predict(X_test)
    acc = np.mean(y_p == y_test)
    final_loss = model.loss_history[-1][1] if model.loss_history else 'N/A'
    print(f"  lr={learning_rate:.3f}: accuracy={acc:.4f}, final_loss={final_loss}")


# =====================================================================
#   PARTE 19: MODEL SELECTION GUIDE
# =====================================================================

print("\n\n" + "=" * 80)
print("=== CAPITULO 19: MODEL SELECTION ===")
print("=" * 80)

"""
GUIA DE SELECCION DE MODELO:

| Escenario               | Modelo recomendado     |
|-------------------------|------------------------|
| Baseline                | LogisticRegression     |
| Interpretable           | Decision Tree (shallow)|
| Small data              | Naive Bayes            |
| High-dimensional        | SVM (kernel)           |
| Non-linear boundaries   | Random Forest, SVM-RBF |
| Fast prediction needed  | Naive Bayes, LogReg    |
| Feature selection needed| Lasso, L1-LogReg       |
| Imbalanced classes      | Weighted LogReg, SMOTE |
| Few features            | KNN (with scaling)     |
| Production/speed        | Logistic Regression    |

REGLA DE ORO:
  1. Empezar con LogisticRegression.
  2. Si no es suficiente, Random Forest.
  3. Si aun no, XGBoost.
  4. Neural Networks solo si hay MUCHOS datos.
"""

guide = [
    ("Baseline", "LogisticRegression"),
    ("Interpretable", "Decision Tree"),
    ("Small data", "Naive Bayes"),
    ("Non-linear", "Random Forest / SVM-RBF"),
    ("Imbalanced", "Weighted + SMOTE"),
    ("Production", "LogReg (fast, simple)"),
]

print(f"\n  Model selection guide:")
for scenario, model in guide:
    print(f"    {scenario:>20s} → {model}")


print("\n" + "=" * 80)
print("=== CONCLUSION ARQUITECTONICA ===")
print("=" * 80)

"""
RESUMEN DE CLASIFICACION:

1. Logistic Regression: sigmoid + BCE + gradient descent.
2. Decision Tree: recursive splitting, Gini/entropy.
3. KNN: lazy learner, distance-based, scale features!
4. Naive Bayes: probabilistic, fast, assumes independence.
5. Metrics: Accuracy, Precision, Recall, F1, AUC.
6. Threshold tuning: optimize for business metric.
7. SIEMPRE: scale for KNN/Logistic, no need for trees.

Siguiente archivo: Unsupervised Learning.
"""

print("\n FIN DE ARCHIVO 03_clasificacion.")
print(" Clasificacion ha sido dominada.")
