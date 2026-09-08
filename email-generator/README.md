# Email Template Generator — Scholars Queensway

Build parent emails from reusable templates: fill a single email, or generate a
whole batch from an Excel/CSV file. Templates are stored in **`templates.json`**
in this folder — a real file you can share, copy to another computer, and commit
to git.

## Run it

**Windows:** double-click **`start.bat`**
**Mac/Linux:** run **`./start.sh`** (first time: `chmod +x start.sh`)

Either one starts a tiny local server and opens the app in your browser at
`http://127.0.0.1:8770/index.html`. Leave the little console window open while you
work; press **Ctrl+C** (or close it) to stop.

Requires **Python 3** (already on most machines; get it at https://python.org if not).

> You *can* also open `index.html` directly by double-clicking, but then it can't
> read or write `templates.json` — it falls back to a temporary browser copy and
> shows a warning. Use `start.bat` / `start.sh` for the real, shared templates.

## What it does

- **Single email** — pick a template, fill in the details, copy the subject and
  body separately (links preserved), or download as Word.
- **Bulk from Excel** — upload a spreadsheet and get one Word doc with every
  email, one per page.
- **Edit templates** — create / edit / delete templates. Saved straight to
  `templates.json`.
- **Guide** — every placeholder explained.

## Placeholders

| Placeholder | Fills with |
|---|---|
| `{{StudentName}}` | student's first name |
| `{{LastName}}`, `{{FullName}}` | last / full name |
| `{{ParentName}}` | parent / guardian name |
| `{{anything}}` | **custom field** — see below |

**Custom fields:** use any placeholder you want, e.g. `{{hours}}`, `{{grade}}`,
`{{StartDate}}`, `{{amount}}`. Matching ignores case and spaces.
- In **bulk**, every column in your Excel is available automatically — add a
  `Hours` column and `{{hours}}` fills from it.
- In **single**, an input box appears for each custom placeholder in the template.

**Hyperlinks:** write `[visible text](https://url)` — it stays a real clickable
link when you copy into Gmail/Outlook or export to Word.

**Pronouns (optional):** `{{he}}`, `{{him}}`, `{{his}}` follow a Gender field.
The built-in templates are written without pronouns, so you can ignore Gender.

## Templates file / git

`templates.json` is the single source of truth. To version it:

```
git init
git add .
git commit -m "Email templates"
```

Share the whole folder (or just `templates.json`) to move templates between
machines or people. The app keeps automatic backups: `templates.json.bak` is the
previous version after each save.

## Files

- `index.html` — the app
- `server.py` — local server + read/write of `templates.json`
- `templates.json` — your templates (tracked in git)
- `start.bat` / `start.sh` — launchers
