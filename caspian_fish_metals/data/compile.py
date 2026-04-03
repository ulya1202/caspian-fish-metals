"""
Dataset construction from verified open-access Caspian Sea fish studies.

Every value is traceable to a DOI + table reference + verification level.
See README.md for the full source list.
"""
import pandas as pd
import numpy as np


def _row(paper, doi, verif, tref, species, family, tissue,
         tcat, edible, country, basin, loc, yr, n, tl,
         method, metal, conc, sd):
    return {
        "paper_id": paper, "doi": doi, "verification": verif,
        "table_ref": tref, "species": species, "family": family,
        "tissue": tissue, "tissue_cat": tcat, "edible": edible,
        "country": country, "basin": basin, "location": loc,
        "year": yr, "n": n, "trophic_level": tl,
        "method": method, "metal": metal, "conc": conc, "sd": sd,
    }


def _bakhshalizadeh_2022():
    """
    Animals, 12(20), 2819.  PMC9597724.  CC BY 4.0.
    Table 1 — VERBATIM from open-access HTML.
    C. auratus (n=20), C. saliens (n=29).
    ICP-MS, Agilent 8900.  µg/g wet weight.
    """
    common = dict(
        paper="Bakhshalizadeh et al., 2022",
        doi="10.3390/ani12202819", verif="VERBATIM_TABLE",
        tref="Table 1", country="Iran", basin="South",
        loc="Bandar Anzali", yr=2021, method="ICP-MS",
    )

    species_data = [
        ("Chelon auratus", "Mugilidae", 20, 2.5, [
            ("caudal_muscle", "red_muscle", "limited",
             {"As":(1.71,2.21),"Cd":(0.45,0.70),"Cu":(133.53,50.80),
              "Hg":(4.75,8.18),"Ni":(10.43,18.33),"Pb":(7.31,11.77),
              "Zn":(375.16,140.37)}),
            ("ventral_muscle", "white_muscle", "yes",
             {"As":(0.65,0.42),"Cd":(0.10,0.18),"Cu":(28.04,73.84),
              "Hg":(0.03,0.02),"Ni":(0.32,0.23),"Pb":(0.11,0.08),
              "Zn":(7.84,4.51)}),
            ("dorsal_muscle", "white_muscle", "yes",
             {"As":(0.43,0.14),"Cd":(0.04,0.04),"Cu":(8.60,22.73),
              "Hg":(0.06,0.03),"Ni":(0.30,0.33),"Pb":(0.16,0.23),
              "Zn":(18.77,5.66)}),
        ]),
        ("Chelon saliens", "Mugilidae", 29, 2.4, [
            ("caudal_muscle", "red_muscle", "limited",
             {"As":(1.29,1.51),"Cd":(0.38,0.80),"Cu":(48.53,49.79),
              "Hg":(3.23,5.36),"Ni":(5.20,7.62),"Pb":(6.01,7.17),
              "Zn":(201.38,204.60)}),
            ("ventral_muscle", "white_muscle", "yes",
             {"As":(0.68,0.20),"Cd":(0.18,0.19),"Cu":(27.62,18.11),
              "Hg":(0.05,0.02),"Ni":(0.45,0.34),"Pb":(0.14,0.06),
              "Zn":(17.66,2.28)}),
            ("dorsal_muscle", "white_muscle", "yes",
             {"As":(0.52,0.15),"Cd":(0.05,0.05),"Cu":(11.60,26.72),
              "Hg":(0.07,0.03),"Ni":(0.44,0.93),"Pb":(0.12,0.18),
              "Zn":(20.14,20.46)}),
        ]),
    ]

    rows = []
    for sp, fam, n, tl, tissues in species_data:
        for tis, tcat, edib, metals in tissues:
            for m, (mean, sd) in metals.items():
                rows.append(_row(
                    **common, species=sp, family=fam,
                    tissue=tis, tcat=tcat, edible=edib,
                    n=n, tl=tl, metal=m, conc=mean, sd=sd))
    return rows


def _bakhshalizadeh_2023():
    """
    Environ Geochem Health, 45(8), 6533-6542.  PMC10403408.
    Table 2 — VERBATIM.  Medians (IQR) in ng/g -> µg/g.
    C. auratus, 5 tissues.
    """
    common = dict(
        paper="Bakhshalizadeh et al., 2023",
        doi="10.1007/s10653-023-01593-w", verif="VERBATIM_TABLE",
        tref="Table 2", species="Chelon auratus", family="Mugilidae",
        country="Iran", basin="South", loc="Bandar Anzali",
        yr=2022, n=20, tl=2.5, method="ICP-MS",
    )

    tissues = {
        "gill":      ("organ","no",  {"As":(532,563),"Cd":(18.0,46.9),
                                       "Hg":(26.5,55.2),"Pb":(355,235)}),
        "intestine": ("organ","no",  {"As":(1329,829),"Cd":(172,202),
                                       "Hg":(71.7,35.3),"Pb":(970,1312)}),
        "kidney":    ("organ","no",  {"As":(769,638),"Cd":(130,65.8),
                                       "Hg":(54.3,32.3),"Pb":(513,932)}),
        "liver":     ("organ","no",  {"As":(2389,1219),"Cd":(1689,2098),
                                       "Hg":(212,258),"Pb":(122,113)}),
        "muscle":    ("white_muscle","yes",
                                      {"As":(497,367),"Cd":(23.8,40.7),
                                       "Hg":(29.6,15.9),"Pb":(67.2,114)}),
    }

    rows = []
    for tis, (tcat, edib, metals) in tissues.items():
        for m, (med, iqr) in metals.items():
            rows.append(_row(
                **common, tissue=tis, tcat=tcat, edible=edib,
                metal=m, conc=med / 1000, sd=iqr / 1000))
    return rows


