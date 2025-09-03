---
lang: en
source_lang: kr
source_sha: ac9ae8d09e3a127a4d0a9130a7e495831ea1dc7c33044a909e7c6c249d3aab77
---
```markdown
# Git Style Guide

## Commit Message
- Use **sentence-style, concise** commit messages. (Conventional Commits not used)
  Ex: `Fix PS1 prompt escaping for zsh.`
- Adhere to the **3-line rule** in PR descriptions: summarize changes, scope of impact, and rollback method.

## Branch Naming
- Clarify the purpose of branches by using prefixes such as `feature/`, `bugfix/`, and `hotfix/`.
- Use only lowercase English letters, numbers, and hyphens (-) in branch names.
  Ex: `feature/user-authentication`, `bugfix/login-error-handling`

## Pull Request (PR)
- The PR title should clearly summarize the changes.
- The PR description should include the following:
  - **Summary of Changes**: Briefly describe what you changed.
  - **Scope of Impact**: Explain which parts are affected by the changes.
  - **Rollback Method**: Explain how to roll back if a problem occurs.

## Code Review
- Reviews should be **constructive feedback**, focusing on the code rather than the individual.
- Clearly explain **"Why"** and **"How"**.
- Review comments should be **actionable**.
- **Don't forget to praise.**

## Development Process
1.  **Feature Analysis**: Analyze the context of the Jira ticket.
2.  **Development Plan Establishment**: Analyze existing code and create a development plan by dividing the implementation steps into small steps of 5 to 6 stages. Save the plan in a `docs/[feature]_[summary].md` file. (Do not modify the code at this stage.)
3.  **Plan Review**: Review the created `[feature]_[summary].md` file. If there are items that need to be modified, modify them directly or request the Agent to change them.
4.  **Step-by-Step Implementation**: Request the Agent to implement the code step by step based on `[feature]_[summary].md`. (The quality of the output improves when requested in appropriately small steps.) (Commit & push are recommended in step units.)
5.  **Content Review**: Review the modified content with Diff. (You can review it directly or with other tools such as Claude Code.)
6.  **Plan Update**: If the development plan is modified during the implementation process, reflect it in the .md file to keep the document consistent with the implementation status. (After the implementation is complete, you can have the Agent update the .md file with the actual implemented content.)
7.  **Testing and Static Analysis**: Perform testing and static analysis.
8.  **PR Creation**: Create a PR when testing and static analysis are complete.
9.  **Automatic Review**: A review of the PR is automatically performed by Claude. (Request if there is no setting in the repo)
10. **Review Reflection**: Check the review contents on GitHub and make necessary corrections.
11. **Partner Review Request**: Request a review from a Partner as well.
12. **Merge**: Merge when the Partner approves.
```