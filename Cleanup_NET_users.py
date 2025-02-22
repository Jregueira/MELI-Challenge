import pandas as pd

# Load the dataset (adjust the file path as needed)



df = pd.read_csv("API_IT.NET.USER.ZS_DS2_en_csv_v2_76190\API_IT.NET.USER.ZS_DS2_en_csv_v2_76190.csv", skiprows=4)
df.columns = df.columns.str.strip()
selected_countries = ["Argentina", "Uruguay", "Chile"]  # Add more countries if needed
df_filtered = df[df["Country Name"].isin(selected_countries)]

df_filtered = df_filtered.drop(columns=["Indicator Name", "Indicator Code", "Unnamed: 68"], errors="ignore")

df_argentina_melted = df_filtered.melt(id_vars=["Country Name", "Country Code"], 
                                        var_name="Year", value_name="Internet Usage (%)")

# Convert "Year" to numeric
df_argentina_melted["Year"] = pd.to_numeric(df_argentina_melted["Year"], errors="coerce")

# Sort by year
df_argentina_melted = df_argentina_melted.sort_values(by="Year")

# isplay first roDws
print(df_argentina_melted.head())
print(df_argentina_melted)


#Save the cleaned dataset (optional)
df_argentina_melted.to_csv("CSV CLEAN/Cleaned_API_IT.NET.USER.csv", index=True,  sep = ";")
