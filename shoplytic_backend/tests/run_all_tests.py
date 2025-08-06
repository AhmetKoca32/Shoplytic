"""
Tüm Testleri Çalıştıran Ana Test Runner
"""
import sys
import os
import time
import subprocess
from datetime import datetime

# Proje root'unu Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_test_file(test_file, test_name):
    """Belirli bir test dosyasını çalıştır"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name} Testleri Başlıyor...")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Test dosyasını çalıştır
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(test_file))
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_name} testleri başarıyla tamamlandı! ({duration:.2f}s)")
            return True, duration
        else:
            print(f"❌ {test_name} testleri başarısız oldu!")
            print(f"📋 Hata Çıktısı:")
            print(result.stderr)
            return False, duration
            
    except Exception as e:
        print(f"❌ {test_name} testleri çalıştırılırken hata oluştu: {str(e)}")
        return False, 0

def run_pytest_tests():
    """Pytest ile testleri çalıştır"""
    print(f"\n{'='*60}")
    print(f"🧪 Pytest Testleri Başlıyor...")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Pytest ile tüm testleri çalıştır
        result = subprocess.run([
            "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"✅ Pytest testleri başarıyla tamamlandı! ({duration:.2f}s)")
            return True, duration
        else:
            print(f"❌ Pytest testleri başarısız oldu!")
            print(f"📋 Hata Çıktısı:")
            print(result.stderr)
            return False, duration
            
    except Exception as e:
        print(f"❌ Pytest testleri çalıştırılırken hata oluştu: {str(e)}")
        return False, 0

def run_coverage_tests():
    """Coverage ile test coverage'ını hesapla"""
    print(f"\n{'='*60}")
    print(f"📊 Test Coverage Hesaplanıyor...")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Coverage ile testleri çalıştır
        result = subprocess.run([
            "coverage", "run", "-m", "pytest", "tests/"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        
        if result.returncode == 0:
            # Coverage raporu oluştur
            report_result = subprocess.run([
                "coverage", "report", "--show-missing"
            ], capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(report_result.stdout)
            print(f"✅ Coverage raporu oluşturuldu! ({duration:.2f}s)")
            return True, duration
        else:
            print(f"❌ Coverage testleri başarısız oldu!")
            print(result.stderr)
            return False, 0
            
    except Exception as e:
        print(f"❌ Coverage testleri çalıştırılırken hata oluştu: {str(e)}")
        return False, 0

def generate_test_report(results):
    """Test raporu oluştur"""
    print(f"\n{'='*80}")
    print(f"📋 TEST RAPORU")
    print(f"{'='*80}")
    
    total_tests = len(results)
    passed_tests = sum(1 for success, _ in results if success)
    failed_tests = total_tests - passed_tests
    total_duration = sum(duration for _, duration in results)
    
    print(f"📊 Genel İstatistikler:")
    print(f"  ✅ Başarılı Testler: {passed_tests}")
    print(f"  ❌ Başarısız Testler: {failed_tests}")
    print(f"  📈 Başarı Oranı: {(passed_tests/total_tests)*100:.1f}%")
    print(f"  ⏱️  Toplam Süre: {total_duration:.2f} saniye")
    
    print(f"\n📋 Detaylı Sonuçlar:")
    for i, (success, duration) in enumerate(results):
        status = "✅ BAŞARILI" if success else "❌ BAŞARISIZ"
        print(f"  {i+1}. {status} - {duration:.2f}s")
    
    if failed_tests == 0:
        print(f"\n🎉 Tüm testler başarıyla geçti!")
        return True
    else:
        print(f"\n⚠️  {failed_tests} test başarısız oldu!")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 Shoplytic Backend Test Suite Başlıyor...")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Test Dizini: {os.path.abspath(__file__)}")
    
    # Test dosyalarını tanımla
    test_files = [
        ("test_agents.py", "AI Agent"),
        ("test_api.py", "API Endpoint"),
        ("test_ecommerce.py", "E-ticaret Entegrasyon"),
        ("test_langchain_integration.py", "LangChain Entegrasyon")
    ]
    
    results = []
    
    # Her test dosyasını çalıştır
    for test_file, test_name in test_files:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(test_path):
            success, duration = run_test_file(test_path, test_name)
            results.append((success, duration))
        else:
            print(f"⚠️  Test dosyası bulunamadı: {test_path}")
            results.append((False, 0))
    
    # Pytest testleri çalıştır
    pytest_success, pytest_duration = run_pytest_tests()
    results.append((pytest_success, pytest_duration))
    
    # Coverage testleri çalıştır (opsiyonel)
    try:
        coverage_success, coverage_duration = run_coverage_tests()
        results.append((coverage_success, coverage_duration))
    except:
        print("⚠️  Coverage testleri atlandı (coverage paketi yüklü değil)")
        results.append((True, 0))  # Coverage başarısız olsa bile ana testleri etkilemesin
    
    # Test raporu oluştur
    overall_success = generate_test_report(results)
    
    # Sonuç
    if overall_success:
        print(f"\n🎉 Tüm testler başarıyla tamamlandı!")
        return 0
    else:
        print(f"\n⚠️  Bazı testler başarısız oldu!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 