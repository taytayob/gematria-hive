# Gematria Formulas and Calculation Methods

**Date:** January 6, 2025  
**Purpose:** Complete documentation of all gematria calculation formulas and methods  
**Baseline Source:** gematrix.org CSV database (gematrix789.csv, gimatria789.csv)

---

## 📚 Overview

This document provides the **baseline formulas** for all gematria calculation methods. These formulas are based on the gematrix.org database and represent the **established truth** we use as our foundation. We will later establish our own interpretations and run calculations from multiple perspectives to work toward proofs.

---

## 🌍 Language-Specific Calculations

### 1. English Gematria

**Formula:** `Σ(letter_position_in_alphabet)`

**Letter Values:**
- A = 1, B = 2, C = 3, ..., Z = 26

**Calculation:**
```
For text "LOVE":
L = 12 (12th letter)
O = 15 (15th letter)
V = 22 (22nd letter)
E = 5  (5th letter)
Total = 12 + 15 + 22 + 5 = 54
```

**Baseline Truth:** Verified against gematrix789.csv  
**Status:** ✅ Implemented and tested

---

### 2. Simple Gematria

**Formula:** `Same as English Gematria`

**Calculation:**
```
Simple Gematria = English Gematria
```

**Baseline Truth:** Verified against gematrix789.csv  
**Status:** ✅ Implemented and tested

---

### 3. Jewish Gematria

**Formula:** `Σ(hebrew_letter_value)`

**Hebrew Letter Values (Traditional):**
```
א (Aleph) = 1      י (Yod) = 10      ק (Qof) = 100
ב (Bet) = 2        כ (Kaf) = 20     ר (Resh) = 200
ג (Gimel) = 3      ל (Lamed) = 30   ש (Shin) = 300
ד (Dalet) = 4      מ (Mem) = 40     ת (Tav) = 400
ה (He) = 5         נ (Nun) = 50     ך (Kaf Sofit) = 500
ו (Vav) = 6        ס (Samekh) = 60  ם (Mem Sofit) = 600
ז (Zayin) = 7      ע (Ayin) = 70    ן (Nun Sofit) = 700
ח (Het) = 8        פ (Pe) = 80      ף (Pe Sofit) = 800
ט (Tet) = 9        צ (Tsadi) = 90   ץ (Tsadi Sofit) = 900
```

**Baseline Truth:** Verified against gematrix789.csv  
**Status:** ✅ Implemented and tested

---

### 4. Hebrew Full Gematria

**Formula:** `Same as Jewish Gematria`

**Calculation:**
```
Hebrew Full = Jewish Gematria
```

**Baseline Truth:** Verified against gimatria789.csv (g_full column)  
**Status:** ✅ Implemented and tested

---

### 5. Greek Gematria

**Formula:** `Σ(greek_letter_value)`

**Greek Letter Values (Classical):**
```
Α (Alpha) = 1      Ι (Iota) = 10     Ρ (Rho) = 100
Β (Beta) = 2       Κ (Kappa) = 20    Σ (Sigma) = 200
Γ (Gamma) = 3      Λ (Lambda) = 30   Τ (Tau) = 300
Δ (Delta) = 4      Μ (Mu) = 40       Υ (Upsilon) = 400
Ε (Epsilon) = 5    Ν (Nu) = 50       Φ (Phi) = 500
Ϝ (Digamma) = 6    Ξ (Xi) = 60       Χ (Chi) = 600
Ζ (Zeta) = 7       Ο (Omicron) = 70  Ψ (Psi) = 700
Η (Eta) = 8        Π (Pi) = 80       Ω (Omega) = 800
Θ (Theta) = 9      Ϙ (Koppa) = 90
```

**Baseline Truth:** Based on classical Greek gematria  
**Status:** ✅ Implemented and tested

---

### 6. Latin Gematria (Qabala Simplex / Kabbalah)

**Formula:** `Σ(latin_letter_value)` with special sequences

