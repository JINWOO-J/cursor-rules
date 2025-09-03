---
lang: en
source_lang: kr
source_sha: ac9ae8d09e3a127a4d0a9130a7e495831ea1dc7c33044a909e7c6c249d3aab77
---
```md
# Git Style Guide

## Commit Message
- Commit messages should be in **sentence form and concise**. (Conventional Commits not used)
  Ex: `Fix PS1 prompt escaping for zsh.`
- Adhere to the **3-line rule** in PR descriptions: change summary, scope of impact, and rollback method.

## Branch Naming
- Branch names should use prefixes like `feature/`, `bugfix/`, `hotfix/` to clarify their purpose.
- Branch names should only use lowercase English letters, numbers, and hyphens (-).
  Ex: `feature/user-authentication`, `bugfix/login-error-handling`

## Pull Request (PR)
- PR titles should clearly summarize the changes.
- PR descriptions should include the following:
  - **Change Summary**: Briefly explain what was changed.
  - **Scope of Impact**: Explain which parts are affected by the changes.
  - **Rollback Method**: Explain how to rollback in case of problems.

## Code Review
- Reviews should be **constructive feedback**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**.
- Review comments should be **actionable**.
- **Don't forget compliments.**

## Development Process
1.  **Feature Analysis**: Analyze the context of the Jira ticket.
2.  **Development Plan Establishment**: Analyze existing code to create a development plan by dividing the implementation steps into small steps of 5-6 stages. Save the plan in a `docs/[feature]_[summary].md` file. (Do not modify code at this stage.)
3.  **Plan Review**: Review the created `[feature]_[summary].md` file. If there are items that need modification, modify them directly or request changes from the Agent.
4.  **Step-by-Step Implementation**: Request code implementation step by step to the Agent based on `[feature]_[summary].md`. (The quality of the result improves when requested in appropriately small steps.) (It is recommended to commit & push in step units)
5.  **Content Review**: Review the modified content with Diff. (You can review it directly or with other tools such as Claude Code.)
6.  **Plan Update**: If the development plan is modified during the implementation process, reflect it in the .md file to keep the document and implementation status consistent. (After the implementation is finished, you can have the Agent update the .md with the actual implemented content.)
7.  **Testing and Static Analysis**: Perform testing and static analysis.
8.  **PR Creation**: Create a PR when testing and static analysis are complete.
9.  **Automatic Review**: A review of the PR is performed automatically by Claude. (Request if there is no setting in the repo)
10. **Review Reflection**: Check the review content on GitHub and make necessary corrections.
11. **Partner Review Request**: Request a review from a Partner as well.
12. **Merge**: Merge when the Partner approves.
```