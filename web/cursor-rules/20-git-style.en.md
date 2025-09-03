---
lang: en
source_lang: kr
source_sha: ac9ae8d09e3a127a4d0a9130a7e495831ea1dc7c33044a909e7c6c249d3aab77
---
```md
# Git Style Guide

## Commit Messages
- Use **sentence-style, concise** commit messages. (Conventional Commits not used)
  Ex: `Fix PS1 prompt escaping for zsh.`
- Adhere to the **3-line rule** in PR descriptions: change summary, scope of impact, rollback method.

## Branch Naming
- Clearly define the purpose of a branch by using prefixes such as `feature/`, `bugfix/`, `hotfix/`.
- Branch names should only use lowercase English letters, numbers, and hyphens (-).
  Ex: `feature/user-authentication`, `bugfix/login-error-handling`

## Pull Request (PR)
- PR titles should clearly summarize the changes.
- PR descriptions should include the following:
  - **Change Summary**: Briefly describe what was changed.
  - **Scope of Impact**: Describe what parts are affected by the changes.
  - **Rollback Method**: Describe how to rollback in case of issues.

## Code Review
- Reviews should be **constructive feedback** and focus on the code, not the individual.
- Clearly explain **"Why"** and **"How"**.
- Review comments should be **actionable**.
- **Don't forget to praise.**

## Development Process
1.  **Feature Analysis**: Analyze the context of the Jira ticket.
2.  **Development Plan**: Analyze existing code and create a development plan by dividing the implementation into small steps of 5-6 stages. Save the plan in a `docs/[feature]_[summary].md` file. (Do not modify the code at this stage.)
3.  **Plan Review**: Review the created `[feature]_[summary].md` file. If there are items that need modification, modify them directly or request changes from the Agent.
4.  **Step-by-Step Implementation**: Request code implementation from the Agent step-by-step based on `[feature]_[summary].md`. (The quality of the output improves when requests are made in appropriately small steps.) (Commit & push are recommended on a per-step basis.)
5.  **Content Review**: Review the modified content using Diff. (You can review it directly or with other tools such as Claude Code.)
6.  **Plan Update**: If the development plan is modified during the implementation process, reflect it in the .md file to keep the document consistent with the implementation status. (After the implementation is complete, you can have the Agent update the .md file with the actual implemented content.)
7.  **Testing and Static Analysis**: Perform testing and static analysis.
8.  **PR Creation**: Create a PR after testing and static analysis are complete.
9.  **Automatic Review**: A review of the PR is automatically performed by Claude. (Request if there is no setting in the repo)
10. **Review Reflection**: Check the review content on GitHub and make the necessary modifications.
11. **Partner Review Request**: Request a review from a Partner as well.
12. **Merge**: Merge when the Partner approves.
```