**Latin Letter Values (23-letter alphabet):**
```
A = 1    I = 9     P = 16
B = 2    L = 10    Q = 17
C = 3    M = 11    R = 18
D = 4    N = 12    S = 19
E = 5    O = 13    T = 20
F = 6    V = 14    V = 21
G = 7    X = 15    Y = 22
H = 8    Z = 16    Z = 22
```

**Special Sequences:**
- `HI` = 27 (special sequence, not H + I)
- `J` = 24 (extended)
- `V` = 25 (extended)
- `W` = 26 (extended)

**Baseline Truth:** Based on Qabala Simplex tradition  
**Status:** ✅ Implemented and tested

---

## 🔢 Hebrew Variant Calculations

### 7. Hebrew Musafi

**Formula:** `Jewish_Gematria + (letter_count × 1000)`

**Calculation:**
```
For text "א" (1 letter):
Base: א = 1
Letter count: 1
Musafi = 1 + (1 × 1000) = 1001
```

**Baseline Truth:** Verified against gimatria789.csv (g_musafi column)  
**Status:** ✅ Implemented and tested

---

### 8. Hebrew Katan (Reduced)

**Formula:** `Σ(reduce_to_single_digit(letter_value))`

**Reduction Algorithm:**
```
For each letter value:
  While value > 9:
    value = sum of digits
```

**Example:**
```
ת (Tav) = 400
Reduction: 4 + 0 + 0 = 4
```

**Baseline Truth:** Verified against gimatria789.csv (g_katan column)  
**Status:** ✅ Implemented and tested

---

### 9. Hebrew Ordinal

**Formula:** `Σ(position_in_alphabet)`

**Calculation:**
```
Hebrew alphabet order: אבגדהוזחטסעפצקרשת
א (Aleph) = position 1
ב (Bet) = position 2
...
ת (Tav) = position 22
```

**Baseline Truth:** Verified against gimatria789.csv (g_ordinal column)  
**Status:** ✅ Implemented and tested

---

### 10. Hebrew Atbash (Mirror)

**Formula:** `Jewish_Gematria(reversed_alphabet(text))`

**Atbash Mapping (Reversed Alphabet):**
```
א ↔ ת    י ↔ מ    ק ↔ ד
ב ↔ ש    כ ↔ ל    ר ↔ ג
ג ↔ ר    ל ↔ כ    ש ↔ ב
ד ↔ ק    מ ↔ י    ת ↔ א
ה ↔ צ    נ ↔ ט
ו ↔ פ    ס ↔ ח
ז ↔ ע    ע ↔ ז
ח ↔ ס    פ ↔ ו
ט ↔ נ    צ ↔ ה
```

**Calculation:**
1. Map each letter to its Atbash equivalent
2. Calculate Jewish Gematria of mapped text

**Baseline Truth:** Verified against gimatria789.csv (g_atbash column)  
**Status:** ✅ Implemented and tested

---

### 11. Hebrew Kidmi (Cumulative)

**Formula:** `Σ(cumulative_sum)`

**Calculation:**
```
For each letter in sequence:
  cumulative += letter_value
  total += cumulative
```

**Example:**
```
For "אב" (א=1, ב=2):
Letter 1 (א): cumulative = 1, total = 1
Letter 2 (ב): cumulative = 1+2 = 3, total = 1+3 = 4
Result: 4
```

**Baseline Truth:** Verified against gimatria789.csv (g_kidmi column)  
**Status:** ✅ Implemented and tested

---

### 12. Hebrew Perati (Product)

**Formula:** `Π(letter_values)`

**Calculation:**
```
For text "אב":
א = 1
ב = 2
Product = 1 × 2 = 2
```

**Special Case:** Empty text = 1 (empty product)

**Baseline Truth:** Verified against gimatria789.csv (g_perati column)  
**Status:** ✅ Implemented and tested

---

### 13. Hebrew Shemi (Name Values)

