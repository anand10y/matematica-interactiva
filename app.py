import streamlit as st
from sympy import symbols, Eq, expand, factor, sqrt, latex, simplify
from sympy import Rational, Integer
import math

st.set_page_config(page_title="Matematică - Pași explicați", page_icon="🧮", layout="centered")

# ----------------- Utilitare -----------------
x = symbols('x')

def is_perfect_square(n):
    if n < 0:
        return False
    r = int(math.isqrt(int(n)))
    return r*r == n

def L(expr):
    """LaTeX safe."""
    return f"${latex(expr)}$"

# ----------------- Generare pași: Liniară -----------------
def build_linear_steps(a, b, c, d):
    steps = []
    a, b, c, d = Integer(a), Integer(b), Integer(c), Integer(d)

    eq0 = Eq(a*x + b, c*x + d)
    steps.append(("Enunț", f"Rezolvăm ecuația {L(eq0)}."))

    # 1) Dezvoltăm (formal)
    eq1 = Eq(expand(a*x + b), expand(c*x + d))
    steps.append(("Dezvoltăm", f"Dezvoltăm termenii (aici rămân la fel): {L(eq1)}."))

    # 2) Mutăm termenii cu x în stânga (scădem c*x)
    eq2 = Eq(eq1.lhs - c*x, eq1.rhs - c*x)
    steps.append(("Mutăm x la stânga", f"Scădem {L(c*x)} din ambele părți: {L(eq2)}."))

    # 3) Mutăm termenii constanți în dreapta (scădem b)
    eq3 = Eq(eq2.lhs - b, eq2.rhs - b)
    steps.append(("Mutăm constantele la dreapta", f"Scădem {L(b)} din ambele părți: {L(eq3)}."))

    # 4) Combinăm termenii asemenea
    lhs_simpl = simplify(eq3.lhs)
    rhs_simpl = simplify(eq3.rhs)
    eq4 = Eq(lhs_simpl, rhs_simpl)
    steps.append(("Combinăm termenii", f"Combinăm termenii asemenea: {L(eq4)}."))

    coef_x = simplify(eq4.lhs / x) if eq4.lhs.has(x) and simplify(eq4.lhs/x).free_symbols == set() else a - c
    # în mod tipic coef_x = a - c, iar dreapta = d - b
    if isinstance(coef_x, Rational) or isinstance(coef_x, Integer):
        coef_x = simplify(coef_x)
    rhs_const = simplify(rhs_simpl)

    # 5) Cazuri
    if coef_x == 0:
        if rhs_const == 0:
            steps.append(("Concluzie", "Obținem identitatea adevărată 0 = 0 ⇒ **infinit de multe soluții**."))
        else:
            steps.append(("Concluzie", f"Obținem contradicția {L(Eq(0, rhs_const))} ⇒ **fără soluții**."))
        return steps

    eq5 = Eq(coef_x*x, rhs_const)
    steps.append(("Izolăm x", f"Ecuație liniară simplă: {L(eq5)}."))

    sol = simplify(rhs_const/coef_x)
    eq6 = Eq(x, sol)
    steps.append(("Împărțim la coeficientul lui x", f"Împărțim ambele părți la {L(coef_x)}: {L(eq6)}."))

    steps.append(("Răspuns", f"Soluția este {L(eq6)}."))
    return steps

