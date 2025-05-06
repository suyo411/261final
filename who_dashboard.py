import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="WHO Mortality Dashboard", layout="wide")
st.title("🌍 WHO Infant Female Mortality Dashboard")

# 读取并缓存数据
@st.cache_data
def load_data():
    main_df = pd.read_csv("API_SP.DYN.IMRT.FE.IN_DS2_en_csv_v2_2253793.csv", skiprows=4)
    meta_df = pd.read_csv("Metadata_Country_API_SP.DYN.IMRT.FE.IN_DS2_en_csv_v2_2253793.csv")
    merged = pd.merge(main_df, meta_df, on="Country Code")
    return merged

df = load_data()
years = [str(y) for y in range(1960, 2021)]

# 左侧筛选栏
st.sidebar.header("📊 Filter Options")
country_options = sorted(df["Country Name"].dropna().unique())
default_countries = ["China", "India", "United States"]
default_countries = [c for c in default_countries if c in country_options]
selected_countries = st.sidebar.multiselect("Select countries", options=country_options, default=default_countries)
year_range = st.sidebar.slider("Select year range", 1960, 2020, (2000, 2020))
selected_years = [str(y) for y in range(year_range[0], year_range[1]+1)]

# 国家趋势图 📈
filtered_df = df[df["Country Name"].isin(selected_countries)]
st.subheader("📈 Mortality Trend by Country")
fig1, ax1 = plt.subplots()
for country in selected_countries:
    row = filtered_df[filtered_df["Country Name"] == country]
    if not row.empty:
        ax1.plot(selected_years, row[selected_years].values.flatten(), label=country)
ax1.set_ylabel("Mortality Rate")
ax1.set_xticks(range(len(selected_years)))
ax1.set_xticklabels(selected_years, rotation=45)
ax1.legend()
st.pyplot(fig1)

# 按 Income Group 📉
st.subheader("📉 Mortality Trend by Income Group")
fig2, ax2 = plt.subplots()
for income_group in df["IncomeGroup"].dropna().unique():
    group = df[df["IncomeGroup"] == income_group]
    mean_vals = group[selected_years].mean(skipna=True)
    ax2.plot(selected_years, mean_vals, label=income_group)
ax2.set_ylabel("Mortality Rate")
ax2.set_xticks(range(len(selected_years)))
ax2.set_xticklabels(selected_years, rotation=45)
ax2.legend()
st.pyplot(fig2)

# 按 Region 🌍
st.subheader("🌎 Mortality Trend by Region")
fig3, ax3 = plt.subplots(figsize=(10, 6))
for region in df["Region"].dropna().unique():
    group = df[df["Region"] == region]
    mean_vals = group[selected_years].mean(skipna=True)
    ax3.plot(selected_years, mean_vals, label=region)
ax3.set_ylabel("Mortality Rate")
ax3.set_xticks(range(len(selected_years)))
ax3.set_xticklabels(selected_years, rotation=45)
ax3.legend(fontsize=7, ncol=2)
st.pyplot(fig3)

# 死亡率最高/最低国家 🏆
st.subheader("🏆 Country Rankings in a Specific Year")
ranking_year = st.selectbox("Select year for ranking", options=years[::-1], index=years.index("2000"))
ranking_df = df[["Country Name", ranking_year]].dropna().sort_values(by=ranking_year, ascending=False)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"🔺 Top 5 Mortality Rates in {ranking_year}")
    st.dataframe(ranking_df.head(5).reset_index(drop=True))
with col2:
    st.markdown(f"🔻 Bottom 5 Mortality Rates in {ranking_year}")
    st.dataframe(ranking_df.tail(5).reset_index(drop=True))
