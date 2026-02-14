#!/usr/bin/env bash
# Weddingfinder Force Work Cycle
# This script forces the system to actually do work

set -e

echo "🚀 Weddingfinder Force Work Cycle"
echo "=================================="

# Check if gateway is running
echo "📡 Checking gateway..."
openclaw health
echo "✅ Gateway online"

# Force a CEO work cycle
echo ""
echo "👔 Activating CEO Mode..."
echo "------------------------"
openclaw agent --message "You are the CEO of Weddingfinder. 

Read the file .agent/agents/TASKS.md to understand the current state.

Your task RIGHT NOW:
1. Identify the highest priority task that is NOT blocked
2. If Task 1.1 (Project Setup) is available, delegate it to the Frontend Dev
3. If Task 1.1 is blocked, delegate Task 2.1 (Scraper Setup) instead - the scraper is INDEPENDENT and should ALWAYS run
4. If both are blocked, delegate ANY available task from any workstream

Delegation format (be specific):
**Task: [TASK ID] - [Title]**
Priority: HIGH
Reference: TASKS.md Section [X]

What: [Brief description]
Deliverable: [Specific output expected]
Context: App is in WeddingfinderApp/, Supabase URL is in memory
Success Criteria:
- [ ] [Criterion 1]

Complete this task NOW, then report back with:
- Status: ✅ Complete or 🔄 In Progress
- Result: Summary of what was done
- Next: What should happen next

Do NOT say you'll do something later. DO IT NOW." --deliver --reply-channel telegram --reply-to 868619775

echo ""
echo "✅ Work cycle complete"
echo "📊 Check Telegram for results"