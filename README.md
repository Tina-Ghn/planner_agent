# Study planner

This is a little tool that asks OpenAI to turn your study goal into a day-by-day plan. You can use it in the terminal or in the browser.

**What it does:** you describe what you want (e.g. pass an exam in two months), say how many minutes you have per day, and optionally how many days the plan should span—or let the app guess that from your goal. It can also remember which days you already finished so the next plan does not repeat the same stuff.

## Quick start

You need Python and an OpenAI API key.

```bash
pip install -r requirements.txt
cp .env.example .env
```

Put your key inside `.env` as `OPENAI_API_KEY=...`. 

Then, from this folder:

```bash
python main.py
```

For a simple web version:

```bash
streamlit run app.py
```

Most settings (model name, default minutes, how hard the validator should retry) live in `config.py` if you want to tweak them.

## TODO (ideas for later)

Nothing here is urgent—just a scratchpad so future-you remembers what might be nice.

- [ ] **Tests** — a few unit tests for the validator and memory loader would make refactors less scary.
- [ ] **Export** — download the plan as PDF or `.ics` so it lands on a real calendar.
- [ ] **Smarter goal parsing** — pull “60 minutes” and “two months” straight out of one goal sentence so the UI asks fewer questions.
- [ ] **Cost / usage** — show rough token spend after each run (optional, behind a setting).
- [ ] **Notebook** — align `notbk.ipynb` with the same flow as `main.py` / `app.py` so examples don’t drift.
- [ ] **Deploy** — tiny hosted demo (Streamlit Cloud, etc.) with env vars in the host, not in the repo.

That’s it. Have fun studying.
