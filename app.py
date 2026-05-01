"""Simple web UI for the study planner. Run from project root: streamlit run app.py"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from agent.agent import StudyPlannerAgent
from config import (
    DEFAULT_PLAN_DAYS,
    MAX_ITERATIONS,
    MAX_MIN_PER_DAY,
    MAX_PLAN_DAYS,
    OPENAI_API_KEY,
)
from memory.store import mark_day_completed

st.set_page_config(page_title="Study Planner", layout="wide")
st.title("Study Planner Agent")

if not OPENAI_API_KEY:
    st.error(
        "Missing `OPENAI_API_KEY` in `.env`. Add it in the project root, then refresh this page."
    )
    st.stop()

agent = StudyPlannerAgent()

tab_plan, tab_memory = st.tabs(["Create study plan", "Log completed day"])

with tab_plan:
    st.subheader("New plan")
    goal = st.text_area(
        "Your study goal",
        placeholder="e.g. Pass B1 telc in 2 months with 60 minutes per day",
        height=120,
    )
    col1, col2 = st.columns(2)
    with col1:
        minutes = st.number_input(
            "Minutes per study day",
            min_value=1,
            max_value=240,
            value=MAX_MIN_PER_DAY,
            step=5,
        )
    with col2:
        auto_length = st.checkbox(
            "Let the agent choose how many days (from your goal)",
            value=True,
        )
        if not auto_length:
            plan_days = st.number_input(
                "Number of days in the plan",
                min_value=1,
                max_value=MAX_PLAN_DAYS,
                value=DEFAULT_PLAN_DAYS,
                step=1,
            )
        else:
            plan_days = None

    if st.button("Generate plan", type="primary"):
        if not goal.strip():
            st.warning("Please enter a study goal.")
        else:
            with st.spinner("Calling the model (this can take a minute)…"):
                try:
                    result = agent.run(
                        goal=goal.strip(),
                        max_min_per_day=int(minutes),
                        plan_num_days=plan_days,
                        max_iterations=MAX_ITERATIONS,
                    )
                except Exception as e:
                    st.exception(e)
                else:
                    if result.get("length_estimate"):
                        le = result["length_estimate"]
                        st.info(
                            f"**Plan length:** {result['plan_num_days']} days "
                            f"(model suggested {le.get('model_suggested_days')}). "
                            + (f"*{le.get('rationale', '')}*" if le.get("rationale") else "")
                        )
                    st.success(f"Done in **{result['iterations']}** iteration(s).")

                    days = result["plan"].days
                    for d in days:
                        with st.expander(f"{d.day} — {d.topic} ({d.duration_minutes} min)"):
                            st.write(d.task)

                    with st.expander("Full JSON (plan)"):
                        st.code(result["plan"].model_dump_json(indent=2), language="json")

                    with st.expander("Validation"):
                        st.json(result["validation"])

with tab_memory:
    st.subheader("Mark a day completed")
    st.caption("Updates `data/study_memory.json` so future plans can skip completed topics.")
    day = st.text_input("Day label", placeholder='e.g. "Day 1"')
    note = st.text_area("Note (optional)", placeholder="What you covered…", height=80)
    if st.button("Save to memory"):
        if not day.strip():
            st.warning("Enter which day you completed (e.g. Day 1).")
        else:
            try:
                memory = mark_day_completed(day=day.strip(), note=note.strip())
            except Exception as e:
                st.exception(e)
            else:
                st.success("Memory updated.")
                st.json(memory.model_dump())
