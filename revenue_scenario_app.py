import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="📊 Credit Revenue Scenarios", layout="wide")
st.title("💰 Προβολή Εσόδων ανά Σενάριο Credits")

st.markdown("""
Αυτό το διαδραστικό εργαλείο συγκρίνει 4 διαφορετικά σενάρια μονεταριοποίησης με credits,
λαμβάνοντας υπόψιν τιμές, δωρεάν μονάδες και ποσοστά μετατροπής.
""")

# Base settings
base_traffic = 1000
growth_rate = 0.10
searches_per_user = 5
months = pd.date_range(start=pd.Timestamp.today().replace(day=1) + pd.DateOffset(months=1),
                       periods=12, freq='MS').strftime('%b %Y')

# Scenario definitions
scenarios = {
    "Scenario 1 (€0.60)": {
        "avg_price": 0.60,
        "free_credits": 2,
        "extra_credits": 0,
        "conversion": {
            "signup": 0.20,
            "profile": 0.50,
            "search": 0.80,
            "limit": 0.65,
            "purchase": 0.20
        }
    },
    "Scenario 2 (€0.70)": {
        "avg_price": 0.70,
        "free_credits": 2,
        "extra_credits": 1,
        "conversion": {
            "signup": 0.22,
            "profile": 0.60,
            "search": 0.85,
            "limit": 0.50,
            "purchase": 0.15
        }
    },
    "Scenario 3 (€0.50)": {
        "avg_price": 0.50,
        "free_credits": 1,
        "extra_credits": 0,
        "conversion": {
            "signup": 0.25,
            "profile": 0.45,
            "search": 0.85,
            "limit": 0.70,
            "purchase": 0.25
        }
    },
    "Scenario 4 (€1.00 + Δώρα)": {
        "avg_price": 1.00 * 0.77,  # gift effect
        "free_credits": 2,
        "extra_credits": 1,
        "conversion": {
            "signup": 0.18,
            "profile": 0.55,
            "search": 0.75,
            "limit": 0.60,
            "purchase": 0.18
        }
    }
}

# Display conversion rates table
conversion_data = []
for name, config in scenarios.items():
    row = {
        "Σενάριο": name,
        "% Εγγραφή": f"{config['conversion']['signup']*100:.0f}%",
        "% Συμπλ. Προφίλ": f"{config['conversion']['profile']*100:.0f}%",
        "% Κάνουν Αναζήτηση": f"{config['conversion']['search']*100:.0f}%",
        "% Φτάνουν στο Όριο": f"{config['conversion']['limit']*100:.0f}%",
        "% Αγοράζουν": f"{config['conversion']['purchase']*100:.0f}%"
    }
    conversion_data.append(row)

conversion_df = pd.DataFrame(conversion_data)
st.subheader("📋 Ποσοστά Μετατροπών ανά Σενάριο")
st.dataframe(conversion_df, use_container_width=True)

fig = go.Figure()
summary_table = []

for name, config in scenarios.items():
    revenue_series = []
    traffic = base_traffic
    total_revenue = 0

    for _ in months:
        c = config['conversion']
        signups = traffic * c['signup']
        profiles = signups * c['profile']
        searches = profiles * c['search']
        limited = searches * c['limit']
        buyers = limited * c['purchase']

        total_credits = buyers * searches_per_user
        free = buyers * (config['free_credits'] + config['extra_credits'])
        paid_credits = max(total_credits - free, 0)
        revenue = paid_credits * config['avg_price']
        revenue_series.append(revenue)

        total_revenue += revenue
        traffic *= (1 + growth_rate)

    fig.add_trace(go.Scatter(x=months, y=revenue_series, mode='lines+markers', name=name))
    summary_table.append({"Σενάριο": name, "Ετήσια Έσοδα (€)": round(total_revenue, 2)})

# Chart rendering
st.plotly_chart(fig, use_container_width=True)

# Summary table
summary_df = pd.DataFrame(summary_table)
st.subheader("📌 Σύγκριση Ετήσιων Εσόδων")
st.dataframe(summary_df, use_container_width=True)

st.markdown("""
🔄 Τα δεδομένα βασίζονται σε εκτιμήσεις με πιθανότητες μετατροπής σε κάθε βήμα χρήσης,
και μπορούν να προσαρμοστούν για πιο ρεαλιστική ανάλυση αν μας δοθούν νέα insights.
""")


