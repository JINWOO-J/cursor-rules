---
lang: en
source_lang: kr
source_sha: ac9ae8d09e3a127a4d0a9130a7e495831ea1dc7c33044a909e7c6c249d3aab77
---
```yaml
title: Git Style Guide
description: Git style guide for development.
```

# Git Style Guide

## Commit Messages
- Use **sentence-style, concise** commit messages. (Conventional Commits not used)
  Ex: `Fix PS1 prompt escaping for zsh.`
- Adhere to the **3-line rule** in PR descriptions: change summary, scope of impact, and rollback method.

## Branch Naming
- Clearly state the purpose of the branch by using prefixes such as `feature/`, `bugfix/`, `hotfix/`.
- Use only lowercase English letters, numbers, and hyphens (-) for branch names.
  Ex: `feature/user-authentication`, `bugfix/login-error-handling`

## Pull Request (PR)
- The PR title should clearly summarize the changes.
- The PR description should include the following:
  - **Change Summary**: Briefly describe what was changed.
  - **Scope of Impact**: Describe which parts are affected by the changes.
  - **Rollback Method**: Describe how to roll back in case of issues.

## Code Review
- Reviews should be **constructive feedback**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**.
- Review comments should be **actionable**.
- **Don't forget to praise.**

## Development Process
1.  **Feature Analysis**: Analyze the context of the Jira ticket.
2.  **Develop a Plan**: Analyze existing code and create a development plan by dividing the implementation into small steps of 5-6 stages. Save the plan in a `docs/[feature]_[summary].md` file. (Do not modify code at this stage.)
3.  **Review the Plan**: Review the created `[feature]_[summary].md` file. If there are items that need to be modified, modify them directly or request changes from the Agent.
4.  **Step-by-Step Implementation**: Request code implementation from the Agent step by step based on `[feature]_[summary].md`. (The smaller the steps are, the better the quality of the results) (It is recommended to commit & push in step units)
5.  **Review Content**: Review the modified content with Diff. (You can review it directly or with other tools such as Claude Code.)
6.  **Update the Plan**: If the development plan is modified during the implementation process, reflect it in the .md file to keep the document and implementation status consistent. (After the implementation is complete, you can have the Agent update the .md file with the actual implemented content.)
7.  **Testing and Static Analysis**: Perform testing and static analysis.
8.  **Create PR**: Create a PR when testing and static analysis are complete.
9.  **Automated Review**: A review of the PR is automatically performed by Claude. (Request if there is no configuration in the repo)
10. **Reflect Review**: Check the review content in GitHub and make the necessary corrections.
11. **Request Partner Review**: Request a review from a Partner as well.
12. **Merge**: Merge when the Partner approves.
