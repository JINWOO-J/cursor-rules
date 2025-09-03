---
lang: en
source_lang: kr
source_sha: ac9ae8d09e3a127a4d0a9130a7e495831ea1dc7c33044a909e7c6c249d3aab77
---
# Git Style Guide

## Commit Messages
- Commit messages should be written in **declarative sentences** and kept concise. (Conventional Commits are not used)
  Example: `Fix PS1 prompt escaping for zsh.`
- Adhere to the **three-line guideline** for PR descriptions: summary of changes, scope of impact, and rollback method.

## Branch Naming
- Branch names should use prefixes such as `feature/`, `bugfix/`, `hotfix/` to clearly indicate their purpose.
- Branch names should only use lowercase English letters, numbers, and hyphens (-).
  Example: `feature/user-authentication`, `bugfix/login-error-handling`

## Pull Request (PR)
- The PR title should clearly summarize the changes.
- The PR description should include:
  - **Summary of Changes**: Briefly explain what has been changed.
  - **Scope of Impact**: Explain which parts are affected by the changes.
  - **Rollback Method**: Explain how to rollback in case of problems.

## Code Review
- Reviews should provide **constructive feedback** and focus on the code, not the individual.
- Clearly explain the **"Why"** and **"How"**.
- Review comments should be **actionable**.
- **Don't forget to give praise!**

## Development Process
1.  **Feature Analysis**: Analyze the context of the Jira ticket.
2.  **Development Plan Creation**: Analyze existing code and create a development plan by dividing the implementation into 5-6 small steps. Save the plan in the `docs/[feature]_[summary].md` file. (No code modification at this stage.)
3.  **Plan Review**: Review the created `[feature]_[summary].md` file. If any modifications are needed, modify them directly or request changes from the Agent.
4.  **Step-by-Step Implementation**: Request code implementation from the Agent based on `[feature]_[summary].md`. (Requesting in appropriately small steps improves the quality of the results) (It is recommended to commit & push per step)
5.  **Content Review**: Review the modified content using Diff. (You can also review it directly or with other tools like Claude Code.)
6.  **Plan Update**: If the development plan is modified during the implementation process, reflect it in the .md file to keep the document and implementation status consistent. (You can also ask the Agent to update the .md file with the actual implemented content after the implementation is complete.)
7.  **Testing and Static Analysis**: Perform testing and static analysis.
8.  **PR Creation**: Create a PR after testing and static analysis are complete.
9.  **Automated Review**: Automated review of the PR is performed by Claude. (Request if the repo doesn't have the setting)
10. **Review Incorporation**: Check the review content on GitHub and make necessary modifications.
11. **Partner Review Request**: Request a review from a Partner.
12. **Merge**: Merge after the Partner approves.
