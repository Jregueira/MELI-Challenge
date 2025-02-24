import pandas as pd
import os

# Add this after your imports
if not os.path.exists("CSV CLEAN"):
    os.makedirs("CSV CLEAN")

# Function to clean up a given CSV file and add new rows for the average metric
# of all countries except Argentina under the country name "Rest of Latam"
def clean_csv(input_file, output_file, selected_countries, metric):
    # Load the dataset, skipping the first 4 rows
    df = pd.read_csv(input_file, skiprows=4)
    df.columns = df.columns.str.strip()  # Strip column names
    
    # Print columns to debug
    print(f"Columns in {input_file}:")
    print(df.columns.tolist())
    
    # Map common country column names
    country_col = None
    possible_country_cols = ['Country Name', 'Country', 'CountryName', 'Nation', 'Country/Region']
    
    for col in possible_country_cols:
        if col in df.columns:
            country_col = col
            break
    
    if country_col is None:
        raise ValueError(f"Could not find country column in {input_file}. Available columns: {df.columns.tolist()}")

    # Filter rows for the selected countries using the found column name
    df_filtered = df[df[country_col].isin(selected_countries)]
    
    # Drop unwanted columns
    df_filtered = df_filtered.drop(columns=["Indicator Name", "Indicator Code", "Unnamed: 68"], errors="ignore")
    
    # Reshape the dataframe using the found country column
    df_melted = df_filtered.melt(
        id_vars=[country_col, "Country Code"],
        var_name="Year",
        value_name=metric
    )
    
    # Rename the country column to standardize it
    df_melted = df_melted.rename(columns={country_col: "Country Name"})
    
    # Convert "Year" to numeric and sort the dataframe by Year
    df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors="coerce")
    df_melted = df_melted.sort_values(by="Year")
    
    # Compute the average of the metric for all countries except Argentina for each year
    avg_excl_arg = (
        df_melted[df_melted["Country Name"] != "Argentina"]
        .groupby("Year")[metric]
        .mean()
        .reset_index()
    )
    
    # Create new rows for each year with the computed average, using "Rest of Latam" as the country name
    avg_excl_arg["Country Name"] = "Rest of Latam"
    avg_excl_arg["Country Code"] = None  # Placeholder; adjust as needed
    # Ensure the new dataframe has the same column order as df_melted
    avg_excl_arg = avg_excl_arg[["Country Name", "Country Code", "Year", metric]]
    
    # Append the new rows to the melted dataframe
    df_final = pd.concat([df_melted, avg_excl_arg], ignore_index=True)
    
    # Display the results (optional)
    print(df_final.head())
    print(df_final)
    
    # Save the cleaned dataset with the additional entries
    df_final.to_csv(f"CSV CLEAN/{output_file}", index=True, sep=";")

# Define file paths


# Clean the fixed telephone dataset
clean_csv(
    input_file = "RawFiles/FIXED_TEL_100.csv", 
    output_file = "Cleaned_FIXED_TEL_100_norm.csv",
    selected_countries=["Argentina", "Uruguay", "Chile", "Bolivia", "Paraguay"], 
    metric="Fixed Telephone Lines"  
)

# Clean the mobile telephone dataset
clean_csv(
    input_file = "RawFiles/MOBILE_TEL_100.csv",  
    output_file = "Cleaned_MOBILE_TEL_100_norm.csv",
    selected_countries=["Argentina", "Uruguay", "Chile", "Bolivia", "Paraguay"], 
    metric="Mobile Telephone Lines"  
)

clean_csv(
    input_file = "RawFiles/API_IT.NET.USER.ZS_DS2_en_csv_v2_76190.csv",  
    output_file = "Cleaned_NET.USER_norm.csv",
    selected_countries=["Argentina", "Uruguay", "Chile", "Bolivia", "Paraguay"], 
    metric="Internet Usage (%)" 