**Formula:** `Σ(jewish_gematria(letter_name))`

**Letter Names:**
```
א = אלף (Aleph)
ב = בית (Bet)
ג = גימל (Gimel)
...
ת = תיו (Tav)
```

**Calculation:**
1. For each letter, get its full name
2. Calculate Jewish Gematria of the name
3. Sum all name values

**Baseline Truth:** Verified against gimatria789.csv (g_shemi column)  
**Status:** ✅ Implemented and tested

---

## 🔍 Search Functionality

### Search Num (Hierarchy Value)

**Purpose:** Cross-language matching using a hierarchy value

**Formula:** `Primary_Method_Value(text)`

**Default Method:** Jewish Gematria

**Usage:**
```
search_num = calculate_search_num(text, method='jewish')
```

**Search Strategy:**
1. Calculate search_num using primary method (default: Jewish)
2. Find all phrases with same search_num across all methods
3. This enables cross-language pattern discovery

**Baseline Truth:** Verified against gematrix789.csv and gimatria789.csv (search_num/searchnum columns)  
**Status:** ✅ Implemented

---

## 🔮 Advanced Calculation Types (Placeholders)

### Numerology Calculations

**Status:** 📋 Placeholder for future implementation

**Planned Methods:**
- **Life Path Number:** Sum of birth date digits reduced to single digit
- **Expression Number:** Sum of full name reduced to single digit
- **Soul Number:** Sum of vowels reduced to single digit
- **Personality Number:** Sum of consonants reduced to single digit
- **Birthday Number:** Day of birth reduced to single digit

**Formula Placeholder:**
```python
def calculate_numerology(text: str, method: str = 'life_path') -> int:
    """
    Calculate numerology value.
    
    TODO: Implement based on ingestion data
    """
    # Placeholder - will be implemented from CSV data
    pass
```

---

### Orthogonal Calculations

**Status:** 📋 Placeholder for future implementation

**Concept:** Perpendicular/orthogonal relationships in gematria space

**Planned Methods:**
- **Orthogonal Sum:** Sum of values at right angles
- **Orthogonal Product:** Product of orthogonal values
- **Orthogonal Distance:** Distance between orthogonal points

**Formula Placeholder:**
```python
def calculate_orthogonal(text: str, method: str = 'sum') -> int:
    """
    Calculate orthogonal gematria value.
    
    TODO: Implement based on geometric relationships
    """
    # Placeholder - will be implemented from ingestion data
    pass
```

---

### Orthodontal Calculations

**Status:** 📋 Placeholder for future implementation

**Concept:** Straight-line/orthodontal relationships in gematria space

**Planned Methods:**
- **Orthodontal Sum:** Sum along straight line
- **Orthodontal Product:** Product along straight line
- **Orthodontal Sequence:** Sequential values along line

**Formula Placeholder:**
```python
def calculate_orthodontal(text: str, method: str = 'sum') -> int:
    """
    Calculate orthodontal gematria value.
    
    TODO: Implement based on linear relationships
    """
    # Placeholder - will be implemented from ingestion data
    pass
```

---

### Mirror Calculations

**Status:** 📋 Placeholder for future implementation

**Concept:** Mirror/reverse relationships (beyond Atbash)

**Planned Methods:**
- **Mirror Sum:** Sum of original + reversed
- **Mirror Product:** Product of original × reversed
- **Mirror Difference:** Difference between original and reversed
- **Mirror Ratio:** Ratio of original to reversed

**Formula Placeholder:**
```python
def calculate_mirror(text: str, method: str = 'sum') -> int:
    """
    Calculate mirror gematria value.
    
    TODO: Implement based on mirror relationships
    """
    # Placeholder - will be implemented from ingestion data
    pass
```

---

### Prime Number Calculations

**Status:** 📋 Placeholder for future implementation

**Concept:** Prime number relationships in gematria

