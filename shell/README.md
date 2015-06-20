# Shell

These should run in any Bourne-like shell.  I develop on Ubuntu using **dash**.
Please let me know if you run into something calling itself **sh** where the script doesn't work.

## rename-ogs.sh
Rename files downloaded by [uberdownloader](https://github.com/thouis/uberdownloader).

To run,
```
sh rename-ogs.sh
```

This will rename files matching the pattern `OGS_game_*.sgf`.
If the file is an SGF file, it will extract the date and the players' names.
The new file will be named `OGS-<date>-<game number>-<black player>-<white player>.sgf`.

**NOTE: If the file is not SGF, the results are unpredictable.**
