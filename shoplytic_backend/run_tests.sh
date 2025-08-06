#!/bin/bash

# Shoplytic Backend Test Runner Script
# Bu script tüm testleri çalıştırır ve rapor oluşturur

echo "🚀 Shoplytic Backend Test Suite Başlıyor..."
echo "📅 Tarih: $(date)"
echo "📁 Dizin: $(pwd)"
echo ""

# Python path'ini ayarla
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Test türlerini tanımla
TEST_TYPES=(
    "unit: Birim testleri"
    "api: API endpoint testleri"
    "ecommerce: E-ticaret entegrasyon testleri"
    "agents: AI Agent testleri"
    "integration: Entegrasyon testleri"
)

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test sonuçlarını sakla
declare -A test_results
declare -A test_durations

# Test çalıştırma fonksiyonu
run_test() {
    local test_type=$1
    local test_name=$2
    local test_command=$3
    
    echo -e "${BLUE}🧪 ${test_name} testleri başlıyor...${NC}"
    echo "Komut: $test_command"
    echo ""
    
    start_time=$(date +%s)
    
    if eval "$test_command"; then
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        test_results[$test_type]=true
        test_durations[$test_type]=$duration
        echo -e "${GREEN}✅ ${test_name} testleri başarıyla tamamlandı! (${duration}s)${NC}"
    else
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        test_results[$test_type]=false
        test_durations[$test_type]=$duration
        echo -e "${RED}❌ ${test_name} testleri başarısız oldu! (${duration}s)${NC}"
    fi
    
    echo ""
}

# Ana test fonksiyonu
main() {
    echo "📋 Test Türleri:"
    for test_info in "${TEST_TYPES[@]}"; do
        IFS=':' read -r test_type test_name <<< "$test_info"
        echo "  - $test_type: $test_name"
    done
    echo ""
    
    # 1. Birim testleri
    run_test "unit" "Birim" "python -m pytest tests/ -m unit -v"
    
    # 2. API testleri
    run_test "api" "API" "python -m pytest tests/ -m api -v"
    
    # 3. E-ticaret testleri
    run_test "ecommerce" "E-ticaret" "python -m pytest tests/ -m ecommerce -v"
    
    # 4. Agent testleri
    run_test "agents" "AI Agent" "python -m pytest tests/ -m agents -v"
    
    # 5. Entegrasyon testleri
    run_test "integration" "Entegrasyon" "python -m pytest tests/ -m integration -v"
    
    # 6. Tüm testler
    run_test "all" "Tüm" "python -m pytest tests/ -v"
    
    # 7. Coverage raporu
    echo -e "${BLUE}📊 Coverage raporu oluşturuluyor...${NC}"
    python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
    echo ""
    
    # Test raporu oluştur
    generate_report
}

# Test raporu oluşturma fonksiyonu
generate_report() {
    echo "="*80
    echo "📋 TEST RAPORU"
    echo "="*80
    
    total_tests=${#TEST_TYPES[@]}
    passed_tests=0
    failed_tests=0
    total_duration=0
    
    for test_type in "${!test_results[@]}"; do
        if [[ "${test_results[$test_type]}" == "true" ]]; then
            ((passed_tests++))
        else
            ((failed_tests++))
        fi
        total_duration=$((total_duration + ${test_durations[$test_type]:-0}))
    done
    
    echo "📊 Genel İstatistikler:"
    echo "  ✅ Başarılı Testler: $passed_tests"
    echo "  ❌ Başarısız Testler: $failed_tests"
    echo "  📈 Başarı Oranı: $((passed_tests * 100 / total_tests))%"
    echo "  ⏱️  Toplam Süre: ${total_duration}s"
    
    echo ""
    echo "📋 Detaylı Sonuçlar:"
    for test_info in "${TEST_TYPES[@]}"; do
        IFS=':' read -r test_type test_name <<< "$test_info"
        if [[ "${test_results[$test_type]}" == "true" ]]; then
            echo -e "  ✅ ${test_name}: ${test_durations[$test_type]}s"
        else
            echo -e "  ❌ ${test_name}: ${test_durations[$test_type]}s"
        fi
    done
    
    if [[ $failed_tests -eq 0 ]]; then
        echo ""
        echo -e "${GREEN}🎉 Tüm testler başarıyla geçti!${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}⚠️  $failed_tests test başarısız oldu!${NC}"
        exit 1
    fi
}

# Script'i çalıştır
main "$@" 