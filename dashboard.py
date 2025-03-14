import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("🌿 Dashboard de Irrigação Inteligente")

historico_file = 'historico_irrigacao.csv'
if os.path.exists(historico_file):
    historico = pd.read_csv(historico_file)

    st.subheader("📄 Histórico de Leituras")
    st.dataframe(historico)

    st.subheader("🌱 Umidade do Solo ao Longo do Tempo")
    fig, ax = plt.subplots()
    ax.plot(historico['timestamp'], historico['umidade_do_solo'], marker='o', color='green')
    ax.set_xlabel('Data e Hora')
    ax.set_ylabel('Umidade do Solo (%)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("🌡️ Temperatura ao Longo do Tempo")
    fig, ax = plt.subplots()
    ax.plot(historico['timestamp'], historico['temperatura'], marker='o', color='red')
    ax.set_xlabel('Data e Hora')
    ax.set_ylabel('Temperatura (°C)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("🚰 Decisões de Irrigação")
    decision_count = historico['decisao'].value_counts()
    st.bar_chart(decision_count)

else:
    st.warning("O arquivo de histórico 'historico_irrigacao.csv' não foi encontrado.")

st.markdown("---")