# ----------------- Generare pași: Quadratică -----------------
def build_quadratic_steps(a, b, c):
    steps = []
    a, b, c = Integer(a), Integer(b), Integer(c)

    # Dacă a = 0, reducere la liniară bx + c = 0
    if a == 0:
        steps.append(("Reducere", "Coeficientul lui \(x^2\) este 0 ⇒ ecuația devine liniară."))
        steps += build_linear_steps(0, b, 0, -c)[1:]  # fără să mai repetăm „Enunț”
        return steps

    eq0 = Eq(a*x**2 + b*x + c, 0)
    steps.append(("Enunț", f"Rezolvăm ecuația {L(eq0)}."))

    # 1) Normalizăm (împărțim la a)
    if a != 1:
        eq1 = Eq((a*x**2 + b*x + c)/a, 0)
        steps.append(("Normalizare", f"Împărțim la {L(a)} (≠0): {L(eq1)} ⇒ {L(Eq(x**2 + (b/a)*x + c/a, 0))}."))
    A = a
    B = b
    C = c

    # 2) Discriminant
    Delta = simplify(B**2 - 4*A*C)
    steps.append(("Discriminant", f"Calculăm \(\\Delta = b^2 - 4ac = {latex(B**2)} - 4·{latex(A)}·{latex(C)} = {latex(Delta)}\)."))

    # 3) Formula rădăcinilor
    root_expr = ((-B) + sqrt(Delta))/(2*A), ((-B) - sqrt(Delta))/(2*A)
    steps.append(("Formula rădăcinilor", f"{L(Eq(x, (-B+sqrt(Delta))/(2*A)))} și {L(Eq(x, (-B-sqrt(Delta))/(2*A)))}."))

    # 4) Cazuri după Δ
    if Delta > 0:
        if is_perfect_square(int(Delta)):
            r = Integer(int(math.isqrt(int(Delta))))
            steps.append(("Δ > 0 și pătrat perfect", f"\\(\\Delta={latex(Delta)}={latex(r**2)}\\) ⇒ \\(\\sqrt\\Delta={latex(r)}\\)."))
            x1 = simplify(( -B + r )/(2*A))
            x2 = simplify(( -B - r )/(2*A))
            steps.append(("Soluții reale distincte", f"{L(Eq(x, x1))} și {L(Eq(x, x2))}."))
            # Factorizare opțională
            poly = a*x**2 + b*x + c
            steps.append(("Factorizare", f"{L(poly)} = {L(factor(poly))}."))
        else:
            steps.append(("Δ > 0 (nu e pătrat perfect)", "Soluțiile sunt reale, dar iraționale:"))
            steps.append(("Soluții", f"{L(Eq(x, simplify(root_expr[0])))} și {L(Eq(x, simplify(root_expr[1])))}."))
    elif Delta == 0:
        x0 = simplify(-B/(2*A))
        steps.append(("Δ = 0", f"Rădăcină dublă: {L(Eq(x, x0))}."))
        poly = a*x**2 + b*x + c
        steps.append(("Scriere ca pătrat", f"{L(poly)} = {L(A*(x - x0)**2)}."))
    else:
        steps.append(("Δ < 0", "Soluțiile sunt complexe:"))
        steps.append(("Soluții", f"{L(Eq(x, simplify(root_expr[0])))} și {L(Eq(x, simplify(root_expr[1])))}."))

    return steps

# ----------------- UI -----------------
st.title("🧮 Aplicație pentru învățarea matematicii — pași explicativi")
st.write("Alege tipul problemei și parcurge **pas cu pas** rezolvarea. Formulele sunt randate în LaTeX.")

mode = st.selectbox("Alege tipul de exercițiu", ["Ecuație liniară (ax+b=cx+d)", "Ecuație de gradul II (ax²+bx+c=0)"])

# Session state pentru pași și index curent
if "steps" not in st.session_state:
    st.session_state.steps = []
if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0

def reset_steps(new_steps):
    st.session_state.steps = new_steps
    st.session_state.step_idx = 0

if mode.startswith("Ecuație liniară"):
    colA, colB, colC, colD = st.columns(4)
    with colA: a = st.number_input("a", value=2, step=1)
    with colB: b = st.number_input("b", value=5, step=1)
    with colC: c = st.number_input("c", value=1, step=1)
    with colD: d = st.number_input("d", value=-3, step=1)

    if st.button("Generează pașii"):
        steps = build_linear_steps(a, b, c, d)
        reset_steps(steps)

else:
    colA, colB, colC = st.columns(3)
    with colA: a = st.number_input("a", value=1, step=1)
    with colB: b = st.number_input("b", value=-3, step=1)
    with colC: c = st.number_input("c", value=2, step=1)

    if st.button("Generează pașii"):
        steps = build_quadratic_steps(a, b, c)
        reset_steps(steps)

st.divider()

# Afișare pași + navigare
if st.session_state.steps:
    total = len(st.session_state.steps)
    title, desc = st.session_state.steps[st.session_state.step_idx]
    st.subheader(f"Pasul {st.session_state.step_idx + 1}/{total}: {title}")
    st.markdown(desc)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⬅️ Înapoi", disabled=st.session_state.step_idx == 0):
            st.session_state.step_idx = max(0, st.session_state.step_idx - 1)
    with c3:
        if st.button("Înainte ➡️", disabled=st.session_state.step_idx >= total - 1):
            st.session_state.step_idx = min(total - 1, st.session_state.step_idx + 1)

    st.slider("Sari la pas", 1, total, st.session_state.step_idx + 1, key="slider_jump")
    # sincronizează slider-ul cu indexul
    if st.session_state.slider_jump - 1 != st.session_state.step_idx:
        st.session_state.step_idx = st.session_state.slider_jump - 1

    with st.expander("Vezi toți pașii"):
        for i, (t, d) in enumerate(st.session_state.steps, start=1):
            st.markdown(f"**Pasul {i}: {t}**")
            st.markdown(d)
            st.markdown("---")
else:
    st.info("Completează coeficienții și apasă **Generează pașii** pentru a porni.")
