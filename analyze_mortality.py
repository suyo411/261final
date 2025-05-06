import pandas as pd
import matplotlib.pyplot as plt

# 读取文件，跳过前4行 metadata
df = pd.read_csv("API_SP.DYN.IMRT.FE.IN_DS2_en_csv_v2_2253793.csv", skiprows=4)


# 显示前几行确认数据结构
print(df.head())

# 选取一个国家，比如中国
china_data = df[df["Country Name"] == "China"]

# 提取年份列（1960 到 2020）
years = [str(y) for y in range(1960, 2021)]
china_values = china_data[years].values.flatten()

# 画图
plt.plot(years, china_values)
plt.title("China Infant Female Mortality Rate (per 1000 live births)")
plt.xlabel("Year")
plt.ylabel("Mortality Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
