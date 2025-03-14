import random
import pandas as pd
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

def gerar_dados_simulados(samples=100):
    data = []
    current_time = datetime.now()

    timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    umidade_do_solo = round(random.uniform(10, 90), 2)
    temperatura = round(random.uniform(15, 40), 2)
    luminosidade = round(random.uniform(100, 1000), 2)
    irrigar = 1 if umidade_do_solo < 30 and temperatura > 25 else 0

    for _ in range(samples):
        sample = {
            'timestamp': timestamp,
            'umidade_do_solo': umidade_do_solo,
            'temperatura': temperatura,
            'luminosidade': luminosidade,
            'irrigar' : irrigar
        }
        data.append(sample)
        current_time += timedelta(minutes=15)

    return pd.DataFrame(data)


def simular_nova_leitura():
    return {
        'umidade_do_solo': round(random.uniform(10, 90), 2),
        'temperatura': round(random.uniform(15, 40), 2),
        'luminosidade': round(random.uniform(100, 1000), 2)
    }

data = gerar_dados_simulados(200)

features = ['umidade_do_solo', 'temperatura', 'luminosidade']
X = data[features]
y = data['irrigar']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Precisão:", accuracy_score(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))

historico_file = 'historico_irrigacao.csv'
if os.path.exists(historico_file):
    historico = pd.read_csv(historico_file)
else:
    historico = pd.DataFrame(columns=['timestamp', 'umidade_do_solo', 'temperatura', 'luminosidade', 'decisao'])

new_data = simular_nova_leitura()
print("\nNova leitura de sensores:", new_data)

data_input = scaler.transform([[new_data['umidade_do_solo'], new_data['temperatura'], new_data['luminosidade']]])
prediction = model.predict(data_input)

decision = "Irrigar" if prediction[0] == 1 else "Nao Irrigar"
print(f"Ação: {decision}")

historico = pd.concat([historico, pd.DataFrame({
    'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    'umidade_do_solo': [new_data['umidade_do_solo']],
    'temperatura': [new_data['temperatura']],
    'luminosidade': [new_data['luminosidade']],
    'decisao': [decision]
})], ignore_index=True)

historico.to_csv(historico_file, index=False)
print("\nHistórico atualizado e salvo em 'historico_irrigacao.csv'.")