def _bakhshalizadeh_2024():
    """
    Environ Sci Pollut Res, 31, 23719-23727.  PMC10998770.
    Results section text.  A. stellatus fin spines.
    µg/kg -> µg/g.
    """
    rows = []
    for region, ctry, metals in [
        ("North", "Russia",
         {"As":(1.943,2.805),"Hg":(1.076,0.800),
          "Ni":(3.995,3.837),"V":(13.306,5.475)}),
        ("South", "Iran",
         {"As":(0.291,0.601),"Hg":(0.520,1.576),
          "Ni":(1.314,1.731),"V":(1.314,1.731)}),
    ]:
        for m, (mean, sd) in metals.items():
            rows.append(_row(
                paper="Bakhshalizadeh et al., 2024",
                doi="10.1007/s11356-024-32653-y",
                verif="FROM_TEXT", tref="Results section",
                species="Acipenser stellatus",
                family="Acipenseridae", tissue="fin_spine",
                tcat="hard_tissue", edible="no",
                country=ctry, basin=region,
                loc=f"{region}ern Caspian Sea",
                yr=2022, n=20, tl=3.5, method="ICP-MS",
                metal=m, conc=mean / 1000, sd=sd / 1000))
    return rows


def _hosseini_2013():
    """Biol Trace Elem Res, 154, 357-362.  Abstract."""
    rows = []
    for m, c, s in [("Fe",71.33,0.37),("Cr",0.27,0.019),
                     ("Pb",0.005,0.002),("As",0.005,0.002)]:
        rows.append(_row(
            paper="Hosseini et al., 2013",
            doi="10.1007/s12011-013-9740-6",
            verif="ABSTRACT", tref="Abstract",
            species="Acipenser persicus", family="Acipenseridae",
            tissue="roe", tcat="reproductive", edible="yes_caviar",
            country="Iran", basin="South",
            loc="Southern Caspian Sea",
            yr=2012, n=15, tl=3.4, method="ICP-OES",
            metal=m, conc=c, sd=s))
    return rows


def _mashroofeh_2012():
    """Bull Environ Contam Toxicol, 89(6), 1201-1204.  Abstract."""
    rows = []
    for tis, tcat, edib, m, c, s in [
        ("roe","reproductive","yes_caviar","Zn",21.48,5.20),
        ("roe","reproductive","yes_caviar","Cu",2.05,0.50),
        ("roe","reproductive","yes_caviar","Mn",1.66,0.40),
        ("muscle","white_muscle","yes","Zn",7.49,1.80),
        ("muscle","white_muscle","yes","Cu",1.00,0.25),
        ("muscle","white_muscle","yes","Mn",0.34,0.08),
    ]:
        rows.append(_row(
            paper="Mashroofeh et al., 2012",
            doi="10.1007/s00128-012-0863-9",
            verif="ABSTRACT", tref="Abstract",
            species="Acipenser persicus", family="Acipenseridae",
            tissue=tis, tcat=tcat, edible=edib,
            country="Iran", basin="South",
            loc="South Caspian Sea",
            yr=2011, n=20, tl=3.4, method="AAS",
            metal=m, conc=c, sd=s))
    return rows


def _adel_2016():
    """Toxin Reviews, 35(3-4), 217-223.  Abstract."""
    rows = []
    for m, c, s in [("Cu",1.12,0.264),("Zn",5.37,0.702),
                     ("Cd",0.058,0.023),("Pb",0.20,0.035),
                     ("Hg",0.005,0.002),("As",0.17,0.047),
                     ("Ni",0.33,0.062),("Mn",0.20,0.035)]:
        rows.append(_row(
            paper="Adel et al., 2016",
            doi="10.1080/15569543.2015.1091772",
            verif="ABSTRACT", tref="Abstract",
            species="Esox lucius", family="Esocidae",
            tissue="muscle", tcat="white_muscle", edible="yes",
            country="Iran", basin="South",
            loc="Anzali Wetland, SW Caspian",
            yr=2015, n=30, tl=4.1, method="AAS",
            metal=m, conc=c, sd=s))
    return rows


def _sobhanardakani_2018():
    """Environ Sci Pollut Res, 25, 2664-2671.  Abstract."""
    rows = []
    for m, c, s in [("As",0.01,0.005),("Cd",0.05,0.02),
                     ("Cu",1.42,0.35),("Pb",0.01,0.005),
                     ("Sn",0.28,0.10)]:
        rows.append(_row(
            paper="Sobhanardakani et al., 2018",
            doi="10.1007/s11356-017-0705-8",
            verif="ABSTRACT", tref="Abstract",
            species="Acipenser persicus", family="Acipenseridae",
            tissue="roe", tcat="reproductive", edible="yes_caviar",
            country="Iran", basin="South",
            loc="Southern Caspian Sea",
            yr=2016, n=30, tl=3.4, method="ICP-OES",
            metal=m, conc=c, sd=s))
    return rows


def compile():
    """Merge all sources into a single DataFrame."""
    all_rows = (
        _bakhshalizadeh_2022()
        + _bakhshalizadeh_2023()
        + _bakhshalizadeh_2024()
        + _hosseini_2013()
        + _mashroofeh_2012()
        + _adel_2016()
        + _sobhanardakani_2018()
    )
    df = pd.DataFrame(all_rows)
    df["log_conc"] = np.log10(df["conc"].clip(lower=1e-6))
    return df
