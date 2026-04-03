# Caspian Sea Fish Heavy Metals — Analysis Pipeline

Accompanies the manuscript:  
> "Heavy Metal Concentrations in Caspian Sea Fish Species Compiled From
> Open-Access Sources: Tissue-Specific Bioaccumulation Patterns, Health
> Risk Assessment, and Monitoring Implications for Azerbaijan"

Dataset DOI: https://doi.org/10.5281/zenodo.19410390

## Setup

```bash
pip install pandas numpy scipy matplotlib seaborn
```

## Usage

```bash
python run.py
```

All outputs (tables, figures, dataset CSV) are written to `output/`.

## Project Structure

```
caspian_fish_metals/
├── README.md
├── requirements.txt
├── config.py              # Constants, parameters, file paths
├── run.py                 # Entry point — executes full pipeline
├── data/
│   └── compile.py         # Dataset construction from published sources
├── analysis/
│   ├── descriptive.py     # Table 1: descriptive statistics
│   ├── kruskal.py         # Table 2: Kruskal-Wallis H tests
│   └── health_risk.py     # Table 4: THQ / HI calculations
├── figures/
│   └── plots.py           # Figures 1–4
└── output/                # Generated tables, figures, CSV
```

## Data Sources

| # | Reference | DOI | Verification |
|---|-----------|-----|-------------|
| 1 | Bakhshalizadeh et al., 2022 | 10.3390/ani12202819 | Table (PMC) |
| 2 | Bakhshalizadeh et al., 2023 | 10.1007/s10653-023-01593-w | Table (PMC) |
| 3 | Bakhshalizadeh et al., 2024 | 10.1007/s11356-024-32653-y | Text (PMC) |
| 4 | Hosseini et al., 2013 | 10.1007/s12011-013-9740-6 | Abstract |
| 5 | Mashroofeh et al., 2012 | 10.1007/s00128-012-0863-9 | Abstract |
| 6 | Adel et al., 2016 | 10.1080/15569543.2015.1091772 | Abstract |
| 7 | Sobhanardakani et al., 2018 | 10.1007/s11356-017-0705-8 | Abstract |

## License

Code: MIT  
Dataset: CC BY 4.0
