import streamlit as st
import pandas as pd
import os

# ---------- Config ----------
stats_file = f"https://raw.githubusercontent.com/prerit26/Hospital-Wait-time/main/2. Small and Big hospitals(avg per day one case)/count_more_than_181.csv"
image_folder = f"https://raw.githubusercontent.com/prerit26/Hospital-Wait-time/main/3. Hospital_bell_curves"

# ---------- Load summary stats ----------
@st.cache_data
def load_summary():
    df = pd.read_csv(stats_file)
    df.columns = df.columns.str.strip()
    df['Admission Hospital Name'] = df['Admission Hospital Name'].str.upper().str.strip()
    return df

summary_df = load_summary()

# ---------- UI Header ----------
st.title("🏥 Hospital Wait Time Dashboard")

# ---------- Dropdown ----------
hospital_list = sorted(summary_df['Admission Hospital Name'].unique())
selected_hospital = st.selectbox("Select a Hospital", hospital_list)

# ---------- Show Bell Curve Image ----------
safe_name = selected_hospital.replace(" ", "_").replace("/", "_")
image_path = os.path.join(image_folder, f"{safe_name}.png")

if os.path.exists(image_path):
    st.image(image_path, caption=f"Bell Curve - {selected_hospital}")
else:
    st.warning("No bell curve image found for this hospital.")

# ---------- Show Summary Statistics ----------
st.subheader("📊 Statistical Summary")
stats_row = summary_df[summary_df['Admission Hospital Name'] == selected_hospital]

if not stats_row.empty:
    st.dataframe(stats_row.T.rename(columns={stats_row.index[0]: "Value"}))
else:
    st.error("No statistical data available for this hospital.")
