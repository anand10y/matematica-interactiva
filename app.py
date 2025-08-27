import streamlit as st
from sympy import symbols, Eq, expand, factor, sqrt, latex, simplify, diff, solve
from sympy import Integer
import math
import plotly.graph_objects as go
import numpy as np
import random

st.set_page_config(page_title="Laborator Matematică Interactiv", page_icon="🧮", layout="wide")

x, y, z = symbols('x y z')

def L(expr):
    return f"${latex(expr)}$"

def is_perfect_square(n):
    if n < 0: return False
    r = int(math.isqrt(int(n)))
    return r*r == n

# ----------------- Pași ecuație liniară -----------------
def linear_steps(a, b, c, d):
    steps = []
    a, b, c, d = Integer(a), Integer(b), Integer(c), Integer(d)
    eq0 = Eq(a*x + b, c*x + d)
    steps.append(("Enunț", f"Rezolvăm {L(eq0)}"))

    eq1 = Eq(expand(a*x + b), expand(c*x + d))
    steps.append(("Dezvoltăm", L(eq1)))

    eq2 = Eq(eq1.lhs - c*x, eq1.rhs - c*x)
    steps.append(("Mutăm x la stânga", L(eq2)))

    eq3 = Eq(eq2.lhs - b, eq2.rhs - b)
    steps.append(("Mutăm constantele la dreapta", L(eq3)))

    lhs_simpl = simplify(eq3.lhs)
    rhs_simpl = simplify(eq3.rhs)
    eq4 = Eq(lhs_simpl, rhs_simpl)
    steps.append(("Combinăm termenii", L(eq4)))

    coef_x = simplify(lhs_simpl/x)
    rhs_const = rhs_simpl

    if coef_x == 0:
        if rhs_const == 0:
            steps.append(("Concluzie", "0 = 0 ⇒ infinit de soluții"))
        else:
            steps.append(("Concluzie", f"0 = {rhs_const} ⇒ fără soluții"))
        return steps

    eq5 = Eq(coef_x*x, rhs_const)
    steps.append(("Izolăm x", L(eq5)))
    sol = simplify(rhs_const/coef_x)
    eq6 = Eq(x, sol)
    steps.append(("Răspuns", L(eq6)))
    return steps

# ----------------- Pași ecuație pătratică -----------------
def quadratic_steps(a, b, c):
    steps = []
    a, b, c = Integer(a), Integer(b), Integer(c)
    if a == 0:
        steps.append(("Reducere", "Devine ecuație liniară"))
        steps += linear_steps(0, b, 0, -c)[1:]
        return steps

    eq0 = Eq(a*x**2 + b*x + c, 0)
    steps.append(("Enunț", L(eq0)))

    if a != 1:
        eq1 = Eq((a*x**2 + b*x + c)/a, 0)
        steps.append(("Normalizare", L(Eq(x**2 + (b/a)*x + c/a, 0))))

    Delta = simplify(b**2 - 4*a*c)
    steps.append(("Discriminant", f"Δ = {Delta}"))

    root_expr = ((-b + sqrt(Delta))/(2*a), (-b - sqrt(Delta))/(2*a))

    if Delta > 0:
        if is_perfect_square(int(Delta)):
            r = int(math.isqrt(int(Delta)))
            x1 = simplify((-b + r)/(2*a))
            x2 = simplify((-b - r)/(2*a))
            steps.append(("Soluții reale distincte", f"{L(Eq(x,x1))} și {L(Eq(x,x2))}"))
            steps.append(("Factorizare", L(factor(a*x**2 + b*x + c))))
        else:
            steps.append(("Soluții reale", f"{L(Eq(x, simplify(root_expr[0])))} și {L(Eq(x, simplify(root_expr[1])))}"))
    elif Delta == 0:
        x0 = simplify(-b/(2*a))
        steps.append(("Rădăcină dublă", L(Eq(x,x0))))
        steps.append(("Scriere ca pătrat", L(a*(x-x0)**2)))
    else:
        steps.append(("Δ < 0", "Soluții complexe"))
        steps.append(("Soluții", f"{L(Eq(x, simplify(root_expr[0])))} și {L(Eq(x, simplify(root_expr[1])))}"))

    return steps

# ----------------- Sisteme de ecuații liniare 2x2 -----------------
def solve_linear_system_2x2(a1,b1,c1,a2,b2,c2):
    eq1 = Eq(a1*x + b1*y, c1)
    eq2 = Eq(a2*x + b2*y, c2)
    steps = [("Sistemul inițial", f"{L(eq1)}, {L(eq2)}")]

    # Eliminare x
    det = a1*b2 - a2*b1
    if det == 0:
        steps.append(("Determinant zero", "Sistem dependent sau incompatibil"))
        return steps
    y_sol = simplify((c2*a1 - c1*a2)/(a1*b2 - a2*b1))
    x_sol = simplify((c1 - b1*y_sol)/a1)
    steps.append(("Rezolvare", f"x = {x_sol}, y = {y_sol}"))
    return steps

# ----------------- Funcții și derivate -----------------
def derivative_steps(expr):
    steps = []
    steps.append(("Funcția inițială", L(expr)))
    deriv = diff(expr,x)
    steps.append(("Derivata", L(deriv)))
    return steps, deriv

