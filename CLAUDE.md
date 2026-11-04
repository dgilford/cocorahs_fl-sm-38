# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal analysis of Daniel's at-home CoCoRaHS rain gauge, **station `FL-SM-38`** (Seminole County, FL; first obs Jan 2021), compared against neighboring CoCoRaHS stations and the GHCN-Daily record at **Orlando International Airport (`USW00012815`)**. The stated goal (see `legacy/notes/`) is a **self-updating dashboard**: a daily scheduled pull → station metrics → plots, eventually with CI.

**Repo:** github.com/dgilford/cocorahs_fl-sm-38 (public, MIT). It replaces the old `dgilford/cocorahs`.

**Current state: everything lives in `legacy/`.** There is no package, environment file, test suite, or build.

```
legacy/
  code/cocorahs/        # Old repo shell (github.com/dgilford/cocorahs). Gitignored and superseded
  code/cocorahs_dev/    # The actual working code (scripts + notebooks) and its data/
  data/                 # Latest daily export (2021-01-01 → 2025-02-19)
  notes/                # Lab-notebook entries, CoCoRaHS-only, describing intent and progress
  ams2023/              # AMS 2023 poster PDF (48 MB). Gitignored
```

**Not tracked by git:** all `*.csv` data, `legacy/ams2023/`, and `legacy/code/cocorahs/`. They exist only locally and can be regenerated as described below.

## Running the legacy code

All paths are relative to `legacy/code/cocorahs_dev/`, so run from there.

```bash
cd legacy/code/cocorahs_dev
python get_cocorahs_FL-SM_today.py   # downloads data/cocorahs_FL-SM_01-01-2021_to_<MM-DD-YYYY today>.csv
```

- Depends on the `wget` **PyPI package** (not the CLI), plus pandas/numpy/matplotlib; `haversine` and scipy for the nearby-station cells.
- Notebooks (`explore_cocorahs_data.ipynb`, `cocorahs_ams2023.ipynb`) begin with `%run get_cocorahs_FL-SM_today`, then load the file **named by today's date**, so they only work on a day the download succeeded.
- GHCN loads use relative `./data/ghcn/*.csv` paths. These files are gitignored, so a fresh clone needs them re-ordered from NCEI.
- Run them in this order: `download_dat_interactive` → `explore_cocorahs_data` → `cocorahs_ams2023`. They run top to bottom in the base anaconda env (Python 3.8, pandas 1.5.3) with `jupyter nbconvert --execute --inplace --allow-errors`. Expect the known errors: each notebook ends at a deliberate `break_here` stop cell, and the AMS notebook has unfinished cells (the multi-day spread, `pd.merge()` stub, `full_label`/`annual_precip_std` used before definition, Period plotting).
- Each `%run get_cocorahs_FL-SM_today` re-downloads, and the `wget` package writes duplicates as `... (1).csv` instead of overwriting.
- The legacy notebooks use APIs removed in pandas ≥ 2 (`Series.append`) and matplotlib (`MarkerSize=`). Expect to fix these on a modern env.
- Trace handling differs between the notebooks and changes the results. At FL-SM-38, filling trace as 0.001 (explore notebook) instead of 0.000 (AMS notebook) raises the rain-day fraction by about 4 percentage points.

## Data sources

**CoCoRaHS DEX station dashboard**: <https://dex.cocorahs.org/stations/FL-SM-38/> is the official public dashboard for this station. Information and data can be pulled from it at any time. How it fits into this repo is still undecided, so check what it already shows before building a duplicate view.

**CoCoRaHS export endpoint** (county-wide, all stations):
```
http://data.cocorahs.org/export/exportreports.aspx?ReportType=Daily&dtf=1&Format=CSV&State=FL&County=SM&ReportDateType=reportdate&StartDate=MM/DD/YYYY&EndDate=MM/DD/YYYY&TimesInGMT=False
```
- `ReportType=MultiDay` returns multi-day accumulation reports (`StartDate`, `EndDateTime`, `TotalPrecipAmt`). The only local copy is `data/MultiDayPrecipReports_FL_SM_2021-01-01_1.csv`, which is not refreshed by the script.
- `cocorahs_dev/data/` holds many dated snapshots; each one is a superset of the earlier ones, so only the newest matters.

**GHCN-Daily (Orlando Intl)**: NCEI CDO order CSVs in `cocorahs_dev/data/ghcn/` (columns `STATION,NAME,DATE,PRCP,SNOW,SNWD,TAVG,TMAX,TMIN`, US units, record starts 1952). They are static one-off orders and have no automated refresh.

## Data pitfalls (these matter for any rewrite)

- **Leading whitespace**: the export uses `", "` separators, so string fields carry a leading space. The legacy code matches `' FL-SM-38'` literally. Use `pd.read_csv(..., skipinitialspace=True)`.
- **Trace** is the string `"T"`. The two legacy notebooks disagree on its fill value (`0.000` vs `0.001`), and that choice changes rain-day counts and CDD. Make it an explicit, documented parameter.
- **Rows are newest-first**. The legacy code reverses them with `iloc[::-1]`. Sort by date instead.
- **Rows are observations, not calendar days.** Missing days are never reindexed, so cumulative sums, rain-day fractions and the consecutive-dry-day (`cdd_calc`) loop count observations and quietly bridge gaps. A station can also file more than one report per day.
- **Multi-day reports are not in the daily file.** Rain from those periods is missing from daily totals. `cocorahs_ams2023.ipynb` starts spreading each multi-day total evenly across its days, but the merge is unfinished (`pd.merge()` stub). Even spreading is an assumption.
- **Observation windows differ**: CoCoRaHS days end at the ~7–8 AM local obs time, while GHCN-Daily days at OIA run midnight to midnight. Day-by-day comparisons are offset. Compare at monthly or cumulative scales, or say what the mismatch does to the result.

## Analyses already prototyped (in the notebooks)

Daily time series; total and per-year cumulative rainfall; histogram; monthly accumulation bars; ranked wettest days; rain-day fraction; consecutive dry days; haversine distance and obs count for each county station relative to FL-SM-38; FL-SM-38 against the OIA climatological cumulative mean ± spread. An open question in the notes: **how to correlate zero-inflated daily precipitation between nearby stations**.
