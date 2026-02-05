# test_loader.py
import sys
sys.path.insert(0, r"C:\Users\Bindu\Downloads\HCl AIML project\financial-health-platform")

from src.data_processing.loader import DataLoader

print("Starting data loader test...")

loader = DataLoader()

print("\n=== DATA SUMMARY ===")
summary = loader.get_data_summary()

print("\nMaven Data Files:")
for file, info in summary['maven_data'].items():
    status = "OK" if info.get('exists', False) else "MISSING"
    size = info.get('size_mb', 0) if info.get('exists', False) else 0
    print(f"  [{status}] {file} ({size} MB)")

sme_status = "OK" if summary['sme_data'].get('exists', False) else "MISSING"
rbi_status = "OK" if summary['rbi_benchmark'].get('exists', False) else "MISSING"

print(f"\nSME Data: [{sme_status}]")
print(f"RBI Benchmark: [{rbi_status}]")

print("\n=== LOADING DATA ===")
try:
    maven_data = loader.load_maven_data()
    print("[OK] Maven data loaded")
    
    if maven_data['sales'] is not None:
        print(f"  Sales: {maven_data['sales'].shape}")
    else:
        print("  Sales: NOT LOADED")
        
    if maven_data['products'] is not None:
        print(f"  Products: {maven_data['products'].shape}")
    else:
        print("  Products: NOT LOADED")
    
    sme_data = loader.load_kaggle_sme_data()
    print(f"[OK] SME data loaded: {sme_data.shape}")
    
    rbi_path = loader.load_rbi_benchmark_path()
    if rbi_path:
        print(f"[OK] RBI PDF found")
        print(f"     Path: {rbi_path}")
    else:
        print("[MISSING] RBI PDF not found")
    
    print("\n========================================")
    print("SUCCESS! All data loaded successfully!")
    print("========================================")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()

input("\nPress Enter to exit...")