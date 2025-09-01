.PHONY: rules-merge rules-check dev-setup

CURSOR_RULES_DIR := .cursorrules
MERGED := $(CURSOR_RULES_DIR)/generated/_merged.md

rules-merge:
	mkdir -p $(CURSOR_RULES_DIR)/generated
	cat $(CURSOR_RULES_DIR)/common/00-core.md \
	    $(CURSOR_RULES_DIR)/common/10-security.md \
	    $(CURSOR_RULES_DIR)/common/stacks/*.md \
	    $(CURSOR_RULES_DIR)/project/*.md > $(MERGED)
	cp $(MERGED) .cursorrules.md
	echo "Merged -> .cursorrules.md"

rules-check:
	grep -q "^## Security & Secrets" $(MERGED) || (echo "❌ security section missing"; exit 1)
	echo "✅ rules basic checks passed"

rules-generate: rules-merge rules-check

dev-setup:
	command -v pre-commit >/dev/null || pipx install pre-commit || pip install pre-commit
	pre-commit install -t pre-commit -t commit-msg || true
	@$(MAKE) rules-generate