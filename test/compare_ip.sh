#!/bin/bash

# Load required environment
. ssmuse-sh -x rpn/utils/20220408

echo "=== Testing IP Encoding/Decoding ==="
echo "Height values (kind=0):"
echo "5m above sea level:"
echo "  Encode: $(r.ip1 -o 5.0 0)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 5.0 0))"
echo "1000m above sea level:"
echo "  Encode: $(r.ip1 -o 1000.0 0)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 1000.0 0))"
echo "2000m above sea level:"
echo "  Encode: $(r.ip1 -o 2000.0 0)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 2000.0 0))"
echo

echo "Sigma values (kind=1):"
echo "Sigma 0.0:"
echo "  Encode: $(r.ip1 -o 0.0 1)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 0.0 1))"
echo "Sigma 0.5:"
echo "  Encode: $(r.ip1 -o 0.5 1)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 0.5 1))"
echo "Sigma 1.0:"
echo "  Encode: $(r.ip1 -o 1.0 1)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 1.0 1))"
echo

echo "Pressure values (kind=2):"
echo "Surface pressure (1013.0 mb):"
echo "  Encode: $(r.ip1 -o 1013.0 2)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 1013.0 2))"
echo "850 mb level:"
echo "  Encode: $(r.ip1 -o 850.0 2)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 850.0 2))"
echo "0.5 mb level:"
echo "  Encode: $(r.ip1 -o 0.5 2)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 0.5 2))"
echo

echo "Hybrid values (kind=5):"
echo "Hybrid 0.0:"
echo "  Encode: $(r.ip1 -o 0.0 5)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 0.0 5))"
echo "Hybrid 0.5:"
echo "  Encode: $(r.ip1 -o 0.5 5)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 0.5 5))"
echo "Hybrid 1.0:"
echo "  Encode: $(r.ip1 -o 1.0 5)"
echo "  Decode: $(r.ip1 $(r.ip1 -o 1.0 5))"
echo

echo "=== Testing Height Range (12000 < ip <= 32000) ==="
echo "Edge cases and boundaries:"
echo "12000: $(r.ip1 12000)"  # Just below valid range
echo "12001: $(r.ip1 12001)"  # First valid value
echo "12002: $(r.ip1 12002)"  # Second value
echo "31998: $(r.ip1 31998)"  # Near maximum
echo "31999: $(r.ip1 31999)"  # Second to last value
echo "32000: $(r.ip1 32000)"  # Maximum value
echo "32001: $(r.ip1 32001)"  # Just above valid range
echo
echo "Sample values:"
echo "15000: $(r.ip1 15000)"  # ~15km
echo "20000: $(r.ip1 20000)"  # ~40km
echo "25000: $(r.ip1 25000)"  # ~65km
echo "30000: $(r.ip1 30000)"  # ~90km
echo

echo "=== Testing Sigma Range (2000 <= ip <= 12000) ==="
echo "Edge cases and boundaries:"
echo "1999: $(r.ip1 1999)"    # Just below valid range
echo "2000: $(r.ip1 2000)"    # Minimum value (0.0)
echo "2001: $(r.ip1 2001)"    # Second value (0.0001)
echo "2010: $(r.ip1 2010)"    # 0.001
echo "11990: $(r.ip1 11990)"  # 0.999
echo "11999: $(r.ip1 11999)"  # Second to last value (0.9999)
echo "12000: $(r.ip1 12000)"  # Maximum value (1.0)
echo "12001: $(r.ip1 12001)"  # Just above valid range
echo

echo "=== Testing Pressure Range (0 <= ip < 1100) ==="
echo "Edge cases and boundaries:"
echo "-1: $(r.ip1 -1)"      # Just below valid range
echo "0: $(r.ip1 0)"        # Minimum value
echo "1: $(r.ip1 1)"        # Second value
echo "1097: $(r.ip1 1097)"  # Near maximum
echo "1098: $(r.ip1 1098)"  # Second to last value
echo "1099: $(r.ip1 1099)"  # Maximum value
echo "1100: $(r.ip1 1100)"  # Just above valid range
echo
echo "Common meteorological levels:"
echo "1013: $(r.ip1 1013)"    # Standard surface pressure
echo "850: $(r.ip1 850)"      # 850mb level
echo "700: $(r.ip1 700)"      # 700mb level
echo "500: $(r.ip1 500)"      # 500mb level
echo "250: $(r.ip1 250)"      # 250mb level
echo "100: $(r.ip1 100)"      # 100mb level
echo "10: $(r.ip1 10)"        # 10mb level
echo "1: $(r.ip1 1)"          # 1mb level
echo