# ----------------- Exerciții generate aleator -----------------
def random_linear():
    a = random.randint(1,10)
    b = random.randint(-10,10)
    c = random.randint(-10,10)
    sol = (c-b)/a
    return a,b,c,sol

def random_quadratic():
    a = random.randint(1,5)
    x0 = random.randint(-5,5)
    x1 = random.randint(-5,5)
    poly = a*(x-x0)*(x-x1)
    coeffs = poly.expand().as_poly().all_coeffs()
    return coeffs, [x0,x1]

# ----------------- UI -----------------
st.title("🧮 Laborator Matematică Interactiv")
st.write("Pași detaliați, grafice și exerciții")

mode = st.selectbox("Tipul exercițiului", ["Ecuație liniară","Ecuație pătratică","Sistem 2x2","Derivare funcție","Exercițiu random"])

if "steps" not in st.session_state: st.session_state.steps=[]
if "step_idx" not in st.session_state: st.session_state.step_idx=0

def reset_steps(new_steps):
    st.session_state.steps=new_steps
    st.session_state.step_idx=0

# ----------------- Input și pași -----------------
if mode=="Ecuație liniară":
    a = st.number_input("a",2)
    b = st.number_input("b",5)
    c = st.number_input("c",1)
    d = st.number_input("d",-3)
    if st.button("Generează pașii"):
        reset_steps(linear_steps(a,b,c,d))

elif mode=="Ecuație pătratică":
    a = st.number_input("a",1)
    b = st.number_input("b",-3)
    c = st.number_input("c",2)
    if st.button("Generează pașii"):
        reset_steps(quadratic_steps(a,b,c))
        x_vals = np.linspace(-10,10,500)
        y_vals = a*x_vals**2 + b*x_vals + c
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f"{a}x²+{b}x+{c}"))
        fig.update_layout(title="Grafic interactiv",xaxis_title="x",yaxis_title="y",width=700,height=500)
        st.plotly_chart(fig,use_container_width=True)

elif mode=="Sistem 2x2":
    col1,col2,col3=st.columns(3)
    with col1:
        a1=st.number_input("a1",1)
        b1=st.number_input("b1",1)
        c1=st.number_input("c1",0)
    with col2:
        a2=st.number_input("a2",1)
        b2=st.number_input("b2",-1)
        c2=st.number_input("c2",0)
    if st.button("Generează pașii"):
        reset_steps(solve_linear_system_2x2(a1,b1,c1,a2,b2,c2))

elif mode=="Derivare funcție":
    expr_str=st.text_input("Funcție polinomială (ex: x**3-5*x+2)","x**3-5*x+2")
    if st.button("Calculează derivata"):
        try:
            expr=eval(expr_str)
            steps, deriv = derivative_steps(expr)
            reset_steps(steps)
            # grafic interactiv
            x_vals = np.linspace(-10,10,500)
            y_vals = [expr.subs(x,val) for val in x_vals]
            y_der = [deriv.subs(x,val) for val in x_vals]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name="f(x)"))
            fig.add_trace(go.Scatter(x=x_vals, y=y_der, mode='lines', name="f'(x)"))
            fig.update_layout(title="Funcție și derivată",xaxis_title="x",yaxis_title="y",width=700,height=500)
            st.plotly_chart(fig,use_container_width=True)
        except:
            st.error("Funcție invalidă")

elif mode=="Exercițiu random":
    tipo = st.selectbox("Tip exercițiu",["Liniar","Pătratic"])
    if st.button("Generează exercițiu"):
        if tipo=="Liniar":
            a,b,c,sol = random_linear()
            st.write(f"Rezolvă ecuația: {a}*x + {b} = {c}")
            ans = st.number_input("Răspunsul tău",0)
            if st.button("Verifică răspunsul"):
                if ans==sol:
                    st.success("Corect!")
                else:
                    st.error(f"Gresit. Răspuns corect: {sol}")
        else:
            coeffs, sols = random_quadratic()
            st.write(f"Rezolvă ecuația: {coeffs[0]}*x² + {coeffs[1]}*x + {coeffs[2]} = 0")
            x1 = st.number_input("x1",0)
            x2 = st.number_input("x2",0)
            if st.button("Verifică răspunsul"):
                if set([x1,x2])==set(sols):
                    st.success("Corect!")
                else:
                    st.error(f"Gresit. Răspuns corect: {sols}")

# ----------------- Navigare pași -----------------
st.divider()
if st.session_state.steps:
    total=len(st.session_state.steps)
    title, desc=st.session_state.steps[st.session_state.step_idx]
    st.subheader(f"Pas {st.session_state.step_idx+1}/{total}: {title}")
    st.markdown(desc)

    c1,c2,c3=st.columns([1,2,1])
    with c1:
        if st.button("⬅️ Înapoi",disabled=st.session_state.step_idx==0):
            st.session_state.step_idx-=1
    with c3:
        if st.button("Înainte ➡️",disabled=st.session_state.step_idx>=total-1):
            st.session_state.step_idx+=1

    st.slider("Sari la pas",1,total,st.session_state.step_idx+1,key="slider_jump")
    if st.session_state.slider_jump-1!=st.session_state.step_idx:
        st.session_state.step_idx=st.session_state.slider_jump-1
else:
    st.info("Generează pașii pentru a-i vizualiza aici.")
