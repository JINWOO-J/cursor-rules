---
lang: en
source_lang: kr
source_sha: ac9ae8d09e3a127a4d0a9130a7e495831ea1dc7c33044a909e7c6c249d3aab77
---
```markdown
# Git Style Guide

## Commit Messages
- Use **sentence-style, concise** commit messages. (Conventional Commits not used)
  Ex: `Fix PS1 prompt escaping for zsh.`
- Adhere to the **3-line rule** in PR descriptions: change summary, scope of impact, rollback method.

## Branch Naming
- Clearly indicate the purpose of the branch by using prefixes such as `feature/`, `bugfix/`, `hotfix/`.
- Branch names should only use lowercase English letters, numbers, and hyphens (-).
  Ex: `feature/user-authentication`, `bugfix/login-error-handling`

## Pull Request (PR)
- The PR title should clearly summarize the changes.
- The PR description should include the following:
  - **Change Summary**: Briefly describe what was changed.
  - **Scope of Impact**: Describe which parts are affected by the changes.
  - **Rollback Method**: Describe how to rollback if a problem occurs.

## Code Review
- Reviews should be **constructive feedback** and focus on the code, not the individual.
- Clearly explain **"Why"** and **"How"**.
- Review comments should be **actionable**.
- **Don't forget to praise.**

## Development Process
1.  **Feature Analysis**: Analyze the context of the Jira ticket.
2.  **Development Plan Establishment**: Analyze the existing code and create a development plan by dividing the implementation steps into small steps of 5-6 stages. The plan is saved in the `docs/[feature]_[summary].md` file. (No code modification is done at this stage.)
3.  **Plan Review**: Review the created `[feature]_[summary].md` file. If there are items that need modification, modify them directly or request the Agent to make changes.
4.  **Step-by-Step Implementation**: Request the Agent to implement the code step by step based on `[feature]_[summary].md`. (The quality of the output improves when requests are made in appropriately small steps.) (It is recommended to commit & push in step units.)
5.  **Content Review**: Review the modified content with Diff. (You can review it directly or with other tools such as Claude Code.)
6.  **Plan Update**: If the development plan is modified during the implementation process, reflect it in the .md to keep the document and the implementation status consistent. (After the implementation is finished, you can ask the Agent to update the .md with the actual implemented content.)
7.  **Testing and Static Analysis**: Perform testing and static analysis.
8.  **PR Creation**: Create a PR when testing and static analysis are completed.
9.  **Automatic Review**: A review of the PR is automatically performed by Claude. (Request if there is no setting in the repo)
10. **Review Reflection**: Check the review content on GitHub and make necessary corrections.
11. **Partner Review Request**: Request a review from a Partner as well.
12. **Merge**: Merge when the Partner approves.
```