echo "=== Testing Complex Pressure Range (1200 < ip < 2000) ==="
echo "Edge cases and boundaries:"
echo "1200: $(r.ip1 1200)"  # Just below valid range
echo "1201: $(r.ip1 1201)"  # First valid value
echo
echo "Subrange boundaries:"
echo "1399: $(r.ip1 1399)"  # End of first subrange
echo "1400: $(r.ip1 1400)"  # Start of second subrange
echo "1599: $(r.ip1 1599)"  # End of second subrange
echo "1600: $(r.ip1 1600)"  # Start of third subrange
echo "1799: $(r.ip1 1799)"  # End of third subrange
echo "1800: $(r.ip1 1800)"  # Start of fourth subrange
echo "1999: $(r.ip1 1999)"  # Last valid value
echo "2000: $(r.ip1 2000)"  # Just above valid range
echo
echo "Sample values in each subrange:"
echo "1300: $(r.ip1 1300)"  # First subrange (divide by 20000)
echo "1500: $(r.ip1 1500)"  # Second subrange (divide by 2000)
echo "1700: $(r.ip1 1700)"  # Third subrange (divide by 200)
echo "1900: $(r.ip1 1900)"  # Fourth subrange (divide by 20)
echo

echo "=== Testing Newstyle IP Values ==="
echo "Testing newstyle height values:"
echo "5m above sea level:"
echo "  Encode: $(r.ip1 -n 5.0 0)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 5.0 0))"
echo "1000m above sea level:"
echo "  Encode: $(r.ip1 -n 1000.0 0)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 1000.0 0))"
echo "2000m above sea level:"
echo "  Encode: $(r.ip1 -n 2000.0 0)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 2000.0 0))"
echo

echo "Testing newstyle sigma values:"
echo "Sigma 0.0:"
echo "  Encode: $(r.ip1 -n 0.0 1)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 0.0 1))"
echo "Sigma 0.5:"
echo "  Encode: $(r.ip1 -n 0.5 1)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 0.5 1))"
echo "Sigma 1.0:"
echo "  Encode: $(r.ip1 -n 1.0 1)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 1.0 1))"
echo

echo "Testing newstyle pressure values:"
echo "Surface pressure (1013.0 mb):"
echo "  Encode: $(r.ip1 -n 1013.0 2)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 1013.0 2))"
echo "850 mb level:"
echo "  Encode: $(r.ip1 -n 850.0 2)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 850.0 2))"
echo "0.5 mb level:"
echo "  Encode: $(r.ip1 -n 0.5 2)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 0.5 2))"
echo

echo "Testing newstyle hybrid values:"
echo "Hybrid 0.0:"
echo "  Encode: $(r.ip1 -n 0.0 5)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 0.0 5))"
echo "Hybrid 0.5:"
echo "  Encode: $(r.ip1 -n 0.5 5)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 0.5 5))"
echo "Hybrid 1.0:"
echo "  Encode: $(r.ip1 -n 1.0 5)"
echo "  Decode: $(r.ip1 $(r.ip1 -n 1.0 5))"
echo

# Function to test a single IP value
test_ip() {
    local ip=$1
    echo "Testing IP: $ip"
    echo "r.ip1 output:"
    r.ip1 $ip
    echo "----------------------------------------"
}

echo "=== Testing Additional Basic Pressure Values ==="
test_ip 0
test_ip 10
test_ip 20
test_ip 30
test_ip 40
echo

echo "=== Testing Additional Special Range Values ==="
for ip in {1174..1199}; do
    test_ip $ip
done
echo

echo "=== Testing Additional New-Style Encoded Values ==="
test_ip 58820256
test_ip 58830256
test_ip 58840256
test_ip 59868832
test_ip 59968832
test_ip 60068832
test_ip 60168832
test_ip 60268832
test_ip 60368832
test_ip 66060288 
