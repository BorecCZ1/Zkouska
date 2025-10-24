#!/bin/bash
# Demo skript pro ukázku interaktivního režimu

echo "========================================="
echo "UKÁZKA INTERAKTIVNÍHO REŽIMU"
echo "========================================="
echo ""
echo "Spouštím: python3 main.py"
echo "Používám výchozí soubor (stisknu Enter)"
echo ""
echo "" | python3 main.py 2>&1 | head -30
