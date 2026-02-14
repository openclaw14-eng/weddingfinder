"""
RDW Dashboard - Voertuigregistratie & Rijbewijs Controle
Bonaire-style tropical theme
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="RDW Dashboard - Bonaire",
    page_icon="🚗",
    layout="wide"
)

# Custom CSS - Caribbean theme
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%); }
    .header { 
        background: linear-gradient(90deg, #0052a4 0%, #0077b6 100%); 
        padding: 1.5rem; 
        border-radius: 10px; 
        color: white; 
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #0052a4;
    }
    .search-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🚗 RDW Dashboard - Bonaire</h1>
    <p>Voertuigregistratie & Rijbewijs Controlesysteem</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📋 Menu")
    menu = st.radio("Selecteer module:", 
        ["Voertuig Check", "Rijbewijs Check", "Dashboard", "Statistieken"])
    
    st.divider()
    st.info("🔐 Beveiligde toegang")
    st.write("Gebruiker: Admin")
    st.write("Rol: Inspecteur")

# Mock data
def get_vehicle_data(kenteken):
    """Haal voertuiggegevens op"""
    data = {
        "kenteken": kenteken.upper(),
        "merk": random.choice(["Toyota", "Honda", "Ford", "Chevrolet", "Mitsubishi"]),
        "model": random.choice(["Corolla", "Civic,", "Fiesta", "Silverado", "Pajero"]),
        "bouwjaar": random.randint(2010, 2025),
        "kleur": random.choice(["Wit", "Blauw", "Grijs", "Zwart", "Rood"]),
        "brandstof": random.choice(["Benzine", "Diesel", "Elektrisch", "LPG"]),
        " APK": random.choice(["Geldig", "Verlopen", "Binnenkort verlopen"]),
        "eigenaar": random.choice(["Particulier", "Bedrijf", "Overheid"]),
        "status": random.choice(["Actief", "Gearchiveerd", "Gesearchiveerd"]),
    }
    return data

def get_license_data(rijbewijsnummer):
    """Haal rijbewijsgegevens op"""
    expiry = datetime.now() + timedelta(days=random.randint(-365, 1095))
    data = {
        "nummer": rijbewijsnummer.upper(),
        "naam": random.choice(["Jan Jansen", "Pieter Peterson", "Maria Martinez", "Karel Kers"]),
        "geboortedatum": f"{random.randint(1,28)}-{random.randint(1,12)}-{random.randint(1960, 2005)}",
        "categorie": random.choice(["A", "B", "AB", "BE", "C", "D"]),
        "geldig_tot": expiry.strftime("%d-%m-%Y"),
        "status": "Geldig" if expiry > datetime.now() else "Verlopen",
        "punten": random.randint(0, 12),
    }
    return data

# Main content based on menu selection
if menu == "Voertuig Check":
    st.subheader("🔍 Voertuig Kenteken Check")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            kenteken = st.text_input("Voer kenteken in:", placeholder="BB-123-KR").upper()
        with col2:
            st.write("")
            st.write("")
            check_btn = st.button("🔎 Zoeken", type="primary")
    
    if kenteken and check_btn:
        with st.spinner("Zoeken in RDW database..."):
            vehicle = get_vehicle_data(kenteken)
        
        st.success("✅ Voertuig gevonden!")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Merk", vehicle["merk"])
        c2.metric("Model", vehicle["model"])
        c3.metric("Bouwjaar", str(vehicle["bouwjaar"]))
        c4.metric("Brandstof", vehicle["brandstof"])
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Kleur", vehicle["kleur"])
        c2.metric("APK", vehicle[" APK"])
        c3.metric("Eigenaar", vehicle["eigenaar"])
        c4.metric("Status", vehicle["status"])

elif menu == "Rijbewijs Check":
    st.subheader("🪪 Rijbewijs Controle")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        rijbewijs = st.text_input("Voer rijbewijsnummer in:", placeholder="NL12345678").upper()
    with col2:
        st.write("")
        st.write("")
        check_btn = st.button("🔎 Valideren", type="primary")
    
    if rijbewijs and check_btn:
        with st.spinner("Valideren..."):
            license = get_license_data(rijbewijs)
        
        if license["status"] == "Geldig":
            st.success("✅ Rijbewijs is geldig")
        else:
            st.error("❌ Rijbewijs is verlopen!")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Naam", license["naam"])
        c2.metric("Geb datum", license["geboortedatum"])
        c3.metric("Categorie", license["categorie"])
        c4.metric("Geldig tot", license["geldig_tot"])
        
        st.metric("Strafpunten", f"{license['punten']}/12", 
            delta_color="inverse" if license["punten"] > 6 else "normal")

elif menu == "Dashboard":
    st.subheader("📊 Live Dashboard")
    
    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Voertuigen geregistreerd", "12,847", "+23 vandaag")
    m2.metric("Rijbewijzen actief", "8,432", "+12 vandaag")
    m3.metric("APK checks", "1,247", "+5 vandaag")
    m4.metric("Openstaande boetes", "156", "-8 deze week")
    
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Voertuigen per type")
        chart_data = pd.DataFrame({
            "Type": ["Personenauto", "Bedrijfswagen", "Motor", "Brommer", "Overig"],
            "Aantal": [8450, 2340, 890, 1567, 600]
        })
        st.bar_chart(chart_data.set_index("Type"))
    with c2:
        st.subheader("Brandstof verdeling")
        fuel_data = pd.DataFrame({
            "Brandstof": ["Benzine", "Diesel", "Elektrisch", "Hybride"],
            "Aantal": [5420, 3890, 1230, 2307]
        })
        st.bar_chart(fuel_data.set_index("Brandstof"))
    
    # Recent activity
    st.subheader("📋 Recente Activiteit")
    activity = pd.DataFrame({
        "Tijd": [f"{i} min geleden" for i in range(5, 0, -1)],
        "Actie": ["APK goedgekeurd", "Kenteken vernieuwd", "Rijbewijs verlengd", "Voertuig geregistreerd", "Eigenaar gewijzigd"],
        "Locatie": ["Kralendijk", "Rincon", "Kralendijk", "Antriol", "Kralendijk"]
    })
    st.table(activity)

elif menu == "Statistieken":
    st.subheader("📈 Periodieke Statistieken")
    
    period = st.selectbox("Selecteer periode:", ["Vandaag", "Deze week", "Deze maand", "Dit jaar"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Voertuigregistraties")
        st.line_chart(pd.DataFrame({
            "Dag": ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"],
            "Nieuw": [12, 8, 15, 10, 7, 3, 2]
        }).set_index("Dag"))
    with col2:
        st.write("### Rijbewijs afgifte")
        st.line_chart(pd.DataFrame({
            "Dag": ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"],
            "Nieuw": [5, 3, 7, 4, 2, 1, 0]
        }).set_index("Dag"))

# Footer
st.markdown("---")
st.caption("🚗 RDW Bonaire Dashboard v1.0 | Caribbean Netherlands")