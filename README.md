# UllieMoeke Productions website

Static site for GitHub Pages: the app showcase and a privacy policy for every app.

| URL | File |
|---|---|
| `/` | `index.html` |
| `/privacy/` | `privacy/index.html` |
| `/privacy/literally-emergency/` (+ `nl.html`, `de.html`, `fr.html`) | generated |
| `/privacy/literally-just-a-scanner/` | generated |
| `/privacy/literally-plantscan/` | generated |
| `/app-ads.txt` | AdMob verification for all apps (same publisher ID) |

## Updating privacy policies

```sh
python tools/build_privacy.py            # optional arg: path to the LiterallyEmergency project
```

- **Literally Emergency** is read from the app's `strings.xml` in four languages, so just rerun the script.
- **Scanner** and **Plantscan** texts live in `tools/build_privacy.py`; edit them there when the app's privacy screen changes.

## Publishing

AdMob only reads `app-ads.txt` at the root of a domain, so publish this as a **user site**:
a repository named `<github-username>.github.io`, with Pages set to deploy from the `main` branch, root folder.
The site is then live at `https://<github-username>.github.io/`, and the privacy URLs to paste in Play Console are
`https://<github-username>.github.io/privacy/<app>/`.

All links are relative, so it also works as a project site (`/<repo>/`), but then `app-ads.txt` won't be found.