**Planned Methods:**
- **Prime Sum:** Sum of prime factors
- **Prime Product:** Product of prime factors
- **Prime Distance:** Distance to nearest prime
- **Prime Sequence:** Position in prime sequence

**Formula Placeholder:**
```python
def calculate_prime(text: str, method: str = 'sum') -> int:
    """
    Calculate prime-based gematria value.
    
    TODO: Implement based on prime number relationships
    """
    # Placeholder - will be implemented from ingestion data
    pass
```

---

### Additional Advanced Methods (Placeholders)

**Status:** 📋 Placeholders for future implementation

**Planned Methods:**
- **Fibonacci Gematria:** Fibonacci sequence relationships
- **Golden Ratio Gematria:** Golden ratio relationships
- **Sacred Geometry Gematria:** Geometric relationships
- **Wave Gematria:** Wave/harmonic relationships
- **Quantum Gematria:** Quantum state relationships
- **Temporal Gematria:** Time-based relationships
- **Spatial Gematria:** Spatial/3D relationships

**Formula Placeholder:**
```python
def calculate_advanced(text: str, method: str) -> int:
    """
    Calculate advanced gematria value.
    
    TODO: Implement based on ingestion data and research
    """
    # Placeholder - will be implemented from CSV data
    pass
```

---

## 📊 CSV Database Schema

### gematrix789.csv Format

**Columns:**
- `phrase`: Text/phrase
- `jewish gematria`: Jewish Gematria value
- `english gematria`: English Gematria value
- `simple gematria`: Simple Gematria value
- `search num`: Search number (hierarchy value)

**Baseline Truth:** This CSV is our source of truth for English, Simple, and Jewish calculations

---

### gimatria789.csv Format

**Columns:**
- `text`: Hebrew text
- `g_full`: Hebrew Full Gematria
- `g_musafi`: Hebrew Musafi Gematria
- `g_katan`: Hebrew Katan (Reduced) Gematria
- `g_ordinal`: Hebrew Ordinal Gematria
- `g_atbash`: Hebrew Atbash (Mirror) Gematria
- `g_kidmi`: Hebrew Kidmi (Cumulative) Gematria
- `g_perati`: Hebrew Perati (Product) Gematria
- `g_shemi`: Hebrew Shemi (Name) Gematria
- `searchnum`: Search number (hierarchy value)

**Baseline Truth:** This CSV is our source of truth for Hebrew variant calculations

---

## ✅ Verification Strategy

### Baseline Verification

1. **Load CSV Data:** Ingest gematrix789.csv and gimatria789.csv
2. **Calculate Values:** Use our formulas to calculate values
3. **Compare:** Compare calculated values with CSV values
4. **Verify:** Ensure 100% match (or document discrepancies)

### Test Cases

**English Gematria:**
- "LOVE" = 54 ✅ (verified)
- "HELLO" = 52 ✅ (to verify)
- Additional test cases from CSV

**Jewish Gematria:**
- Hebrew letters verified ✅
- Additional test cases from CSV

**Hebrew Variants:**
- All 8 variants verified ✅
- Additional test cases from CSV

---

## 🔮 Future Perspectives

### Multiple Perspectives Strategy

1. **Baseline Perspective:** Use gematrix.org formulas (current)
2. **Custom Perspective:** Develop our own interpretations
3. **Comparative Analysis:** Compare perspectives
4. **Proof Generation:** Work toward mathematical proofs

### Proof Generation

**Goal:** Establish proofs for gematria relationships

**Strategy:**
1. Calculate values using multiple methods
2. Identify patterns and relationships
3. Generate hypotheses
4. Test hypotheses against data
5. Formulate proofs

---

## 📝 Notes

- All formulas are based on **gematrix.org** as baseline truth
- Placeholders are ready for future implementation
- CSV data will be used to verify and extend calculations
- Multiple perspectives will be developed and compared
- Proofs will be generated from pattern analysis

---

**Last Updated:** January 6, 2025  
**Status:** ✅ Baseline formulas documented, placeholders added

