# Strava Ride Analysis

Utilities for separating Strava workout exports and preparing ride data for
analysis. The current codebase focuses on the file-ingestion step: identifying
TCX activities by sport and moving the matching rides into a clean working
folder for downstream EDA or dashboard work.

## Features

- Parses TCX files using the Python standard library
- Filters activities by sport type, with `Ride` as the default
- Works from the local machine without Colab-specific paths
- Preserves the original TCX files by copying, not moving
- Supports optional recursive scanning and destination cleanup

## Repository layout

```text
Strava-Ride-Analysis/
  TcxFileSegregation.py
  README.md
  LICENSE
  CONTRIBUTING.md
  docs/
    tutorial.md
```

## Quick start

1. Export your Strava activities as TCX files.
2. Put the files in a source folder.
3. Run the script:

```bash
python TcxFileSegregation.py --source . --destination Moved --sport Ride --clear-destination
```

4. Use the files in `Moved/` for the next stage of analysis.

## Tutorial

See [docs/tutorial.md](docs/tutorial.md) for a step-by-step walkthrough.

## Screenshots

This repository is a command-line utility, so the most useful visuals are
example terminal output and any downstream plots or dashboards produced from
the separated ride files. Add those under `docs/images/` when they are
available.

## Notes

- TCX parsing errors are reported per file, so one bad export will not stop the
  whole batch.
- The script copies matching rides into the destination folder instead of
  modifying the source folder.
- The default target sport is `Ride`, but any sport name in the TCX file can be
  supplied.

## How to cite

If you reuse the script or the repository structure, cite it as:

```text
Abeer Nasir Chaudhry, Strava Ride Analysis, GitHub repository.
```

## License

Released under the MIT License. See [LICENSE](LICENSE).
