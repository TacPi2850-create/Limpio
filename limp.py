import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta

# Funzione per generare il calendario delle pulizie
def generate_schedule():
    start_date = datetime.strptime("2025-03-23", "%Y-%m-%d").date()  # prima domenica
    weeks = 52
    persons = ["JL1", "JL2"]
    tasks = ["🛁 Bagno", "🍽️ Cucina"]

    data = []

    for i in range(weeks):
        sunday = start_date + timedelta(weeks=i)
        saturday = sunday - timedelta(days=1)
        wednesday = sunday - timedelta(days=4)

        # Mercoledì: A3 pulisce il bagno
        data.append({"Data": wednesday, "Persona": "A3", "Mansione": "🛁 Bagno"})

        # Sabato: 1 persona di JL1 o JL2 fa il bagno
        saturday_person = persons[i % 2]
        data.append({"Data": saturday, "Persona": saturday_person, "Mansione": "🛁 Bagno"})

        # Domenica: l'altra persona fa la cucina
        sunday_person = persons[(i + 1) % 2]
        data.append({"Data": sunday, "Persona": sunday_person, "Mansione": "🍽️ Cucina"})

    return pd.DataFrame(data)

# Creiamo il calendario delle pulizie
df = generate_schedule()

# Stile CSS migliorato per layout, sfondo e contrasto
st.markdown("""
    <style>
        body, .stApp { background-color: #D6EAF8; }
        .main { background-color: #D6EAF8; }
        .sidebar .sidebar-content { background-color: #D6EAF8; }
        h1, h2, h3, h4, h5, h6, label { color: #0D47A1 !important; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; background-color: #000000; border: 2px solid #FFFFFF; }
        th, td { text-align: center; padding: 12px; font-size: 18px; border: 2px solid #FFFFFF; color: white; background-color: #222; }
        th { background-color: #1F618D; color: white; }
        .sunday { background-color: #1C1C1C !important; font-weight: bold; border: 2px solid #FFFFFF; }
        .task-person-jl1 { color: #FFD700; font-weight: bold; }
        .task-person-jl2 { color: #00FA9A; font-weight: bold; }
        .task-person-a3 { color: #FF69B4; font-weight: bold; }
        .saturday { background-color: #2E2E2E !important; }
        .wednesday { background-color: #424949 !important; }
        .stSelectbox label, .stDateInput label { color: #0D47A1 !important; font-weight: bold; }
        .stTitle { color: #0D47A1 !important; }
        td {
    vertical-align: top;
    line-height: 1.4;
}

    /* Aumenta la larghezza del contenitore Streamlit */
    .main, .stApp {
        max-width: 100% !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Rendi il calendario più grande */
    table {
        width: 100%;
        table-layout: fixed;
    }

    td, th {
        padding: 18px;
        font-size: 20px;
        word-wrap: break-word;
    }

    /* Allarga la colonna di destra */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100% !important;
    }
@media screen and (max-width: 768px) {
    td, th {
        font-size: 16px;
        padding: 10px;
    }
}
.stSelectbox, .stDateInput {
    width: 100% !important;
}
    </style>
""", unsafe_allow_html=True)

# UI Streamlit con layout a colonne
st.markdown("<h1 style='color: #0D47A1;'>📆 Calendario Pulizie Domenicali</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])

with col1:
    selected_year = st.selectbox("📅 Seleziona l'anno", [2025, 2026], index=0)
    selected_month = st.selectbox("🗓️ Seleziona il mese", list(range(1, 13)), index=datetime.today().month - 1)
    selected_date = st.date_input("📅 Seleziona una data per vedere i dettagli delle pulizie", value=datetime.today())
    daily_tasks = df[df["Data"] == selected_date]
    if not daily_tasks.empty:
        st.write("### Dettagli Pulizie per:", selected_date.strftime('%d %B %Y'))
        st.table(daily_tasks)
    else:
        st.write("Un lugar limpio es un lugar feliz! 😊")

# Generazione del calendario mensile
month_days = calendar.monthcalendar(selected_year, selected_month)

# Creazione tabella calendario
calendar_html = "<table>"
calendar_html += "<tr><th>Lun</th><th>Mar</th><th>Mer</th><th>Gio</th><th>Ven</th><th>Sab</th><th style='color: red;'>Dom</th></tr>"

for week in month_days:
    calendar_html += "<tr>"
    for day in week:
        if day == 0:
            calendar_html += "<td></td>"  # Giorno vuoto
        else:
            date = datetime(selected_year, selected_month, day).date()
            task = df[df["Data"] == date]
            cell_content = f"<b>{day}</b><br>"
            
            if not task.empty:
             for _, row in task.iterrows():
              person_class = f"task-person-{row['Persona'].lower()}"
              cell_content += f"<span class='{person_class}'>{row['Persona']}</span> {row['Mansione']}<br>"

    # Chiudiamo la cella solo UNA volta dopo aver aggiunto tutti i task
             if date.weekday() == 6:
               calendar_html += f"<td class='sunday'>{cell_content}</td>"
             elif date.weekday() == 5:
               calendar_html += f"<td class='saturday'>{cell_content}</td>"
             elif date.weekday() == 2:
               calendar_html += f"<td class='wednesday'>{cell_content}</td>"
             else:
               calendar_html += f"<td>{cell_content}</td>"
            else:
             calendar_html += f"<td>{cell_content}</td>"
    calendar_html += "</tr>"


# Mostriamo la tabella calendario nella seconda colonna
with col2:
    st.markdown(calendar_html, unsafe_allow_html=True)
