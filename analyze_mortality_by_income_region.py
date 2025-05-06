import pandas as pd
import matplotlib.pyplot as plt

# === 读取数据 ===
main_df = pd.read_csv("API_SP.DYN.IMRT.FE.IN_DS2_en_csv_v2_2253793.csv", skiprows=4)
meta_df = pd.read_csv("Metadata_Country_API_SP.DYN.IMRT.FE.IN_DS2_en_csv_v2_2253793.csv")

# === 合并主数据与国家元数据 ===
merged_df = pd.merge(main_df, meta_df, on="Country Code")

# === 设定年份 ===
years = [str(y) for y in range(1960, 2021)]

# ==========================================
# 1. 按 IncomeGroup 分组画出平均趋势图
# ==========================================
plt.figure(figsize=(10, 6))
for income in merged_df["IncomeGroup"].dropna().unique():
    group = merged_df[merged_df["IncomeGroup"] == income]
    avg = group[years].mean(skipna=True)
    plt.plot(years, avg, label=income)

plt.title("📈 Infant Female Mortality Rate by Income Group")
plt.xlabel("Year")
plt.ylabel("Mortality Rate (per 1000 live births)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# ==========================================
# 2. 按 Region 分组画出平均趋势图
# ==========================================
plt.figure(figsize=(12, 6))
for region in merged_df["Region"].dropna().unique():
    group = merged_df[merged_df["Region"] == region]
    avg = group[years].mean(skipna=True)
    plt.plot(years, avg, label=region)

plt.title("🌍 Infant Female Mortality Rate by Region")
plt.xlabel("Year")
plt.ylabel("Mortality Rate (per 1000 live births)")
plt.legend(fontsize=7, ncol=2)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# ==========================================
#  3. 某一年死亡率最高/最低的国家（示例：1990年）
# ==========================================
target_year = "1990"
top_n = 10

df_1990 = merged_df[["Country Name", target_year]].dropna()
df_1990 = df_1990.sort_values(by=target_year, ascending=False)

print(f"\n🏆 {target_year} 年死亡率最高的前 {top_n} 个国家：")
print(df_1990.head(top_n).to_string(index=False))

print(f"\n✅ {target_year} 年死亡率最低的前 {top_n} 个国家：")
print(df_1990.tail(top_n).to_string(index=False))
