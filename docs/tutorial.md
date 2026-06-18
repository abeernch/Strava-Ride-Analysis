# Tutorial

1. Export your activities from Strava in TCX format.
2. Place the exported files in a source directory.
3. Run the segregation script from that directory or point `--source` at it.
4. Keep the separated ride files in `Moved/` or a custom destination folder.
5. Load the cleaned files into notebooks, spreadsheets, or Power BI for the
   analysis stage.

## Example commands

Copy ride activities from the current directory:

```bash
python TcxFileSegregation.py
```

Copy from a specific folder and clear the destination first:

```bash
python TcxFileSegregation.py --source "C:\data\strava" --destination "C:\data\rides" --clear-destination
```

## Practical notes

- The parser reads the sport flag from the TCX activity record.
- Files that fail to parse are skipped and reported.
- The script copies matching files, so the source export remains unchanged.
