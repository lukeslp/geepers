#!/bin/bash
# Census Bureau Disability Data Fetcher (Shell Script)
# Fetches ACS 1-year disability data for years 2010-2023 (excluding 2020)

set -e

# Configuration
API_KEY="56e280037b7fbf1788422653faa1cf2adf4276a7"
BASE_URL="https://api.census.gov/data"
OUTPUT_DIR="/home/coolhand/geepers/swarm/cache"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/census-disability-$TIMESTAMP.json"

# Years to fetch (excluding 2020 - no 1-year ACS)
YEARS=(2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2021 2022 2023)

# S1810 variables (Disability Characteristics)
S1810_VARS="NAME,S1810_C01_001E,S1810_C02_001E,S1810_C03_001E,S1810_C01_002E,S1810_C02_002E,S1810_C03_002E,S1810_C01_003E,S1810_C02_003E,S1810_C03_003E,S1810_C01_004E,S1810_C02_004E,S1810_C03_004E"

# B18101 variables (Disability by Age/Sex)
B18101_VARS="NAME,B18101_001E,B18101_002E,B18101_003E,B18101_004E,B18101_005E,B18101_006E,B18101_007E,B18101_008E,B18101_009E"

mkdir -p "$OUTPUT_DIR"

echo "Starting Census disability data fetch..."
echo "Output file: $OUTPUT_FILE"
echo "API Key: ${API_KEY:0:8}...${API_KEY: -8}"
echo "Years: ${YEARS[@]}"
echo ""

# Initialize JSON structure
{
  echo "{"
  echo "  \"metadata\": {"
  echo "    \"fetched_at\": \"$(date -Iseconds)\","
  echo "    \"api_key_masked\": \"${API_KEY:0:8}...${API_KEY: -8}\","
  echo "    \"years_requested\": ${YEARS[@]}"
  echo "  },"
  echo "  \"s1810_data\": {"
} > "$OUTPUT_FILE"

# Fetch S1810 data for each year
first_year=true
for year in "${YEARS[@]}"; do
  echo "Fetching S1810 for $year..."

  if ! $first_year; then
    echo "," >> "$OUTPUT_FILE"
  fi
  first_year=false

  # Fetch data
  response=$(curl -s "${BASE_URL}/${year}/acs/acs1/subject?get=${S1810_VARS}&for=us:*&key=${API_KEY}")

  # Format as JSON
  echo "    \"${year}\": {" >> "$OUTPUT_FILE"
  echo "      \"year\": $year," >> "$OUTPUT_FILE"
  echo "      \"table\": \"S1810\"," >> "$OUTPUT_FILE"
  echo "      \"fetched_at\": \"$(date -Iseconds)\"," >> "$OUTPUT_FILE"
  echo "      \"data\": $(echo "$response" | sed 's/^/        /')" >> "$OUTPUT_FILE"
  echo "    }" >> "$OUTPUT_FILE"
done

echo "" >> "$OUTPUT_FILE"
echo "  }," >> "$OUTPUT_FILE"
echo "  \"b18101_data\": {" >> "$OUTPUT_FILE"

# Fetch B18101 data for each year
first_year=true
for year in "${YEARS[@]}"; do
  echo "Fetching B18101 for $year..."

  if ! $first_year; then
    echo "," >> "$OUTPUT_FILE"
  fi
  first_year=false

  # Fetch data
  response=$(curl -s "${BASE_URL}/${year}/acs/acs1?get=${B18101_VARS}&for=us:*&key=${API_KEY}")

  # Format as JSON
  echo "    \"${year}\": {" >> "$OUTPUT_FILE"
  echo "      \"year\": $year," >> "$OUTPUT_FILE"
  echo "      \"table\": \"B18101\"," >> "$OUTPUT_FILE"
  echo "      \"fetched_at\": \"$(date -Iseconds)\"," >> "$OUTPUT_FILE"
  echo "      \"data\": $(echo "$response" | sed 's/^/        /')" >> "$OUTPUT_FILE"
  echo "    }" >> "$OUTPUT_FILE"
done

echo "" >> "$OUTPUT_FILE"
echo "  }," >> "$OUTPUT_FILE"
echo "  \"summary\": {" >> "$OUTPUT_FILE"
echo "    \"years_targeted\": ${#YEARS[@]}," >> "$OUTPUT_FILE"
echo "    \"fetch_date\": \"$(date)\"" >> "$OUTPUT_FILE"
echo "  }" >> "$OUTPUT_FILE"
echo "}" >> "$OUTPUT_FILE"

echo ""
echo "Fetch complete. Results saved to:"
echo "$OUTPUT_FILE"
echo ""
echo "File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
