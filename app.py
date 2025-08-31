import pandas as pd
import streamlit as st
import plotly.express as px
import io

st.title("📊 Statistici interactive pe clase și probe")

# --- Upload fișier ---
uploaded_file = st.file_uploader("Încarcă fișierul Excel cu elevi", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # --- Calcul media generală dacă lipsește ---
    if "Media" not in df.columns:
        df["Media"] = df[["Ea","Ec","Ed"]].mean(axis=1)

    # --- Status Reușit/Nereușit ---
    df["Status"] = df["Media"].apply(lambda x: "Reușit" if x >= 5 else "Nereușit")

    st.subheader("📋 Date brute")
    st.dataframe(df)

    # --- Selectare clasa și probă ---
    clase = sorted(df["Clasa"].unique())
    clasa_selectata = st.selectbox("Selectează clasa", ["Toate"] + clase)
    probe = ["Ea", "Ec", "Ed"]
    proba_selectata = st.selectbox("Selectează proba", ["Toate"] + probe)

    # --- Filtrare date ---
    df_filtrat = df.copy()
    if clasa_selectata != "Toate":
        df_filtrat = df_filtrat[df_filtrat["Clasa"] == clasa_selectata]

    st.subheader("📋 Date filtrate")
    st.dataframe(df_filtrat)

    # --- Statistica pe clase ---
    st.subheader("📊 Statistica pe clase")
    stat_clasa = []
    for clasa in sorted(df_filtrat["Clasa"].unique()):
        df_clasa = df_filtrat[df_filtrat["Clasa"] == clasa]
        stat_clasa.append({
            "Clasa": clasa,
            "Număr elevi": len(df_clasa),
            "Media Ea": df_clasa["Ea"].mean(),
            "Media Ec": df_clasa["Ec"].mean(),
            "Media Ed": df_clasa["Ed"].mean(),
            "Reușiți": len(df_clasa[df_clasa["Status"]=="Reușit"]),
            "Nereușiți": len(df_clasa[df_clasa["Status"]=="Nereușit"])
        })
    df_stat = pd.DataFrame(stat_clasa)
    st.dataframe(df_stat)

    # --- Grafice interactive ---
    st.subheader("📈 Grafic medii pe probe și clase")
    probe_graf = probe if proba_selectata == "Toate" else [proba_selectata]

    for probă in probe_graf:
        fig = px.bar(df_filtrat, x="Clasa", y=probă, color="Status", barmode="group",
                     title=f"Media pe probă {probă} per clasă")
        st.plotly_chart(fig, use_container_width=True)

    # --- Export Excel ---
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Date brute")
        df_stat.to_excel(writer, index=False, sheet_name="Statistica pe clase")
    data_xlsx = output.getvalue()

    st.download_button(
        label="⬇️ Descarcă raport Excel cu statistici",
        data=data_xlsx,
        file_name="raport_statistic.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
