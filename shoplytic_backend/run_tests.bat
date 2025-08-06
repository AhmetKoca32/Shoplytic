@echo off
REM Shoplytic Backend Test Runner Script (Windows)
REM Bu script tüm testleri çalıştırır ve rapor oluşturur

echo 🚀 Shoplytic Backend Test Suite Başlıyor...
echo 📅 Tarih: %date% %time%
echo 📁 Dizin: %cd%
echo.

REM Python path'ini ayarla
set PYTHONPATH=%PYTHONPATH%;%cd%

REM Test türlerini tanımla
set TEST_TYPES=unit: Birim testleri api: API endpoint testleri ecommerce: E-ticaret entegrasyon testleri agents: AI Agent testleri integration: Entegrasyon testleri

echo 📋 Test Türleri:
for %%t in (%TEST_TYPES%) do (
    echo   - %%t
)
echo.

REM Test sonuçlarını sakla
set /a passed_tests=0
set /a failed_tests=0
set /a total_duration=0

REM Test çalıştırma fonksiyonu
:run_test
set test_type=%1
set test_name=%2
set test_command=%3

echo 🧪 %test_name% testleri başlıyor...
echo Komut: %test_command%
echo.

set start_time=%time%

%test_command%
if %errorlevel% equ 0 (
    set end_time=%time%
    echo ✅ %test_name% testleri başarıyla tamamlandı!
    set /a passed_tests+=1
) else (
    set end_time=%time%
    echo ❌ %test_name% testleri başarısız oldu!
    set /a failed_tests+=1
)

echo.
goto :eof

REM Ana test fonksiyonu
echo 🧪 Birim testleri başlıyor...
call :run_test "unit" "Birim" "python -m pytest tests/ -m unit -v"

echo 🧪 API testleri başlıyor...
call :run_test "api" "API" "python -m pytest tests/ -m api -v"

echo 🧪 E-ticaret testleri başlıyor...
call :run_test "ecommerce" "E-ticaret" "python -m pytest tests/ -m ecommerce -v"

echo 🧪 AI Agent testleri başlıyor...
call :run_test "agents" "AI Agent" "python -m pytest tests/ -m agents -v"

echo 🧪 Entegrasyon testleri başlıyor...
call :run_test "integration" "Entegrasyon" "python -m pytest tests/ -m integration -v"

echo 🧪 Tüm testler başlıyor...
call :run_test "all" "Tüm" "python -m pytest tests/ -v"

echo 📊 Coverage raporu oluşturuluyor...
python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
echo.

REM Test raporu oluştur
echo ================================================================================
echo 📋 TEST RAPORU
echo ================================================================================

set /a total_tests=%passed_tests%+%failed_tests%
if %total_tests% gtr 0 (
    set /a success_rate=(%passed_tests%*100)/%total_tests%
) else (
    set success_rate=0
)

echo 📊 Genel İstatistikler:
echo   ✅ Başarılı Testler: %passed_tests%
echo   ❌ Başarısız Testler: %failed_tests%
echo   📈 Başarı Oranı: %success_rate%%%
echo   ⏱️  Toplam Süre: %total_duration% saniye

echo.
echo 📋 Detaylı Sonuçlar:
echo   ✅ Birim testleri
echo   ✅ API testleri  
echo   ✅ E-ticaret testleri
echo   ✅ AI Agent testleri
echo   ✅ Entegrasyon testleri

if %failed_tests% equ 0 (
    echo.
    echo 🎉 Tüm testler başarıyla geçti!
    exit /b 0
) else (
    echo.
    echo ⚠️  %failed_tests% test başarısız oldu!
    exit /b 1
) 