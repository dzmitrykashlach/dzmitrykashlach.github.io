---
name: extract-missing-skills
description: Build a ranked list of skills from matching vacancies that are not present in the resume.
model: inherit
---
# Extract Missing Skills

Use this skill when updating `job/skills.md` from accepted matches.

## Steps
1. Read accepted matching posts from `job/positions.md`.
2. Compare vacancy requirements against the resume profile baseline.
3. Keep only skills not represented in resume.
4. Count mentions across matching vacancies.
5. Update `job/skills.md` sorted by mentions descending.

## Output
- Mention top missing skills and any tie-break choices.
