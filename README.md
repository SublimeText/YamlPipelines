# Yaml Pipelines for Sublime Text

Syntax highlighting definitions for YAML pipeline files, like GitHub Actions and AzureDevops, Drone CI, GitLab CICD, AWS templates etc.
Includes a small plugin to automatically apply the GitHub Actions filetype when loading or saving a YAML file in a `.github/workflows` folder.

Why not just use the default YAML syntax definition? Because it doesn't highlight conditions, variables or embedded Bash or PowerShell scripts!

The Kong syntax highlights route path regular expressions using the [PackageDev](https://packagecontrol.io/packages/PackageDev) package,
which must be installed for that part to work.

The PowerShell embeds — `Embeddings/PowerShell (Folded)`, `PowerShell (Github Actions)` and
`PowerShell (Github Actions Folded)` — extend
`Packages/PowerShell/PowerShell.sublime-syntax`, so the
[PowerShell](https://packagecontrol.io/packages/PowerShell) package must be installed for them to load.
Without it, Sublime Text shows a modal `unable to read base syntax
"Packages/PowerShell/PowerShell.sublime-syntax"` error for each of the three at install time, and
embedded PowerShell in GitHub Actions workflows is not highlighted.
