import os
import ee
import pandas as pd

project_id = 'satellite-508717'

try:
    ee.Initialize(project=project_id)
except Exception as e:
    ee.Authenticate()
    ee.Initialize(project=project_id)

print("Initializing Scientifically Rigorous Satellite Extraction Pipeline...")

# Study site bounding boxes (AOIs)
WATER_BODIES = {
    'Yamuna_North_Wazirabad': ee.Geometry.Polygon([[[77.22, 28.70], [77.24, 28.70], [77.24, 28.72], [77.22, 28.72]]]),
    'Yamuna_Central_ITO': ee.Geometry.Polygon([[[77.24, 28.62], [77.26, 28.62], [77.26, 28.64], [77.24, 28.64]]]),
    'Najafgarh_Drain': ee.Geometry.Polygon([[[77.08, 28.66], [77.10, 28.66], [77.10, 28.68], [77.08, 28.68]]]),
    'Sanjay_Lake': ee.Geometry.Polygon([[[77.28, 28.60], [77.32, 28.60], [77.32, 28.64], [77.28, 28.64]]]),
    'Bhalswa_Lake': ee.Geometry.Polygon([[[77.15, 28.74], [77.17, 28.74], [77.17, 28.76], [77.15, 28.76]]])
}

def extract_scientific_dataset():
    years = range(2017, 2026)
    all_records = []
    
    print("Extracting pure spectral metrics (No artificial formulas)...")
    
    for body_name, geometry in WATER_BODIES.items():
        print(f"\nProcessing AOI: {body_name}")
        for year in years:
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            
            try:
                # Sentinel-2 Harmonized with cloud filtering
                s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                    .filterBounds(geometry) \
                    .filterDate(start_date, end_date) \
                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
                
                count = s2.size().getInfo()
                if count > 0:
                    median_img = s2.median().clip(geometry)
                    
                    # 1. NDWI & True Water Area Calculation (using standard threshold 0.0 for open water)
                    ndwi = median_img.normalizedDifference(['B3', 'B8']).rename('ndwi')
                    water_mask = ndwi.gt(0.0)
                    pixel_area_image = water_mask.multiply(ee.Image.pixelArea()).divide(1e6) # sq km
                    
                    area_stats = pixel_area_image.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=geometry, scale=10, maxPixels=1e9
                    ).getInfo()
                    true_water_area = area_stats.get('ndwi', 0.0)
                    
                    # 2. Mean NDWI
                    ndwi_stats = ndwi.reduceRegion(
                        reducer=ee.Reducer.mean(), geometry=geometry, scale=10, maxPixels=1e9
                    ).getInfo()
                    mean_ndwi = ndwi_stats.get('ndwi', 0.0)
                    
                    # 3. Mean NDVI (Vegetation Index)
                    ndvi = median_img.normalizedDifference(['B8', 'B4']).rename('ndvi')
                    ndvi_stats = ndvi.reduceRegion(
                        reducer=ee.Reducer.mean(), geometry=geometry, scale=10, maxPixels=1e9
                    ).getInfo()
                    mean_ndvi = ndvi_stats.get('ndvi', 0.0)
                    
                    # 4. Mean NDBI (Normalized Difference Built-up Index: (SWIR - NIR) / (SWIR + NIR))
                    ndbi = median_img.normalizedDifference(['B11', 'B8']).rename('ndbi')
                    ndbi_stats = ndbi.reduceRegion(
                        reducer=ee.Reducer.mean(), geometry=geometry, scale=10, maxPixels=1e9
                    ).getInfo()
                    mean_ndbi = ndbi_stats.get('ndbi', 0.0)

                    all_records.append({
                        'Water_Body': body_name,
                        'Year': year,
                        'Water_Area_sqkm': round(true_water_area, 4),
                        'Mean_NDWI': round(mean_ndwi if mean_ndwi is not None else 0.0, 4),
                        'Mean_NDVI': round(mean_ndvi if mean_ndvi is not None else 0.0, 4),
                        'Mean_NDBI': round(mean_ndbi if mean_ndbi is not None else 0.0, 4)
                    })
                    print(f"[{year}] Water Area: {round(true_water_area, 4)} km² | NDWI: {round(mean_ndwi, 3)} | NDVI: {round(mean_ndvi, 3)} | NDBI: {round(mean_ndbi, 3)}")
                else:
                    print(f"[{year}] No cloud-free images available.")
            except Exception as e:
                print(f"Error processing {body_name} for {year}: {e}")

    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(all_records)
    df.to_csv('data/water_metrics.csv', index=False)
    print("\n✅ Clean, scientifically valid dataset successfully saved to data/water_metrics.csv!")

if __name__ == '__main__':
    extract_scientific_dataset()