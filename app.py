import streamlit as st
from sympy import symbols, Eq, expand, factor, sqrt, latex, simplify
from sympy import Rational, Integer
import math
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Matematică Interactivă", page_icon="🧮", layout="centered")

# ----------------- Utilitare -----------------
x = symbols('x')

def is_perfect_square(n):
    if n < 0:
        return False
    r = int(math.isqrt(int(n)))
    return r*r == n

def L(expr):
    return f"${latex(expr)}$"

# ----------------- Pași ecuație liniară -----------------
def build_linear_steps(a, b, c, d):
    steps = []
    a, b, c, d = Integer(a), Integer(b), Integer(c), Integer(d)
    eq0 = Eq(a*x + b, c*x + d)
    steps.append(("Enunț", f"Rezolvăm ecuația {L(eq0)}."))

    eq1 = Eq(expand(a*x + b), expand(c*x + d))
    steps.append(("Dezvoltăm", f"Dezvoltăm termenii: {L(eq1)}."))

    eq2 = Eq(eq1.lhs - c*x, eq1.rhs - c*x)
    steps.append(("Mutăm x la stânga", f"Scădem {L(c*x)} din ambele părți: {L(eq2)}."))

    eq3 = Eq(eq2.lhs - b, eq2.rhs - b)
    steps.append(("Mutăm constantele la dreapta", f"Scădem {L(b)} din ambele părți: {L(eq3)}."))

    lhs_simpl = simplify(eq3.lhs)
    rhs_simpl = simplify(eq3.rhs)
    eq4 = Eq(lhs_simpl, rhs_simpl)
    steps.append(("Combinăm termenii", f"Combinăm termenii asemenea: {L(eq4)}."))

    coef_x = simplify(lhs_simpl/x)
    rhs_const = rhs_simpl

    if coef_x == 0:
        if rhs_const == 0:
            steps.append(("Concluzie", "0 = 0 ⇒ infinit de soluții"))
        else:
            steps.append(("Concluzie", f"0 = {rhs_const} ⇒ fără soluții"))
        return steps

    eq5 = Eq(coef_x*x, rhs_const)
    steps.append(("Izolăm x", f"{L(eq5)}"))
    sol = simplify(rhs_const/coef_x)
    eq6 = Eq(x, sol)
    steps.append(("Împărțim la coeficient", f"{L(eq6)}"))
    steps.append(("Răspuns", f"Soluția este {L(eq6)}"))
    return steps

# ----------------- Pași ecuație pătratică -----------------
def build_quadratic_steps(a, b, c):
    steps = []
    a, b, c = Integer(a), Integer(b), Integer(c)
    if a == 0:
        steps.append(("Reducere", "Ecuația devine liniară"))
        steps += build_linear_steps(0, b, 0, -c)[1:]
        return steps

    eq0 = Eq(a*x**2 + b*x + c, 0)
    steps.append(("Enunț", f"Rezolvăm {L(eq0)}"))

    if a != 1:
        eq1 = Eq((a*x**2 + b*x + c)/a, 0)
        steps.append(("Normalizare", f"Împărțim la {L(a)} ⇒ {L(Eq(x**2 + (b/a)*x + c/a, 0))}"))

    Delta = simplify(b**2 - 4*a*c)
    steps.append(("Discriminant", f"Δ = b² - 4ac = {Delta}"))

    root_expr = ((-b + sqrt(Delta))/(2*a), (-b - sqrt(Delta))/(2*a))

    if Delta > 0:
        if is_perfect_square(int(Delta)):
            r = int(math.isqrt(int(Delta)))
            x1 = simplify((-b + r)/(2*a))
            x2 = simplify((-b - r)/(2*a))
            steps.append(("Soluții reale distincte", f"{L(Eq(x, x1))} și {L(Eq(x, x2))}"))
            steps.append(("Factorizare", f"{L(factor(a*x**2+b*x+c))}"))
        else:
            steps.append(("Soluții reale", f"{L(Eq(x, simplify(root_expr[0])))} și {L(Eq(x, simplify(root_expr[1])))}"))
    elif Delta == 0:
        x0 = simplify(-b/(2*a))
        steps.append(("Rădăcină dublă", f"{L(Eq(x, x0))}"))
        steps.append(("Scriere ca pătrat", f"{L(a*(x-x0)**2)}"))
    else:
        steps.append(("Δ < 0", "Soluții complexe"))
        steps.append(("Soluții", f"{L(Eq(x, simplify(root_expr[0])))} și {L(Eq(x, simplify(root_expr[1])))}"))

    return steps

# ----------------- UI -----------------
st.title("🧮 Matematică Interactivă")
st.write("Pași detaliați și grafic pentru ecuații")

mode = st.selectbox("Tipul problemei", ["Liniară", "Gradul II"])

if "steps" not in st.session_state:
    st.session_state.steps = []
if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0

def reset_steps(new_steps):
    st.session_state.steps = new_steps
    st.session_state.step_idx = 0

# ----------------- Input coeficienți și pași -----------------
if mode == "Liniară":
    colA, colB, colC, colD = st.columns(4)
    with colA: a = st.number_input("a", value=2, step=1)
    with colB: b = st.number_input("b", value=5, step=1)
    with colC: c = st.number_input("c", value=1, step=1)
    with colD: d = st.number_input("d", value=-3, step=1)
    if st.button("Generează pașii"):
        reset_steps(build_linear_steps(a, b, c, d))

else:
    colA, colB, colC = st.columns(3)
    with colA: a = st.number_input("a", value=1, step=1)
    with colB: b = st.number_input("b", value=-3, step=1)
    with colC: c = st.number_input("c", value=2, step=1)
    if st.button("Generează pașii"):
        reset_steps(build_quadratic_steps(a, b, c))

        # ----------------- Grafic interactiv -----------------
        x_vals = np.linspace(-10, 10, 500)
        y_vals = a*x_vals**2 + b*x_vals + c
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"{a}x²+{b}x+{c}"))
        fig.update_layout(title="Grafic interactiv",
                          xaxis_title="x",
                          yaxis_title="y",
                          width=700, height=500)
        st.plotly_chart(fig, use_container_width=True)

# ----------------- Navigare pași -----------------
st.divider()

if st.session_state.steps:
    total = len(st.session_state.steps)
    title, desc = st.session_state.steps[st.session_state.step_idx]
    st.subheader(f"Pasul {st.session_state.step_idx+1}/{total}: {title}")
    st.markdown(desc)

    c1, c2, c3 = st.columns([1,2,1])
    with c1:
        if st.button("⬅️ Înapoi", disabled=st.session_state.step_idx==0):
            st.session_state.step_idx -= 1
    with c3:
        if st.button("Înainte ➡️", disabled=st.session_state.step_idx >= total-1):
            st.session_state.step_idx += 1

    st.slider("Sari la pas", 1, total, st.session_state.step_idx+1, key="slider_jump")
    if st.session_state.slider_jump -1 != st.session_state.step_idx:
        st.session_state.step_idx = st.session_state.slider_jump -1
else:
    st.info("Completează coeficienții și apasă **Generează pașii**.")
