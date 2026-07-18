# Meal-planning deterministic loop. Every target below is ZERO-TOKEN (plain Python).
# AI touchpoints are NOT make targets — they're prompt templates in ai/ you run by
# hand only for the four fuzzy tasks. See README.
#
# PY override: `make coverage PY=python3` if your interpreter differs.
PY ?= python
SCRIPTS := scripts
CYCLE ?=        # optional: make coverage CYCLE=cycles/2026-06-07.yaml

.PHONY: help new-cycle week coverage grocery defrost schedule deplete deplete-apply validate validate-cycle cook-plan test demo

help:
	@echo "Meal-planning loop (all no-tokens):"
	@echo "  make new-cycle      - interactive: write cycles/<date>.yaml (auto-archives the prior cycle)"
	@echo "  make week           - PREFLIGHT (incl. deplete-nudge) + coverage + grocery + defrost + schedule"
	@echo "  make coverage       - needed vs planned per slot/person; Elena (cover-first) leads"
	@echo "  make grocery        - aggregate ingredients x servings - inventory, by store"
	@echo "  make defrost        - freezer->fridge move schedule"
	@echo "  make schedule       - ordered cook plan for the cycle"
	@echo "  make validate-cycle - per-ingredient inventory check for the cycle (file value vs need, flags short/zero/missing)"
	@echo "  make cook-plan      - generate cycles/<date>-cook-plan.md scaffold (phone artifact)"
	@echo "  make deplete        - dry-run inventory depletion (add APPLY=1 to write)"
	@echo "  make validate       - recipe DB schema + integrity (add STRICT=1 to harden)"
	@echo "  make test           - run the regression tests (scripts/tests/)"
	@echo "  make demo           - validate + coverage + grocery + defrost + schedule on latest cycle"
	@echo ""
	@echo "AI (TOKENS, run by hand — not make): ai/vet_recipe.md, ai/suggest_recipes.md,"
	@echo "  ai/produce_pairing.md, ai/troubleshoot.md"

new-cycle:
	@$(PY) $(SCRIPTS)/new_cycle.py

week:
	@$(PY) $(SCRIPTS)/run_week.py $(CYCLE)

coverage:
	@$(PY) $(SCRIPTS)/coverage.py $(CYCLE)

grocery:
	@$(PY) $(SCRIPTS)/grocery.py $(CYCLE)

defrost:
	@$(PY) $(SCRIPTS)/defrost.py $(CYCLE)

schedule:
	@$(PY) $(SCRIPTS)/cook_schedule.py $(CYCLE)

deplete:
	@$(PY) $(SCRIPTS)/deplete.py $(CYCLE) $(if $(APPLY),--apply,)

validate:
	@$(PY) $(SCRIPTS)/validate.py $(if $(STRICT),--strict,)

validate-cycle:
	@$(PY) $(SCRIPTS)/validate_cycle.py $(CYCLE)

cook-plan:
	@$(PY) $(SCRIPTS)/cook_plan.py $(CYCLE) $(if $(FORCE),--force,)

test:
	@$(PY) -m pytest $(SCRIPTS)/tests -q

demo: validate coverage grocery defrost schedule
	@echo ""
	@echo "Demo complete — full deterministic loop ran with zero AI calls."
