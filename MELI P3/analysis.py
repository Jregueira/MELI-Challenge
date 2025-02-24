import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('MELI P3/productos_ml.csv')

def analyze_streaming_devices():
    # 1. Basic statistics by product category
    def get_product_stats():
        stats = df.groupby('search_term').agg({
            'price': ['count', 'mean', 'min', 'max', 'std'],
            'shipping_free': 'mean'
        })
        print("\n=== Product Category Statistics ===")
        print(stats)
        
        # Visualize price distribution by product
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='search_term', y='price', data=df)
        plt.title('Price Distribution by Product Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('price_distribution.png')
        plt.close()

    # 2. Analyze product conditions
    def analyze_conditions():
        condition_stats = df.groupby(['search_term', 'condition']).size().unstack(fill_value=0)
        print("\n=== Product Condition Distribution ===")
        print(condition_stats)
        
        # Visualize condition distribution
        condition_stats.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Product Condition Distribution by Category')
        plt.tight_layout()
        plt.savefig('condition_distribution.png')
        plt.close()

    # 3. Warranty analysis
    def analyze_warranty():
        # Extract warranty duration 
        df['warranty_duration'] = df['warranty'].str.extract('(\d+)').astype(float)
        
        warranty_stats = df.groupby('search_term')['warranty_duration'].agg(['mean', 'median'])
        print("\n=== Warranty Duration Statistics (in months) ===")
        print(warranty_stats)

   
    # 4. Price range analysis
    def analyze_price_ranges():
        # Create price ranges
        df['price_range'] = pd.qcut(df['price'], q=4, labels=['Budget', 'Mid-Low', 'Mid-High', 'Premium'])
        
        price_range_dist = df.groupby(['search_term', 'price_range']).size().unstack()
        print("\n=== Price Range Distribution ===")
        print(price_range_dist)
        
        # Visualize price ranges
        price_range_dist.plot(kind='bar', stacked=True, figsize=(10, 6))
        plt.title('Price Range Distribution by Product Category')
        plt.tight_layout()
        plt.savefig('price_ranges.png')
        plt.close()

    # Run all analyses
    get_product_stats()
    analyze_conditions()
    analyze_warranty()
    analyze_price_ranges()

if __name__ == "__main__":
    analyze_streaming_devices() 