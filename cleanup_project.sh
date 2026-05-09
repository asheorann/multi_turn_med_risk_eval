#!/bin/bash
# Project cleanup script - Run before sharing with recruiters/professors
# Usage: bash cleanup_project.sh

set -e  # Exit on error

echo "🧹 Cleaning up project for presentation..."
echo ""

# Create docs/archive directory if it doesn't exist
echo "📁 Creating docs/archive directory..."
mkdir -p docs/archive

# Move old planning documents to archive
echo "📦 Archiving old planning documents..."
if [ -f "plan_for_multi_step.txt" ]; then
    mv plan_for_multi_step.txt docs/archive/
    echo "  ✓ Moved plan_for_multi_step.txt"
fi

if [ -f "PRESENTATION_FLOW.md" ]; then
    # Ask user if this is outdated
    read -p "  ⚠️  Is PRESENTATION_FLOW.md outdated? (y/n): " response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        mv PRESENTATION_FLOW.md docs/archive/
        echo "  ✓ Moved PRESENTATION_FLOW.md"
    else
        echo "  → Keeping PRESENTATION_FLOW.md"
    fi
fi

# Remove checkpoint files
echo "🗑️  Removing checkpoint files..."
if [ -d "results/template_adaptive" ]; then
    rm -f results/template_adaptive/*_checkpoint*.json
    echo "  ✓ Removed template_adaptive checkpoints"
fi

# Move dry run results
echo "📂 Organizing dry run results..."
if [ -f "results/phase1_single_turn_dryrun.jsonl" ]; then
    mv results/phase1_single_turn_dryrun.jsonl results/classifier_phase1/
    echo "  ✓ Moved phase1_single_turn_dryrun.jsonl"
fi

# Create .env.example if .env exists
echo "🔒 Creating .env.example..."
if [ -f ".env" ]; then
    if [ ! -f ".env.example" ]; then
        cat > .env.example << 'EOF'
# OpenRouter API (recommended for multi-model access)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# OR use OpenAI directly
OPENAI_API_KEY=sk-xxxxxxxxxxxxx

# Instructions:
# 1. Copy this file to .env
# 2. Replace the xxx values with your actual API keys
# 3. Never commit .env to git
EOF
        echo "  ✓ Created .env.example"
    else
        echo "  → .env.example already exists"
    fi
fi

# Check if LICENSE exists
echo "📄 Checking LICENSE..."
if [ ! -f "LICENSE" ]; then
    echo "  ⚠️  LICENSE file missing - consider adding MIT license"
    echo "     Visit: https://choosealicense.com/licenses/mit/"
else
    echo "  ✓ LICENSE exists"
fi

# Clean up Python cache
echo "🐍 Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "  ✓ Removed __pycache__ and .pyc files"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review README.md and update:"
echo "     - Replace 'Expected Outcomes' with 'Key Findings'"
echo "     - Update experiment status (mark completed)"
echo "     - Add your name to citation (line 248)"
echo ""
echo "  2. Verify .env is not tracked:"
echo "     git status | grep .env"
echo ""
echo "  3. Commit changes:"
echo "     git add -A"
echo "     git commit -m 'Clean up project structure and add documentation'"
echo "     git push"
echo ""
echo "  4. Review PROJECT_REVIEW.md for detailed checklist"
echo ""
