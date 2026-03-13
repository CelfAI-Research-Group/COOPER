
# Dataset Link 

https://huggingface.co/datasets/CelfAI/COOPER

# 📡 COOPER  
### Cellular Operational Observations for Performance and Evaluation Research  
**An Open Benchmark of Synthetic Mobile Network Performance Indicators for Reproducible Research**

---

## 🧭 Overview

**COOPER** is an open-source **synthetic dataset of mobile network performance measurement (PM) time series**, designed to support **reproducible AI/ML research** in wireless networks. The dataset is named in honor of **Martin Cooper**, a pioneer of cellular communications.

COOPER emulates the **statistical distributions, temporal dynamics, and structural patterns** of real 5G network PM data while containing **no sensitive or operator-identifiable information**.

The dataset is released together with a **reproducible benchmarking framework** used to evaluate synthetic data generation methods.

---

## 🎯 Motivation

Access to real telecom PM/KPI data is often restricted due to:

- Confidentiality agreements  
- Privacy regulations  
- Commercial sensitivity  

This lack of open data limits **reproducibility** in AI-driven research for wireless networks. COOPER addresses this gap by providing a **realistic yet privacy-preserving synthetic alternative** suitable for:

- Network monitoring research  
- KPI forecasting  
- Anomaly detection  
- AI-native network automation  
- 5G/6G performance evaluation  

---

## 🏗 Dataset Creation Methodology

To generate COOPER, three complementary synthetic data generation paradigms were evaluated:

1. **Adversarial approaches**
2. **Probabilistic models**
3. **Model-based time-series methods**

These were benchmarked using a **unified quantitative and qualitative evaluation framework** considering:

- Distributional similarity  
- Temporal fidelity  
- Shape alignment  
- Discriminative performance  
- Downstream forecasting capability  

The generator demonstrating the most **balanced and consistent performance** across these criteria was selected to produce COOPER.

---

## 📊 Source Data Characteristics (Before Anonymization)

The real dataset used to model the synthetic data was:

- Fully **anonymized** to remove operator-sensitive information  
- Cleaned and standardized for consistency  

| Property | Value |
|---------|------|
| Radio Access Technology | 5G |
| Number of PM Indicators | 45 |
| Total Number of Cells | 84 |
| Base Stations | 12 |
| Geographic Area | ~1.35 km² |
| Collection Period | 31 days |
| Sampling Interval | 1 hour |
| Data Representation | Multi-cell time series |

A **cell** is defined as a radiating unit within a specific RAT and frequency band. Each base station may host multiple cells.

---

## 📡 Network Deployment Characteristics

The modeled network includes two frequency bands and two 5G architectures:

| Band | Architecture | Number of Cells |
|------|-------------|----------------|
| N28 (700 MHz) | Option 2 (Standalone) | 6 |
| N28 (700 MHz) | Option 3 (Non-Standalone) | 48 |
| N78 (3500 MHz) | Option 2 (Standalone) | 6 |
| N78 (3500 MHz) | Option 3 (Non-Standalone) | 24 |

Most cells operate in **Option 3 (NSA)** mode, reflecting a typical **EN-DC deployment** where LTE provides the control-plane anchor.

---

## 📈 PM Indicator Categories

Indicators follow **3GPP TS 28.552** performance measurement definitions and are grouped into:

### 1️⃣ Radio Resource Control (RRC) Connection
Procedures for establishing UE radio connections and tracking active users.
- `RRC.ConnEstabSucc`
- `RRC.ConnEstabAtt`
- `RRC.ConnMax`

### 2️⃣ Mobility Management
Handover and redirection performance across frequencies.
- `MM.HoExeIntraFreqSucc`
- `MM.HoExeInterFreqSuccOut`

### 3️⃣ Channel Quality Indicator (CQI)
Distribution of downlink channel quality reports (CQI 0–15).
- `CARR.WBCQIDist.Bin0`
- `CARR.WBCQIDist.Bin15`

### 4️⃣ Throughput and Data Volume
Traffic volume and transmission duration.
- `ThpVolDl`
- `ThpTimeDl`

### 5️⃣ Availability
Cell downtime due to failures or energy-saving mechanisms.
- `CellUnavail.System`
- `CellUnavail.EnergySaving`

### 6️⃣ UE Context
User session establishment attempts and successes.
- `UECNTX.Est.Att`
- `UECNTX.Est.Succ`

---

## 🧪 Benchmarking Framework

COOPER is distributed with a **reproducible evaluation pipeline** that allows researchers to compare synthetic data generators using:

- Statistical similarity metrics  
- Temporal alignment measures  
- Shape-based similarity  
- Classification distinguishability  
- Forecasting task performance  

This framework enables standardized evaluation of synthetic telecom datasets.

---

## 🔬 Intended Use Cases

COOPER is suitable for:

- Time-series forecasting research  
- Network anomaly detection  
- Root cause analysis modeling  
- RAN performance optimization studies  
- Reproducible academic research in 5G/6G systems  

---

## ⚠️ Data Notice for Dataset Users

**Due to the real network nature of the source data, some inconsistent values were intentionally maintained in this dataset.**  
We recommend **preprocessing the data before use** (e.g., handling outliers, missing values, or domain-specific inconsistencies) according to your application and methodology.

---

## 🤝 Contribution & Reproducibility

This project promotes **open and reproducible telecom AI research**.  
Researchers are encouraged to:

- Benchmark new generation models using the provided framework  
- Share improvements and derived datasets  
- Compare methods under the same evaluation protocol  

---

## 📜 License

This dataset is released for **research and educational purposes**.  
(Include specific license here, e.g., CC BY 4.0 / MIT / Apache 2.0)

---

## 📖 Citation

If you use COOPER in your research, please cite:

> *COOPER: An Open Benchmark of Synthetic Mobile Network Performance Indicators for Reproducible Research*

(Full citation to be added)

