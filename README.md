# cocorahs_fl-sm-38

Analysis of my at-home [CoCoRaHS](https://www.cocorahs.org/) rain gauge, **station FL-SM-38** (Seminole County, FL). The station started reporting in January 2021. Its record is compared with neighboring county stations and with the GHCN-Daily record at Orlando International Airport (`USW00012815`).

The goal is a self-updating dashboard: pull the data every day, compute station metrics, and plot them.

**Official station dashboard:** CoCoRaHS publishes a public page for this station on its Data Explorer (DEX): <https://dex.cocorahs.org/stations/FL-SM-38/>. It is the reference view of the station's record, and its information and data can be pulled at any time. How this repo will build on it is still undecided.

> This repo replaces the older [dgilford/cocorahs](https://github.com/dgilford/cocorahs).

## Contents

```
legacy/
  code/cocorahs_dev/   # Original download script and exploratory notebooks (2021–2025)
  notes/               # Lab-notebook entries on the project's history and ideas
```

What's been prototyped so far: daily and cumulative rainfall, annual comparisons, monthly totals, rain-day fraction, consecutive dry days, distances to nearby stations, and comparison with Orlando International Airport's climatology.

## Data

Data files are **not tracked** (`*.csv` is gitignored). To regenerate them:

- **CoCoRaHS daily reports (Seminole County):**
  ```bash
  cd legacy/code/cocorahs_dev && python get_cocorahs_FL-SM_today.py
  ```
  This calls the `exportreports.aspx` endpoint on `data.cocorahs.org`. Multi-day reports come from the same endpoint with `ReportType=MultiDay`.
- **GHCN-Daily, Orlando International Airport:** order from [NCEI Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) and save to `legacy/code/cocorahs_dev/data/ghcn/`.

## License

[MIT](LICENSE)
