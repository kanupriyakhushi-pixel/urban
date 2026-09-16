import pandas as pd
import os

def prepare_temporal_features():
    # Load satellite-derived dataset
    if not os.path.exists('data/water_metrics.csv'):
        print("Error: data/water_metrics.csv not found! Please run water_detection.py first.")
        return

    df = pd.read_csv('data/water_metrics.csv')

    # Dynamically map columns based on what's actually in the CSV
    area_col = next((c for c in ['Water_Area_sqkm', 'Water_Area'] if c in df.columns), None)
    ndwi_col = next((c for c in ['Mean_NDWI', 'NDWI'] if c in df.columns), None)
    ndvi_col = next((c for c in ['Mean_NDVI', 'NDVI'] if c in df.columns), None)
    ndbi_col = next((c for c in ['Mean_NDBI', 'NDBI', 'Built_up_%'] if c in df.columns), None)

    if not area_col:
        print("Error: Could not find water area column in CSV.")
        return

    # Sort by water body and year
    df = df.sort_values(['Water_Body', 'Year']).reset_index(drop=True)

    # Previous year's water area
    df['Previous_Water_Area'] = df.groupby('Water_Body')[area_col].shift(1)

    # Water area change percentage
    df['Water_Area_Change_%'] = (
        (df[area_col] - df['Previous_Water_Area']) / df['Previous_Water_Area']
    ) * 100

    # Year-to-year changes for available spectral indices
    if ndwi_col:
        df['NDWI_Change'] = df.groupby('Water_Body')[ndwi_col].diff()
    if ndvi_col:
        df['NDVI_Change'] = df.groupby('Water_Body')[ndvi_col].diff()
    if ndbi_col:
        df['NDBI_Change'] = df.groupby('Water_Body')[ndbi_col].diff()

    # Save processed dataset
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/water_metrics_temporal.csv', index=False)

    print("Temporal feature dataset created successfully!")
    print("Saved at: data/water_metrics_temporal.csv")

    # Print largest water drop for research inspection (Fixed syntax here)
    if 'Water_Area_Change_%' in df.columns and not df['Water_Area_Change_%'].isna().all():
        max_drop = df.loc[df['Water_Area_Change_%'].idxmin()]
        print("\n🚨 Largest Recorded Water Area Drop:")
        print(max_drop[['Water_Body', 'Year', area_col, 'Previous_Water_Area', 'Water_Area_Change_%']])

    print("\nDataset preview:")
    print(df.head(10))

if __name__ == '__main__':
    prepare_temporal_features()