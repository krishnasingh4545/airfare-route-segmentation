import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Airfare Route Segment Explorer",
    page_icon="plane",
    layout="wide"
)

@st.cache_data
def load_data():
    base = "data/"
    eco_clust = pd.read_csv(base + "economy_with_clusters.csv", index_col=0)
    biz_clust = pd.read_csv(base + "business_with_clusters.csv", index_col=0)
    eco_curves = pd.read_csv(base + "price_curves_economy.csv")
    biz_curves = pd.read_csv(base + "price_curves_business.csv")
    return eco_clust, biz_clust, eco_curves, biz_curves

eco_clust, biz_clust, eco_curves, biz_curves = load_data()

st.title("Airfare Route Segment Explorer")
st.markdown("Explore pricing behaviour segments for 30 Indian domestic airfare routes.")

st.sidebar.header("Select a Route")
travel_class = st.sidebar.radio("Class", ["Economy", "Business"])

if travel_class == "Economy":
    cluster_df = eco_clust
    curves_df = eco_curves
else:
    cluster_df = biz_clust
    curves_df = biz_curves

route = st.sidebar.selectbox("Route", sorted(cluster_df.index.tolist()))

row = cluster_df.loc[route]
segment = row["segment"]

st.subheader(f"{route} ({travel_class})")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Segment", segment)
col2.metric("Mean Price", "Rs." + format(int(row["mean_price"]), ","))
col3.metric("Last-Minute Premium", "{:.2f}x".format(row["last_minute_premium"]))
col4.metric("Volatility (CV)", "{:.2f}".format(row["cv_price"]))

st.subheader("Price Trajectory")
route_curve = curves_df[curves_df["route"] == route].sort_values("days_left")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(route_curve["days_left"], route_curve["mean_price"], linewidth=2.5, color="#3498db")
ax.set_xlabel("Days Before Departure")
ax.set_ylabel("Average Price (INR)")
ax.set_title(route + " - Price vs Days to Departure")
ax.grid(True, alpha=0.4)
st.pyplot(fig)

st.subheader("Comparison to Segment Average")
segment_routes = cluster_df[cluster_df["segment"] == segment]
comparison = pd.DataFrame({
    "This Route": [row["mean_price"], row["last_minute_premium"], row["cv_price"]],
    "Segment Average": [
        segment_routes["mean_price"].mean(),
        segment_routes["last_minute_premium"].mean(),
        segment_routes["cv_price"].mean()
    ]
}, index=["Mean Price (Rs.)", "Last-Minute Premium (x)", "Volatility (CV)"])
st.dataframe(comparison.round(2))

st.subheader("Booking Recommendation")
premium = row["last_minute_premium"]
if premium > 2.8:
    st.error("Book EARLY. This route charges " + "{:.2f}".format(premium) + "x more for last-minute bookings.")
elif premium > 2.3:
    st.warning("Book a few weeks ahead. Last-minute premium is " + "{:.2f}".format(premium) + "x.")
else:
    st.success("Flexible. Last-minute premium is only " + "{:.2f}".format(premium) + "x.")

st.markdown("---")
st.markdown("Built as part of the Airfare Route Segmentation project. [View on GitHub](https://github.com/krishnasingh4545/airfare-route-segmentation)")
