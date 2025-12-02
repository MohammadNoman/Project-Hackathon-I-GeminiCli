# Research: Technical Stack Clarifications

**Feature**: Physical AI & Humanoid Robotics Textbook Platform
**Branch**: `001-textbook-platform`
**Date**: 2025-12-01

## Resolved "NEEDS CLARIFICATION" from plan.md

### 1. Python Version

*   **Decision**: Python 3.11
*   **Rationale**: Python 3.11 offers significant performance improvements over previous versions and introduces new features beneficial for FastAPI and AI-related dependencies. It is a stable and widely supported version.
*   **Alternatives considered**: Python 3.10 (slightly older, less performance), Python 3.12 (newer, but some libraries might not have full compatibility yet).

### 2. Node.js/NPM/Yarn Versions

*   **Decision**: Node.js v20 (LTS), npm (latest stable, bundled with Node.js) or Yarn v1/v3 (if specific advanced features are needed, but npm is sufficient for Docusaurus).
*   **Rationale**: Node.js v20 is the current Long Term Support (LTS) release, providing stability and continued maintenance, which is ideal for a project base. npm is the default package manager and generally sufficient for Docusaurus projects. Yarn v1 is widely used, and v3 offers modern features but might introduce complexity. Sticking with npm for simplicity in a hackathon is pragmatic.
*   **Alternatives considered**: Node.js v18 (older LTS), Yarn package manager.

### 3. Frontend Testing Framework

*   **Decision**: Jest and React Testing Library
*   **Rationale**: Jest is a popular and powerful JavaScript testing framework, widely used in React ecosystems for unit and integration testing. React Testing Library provides utilities that encourage good testing practices by focusing on testing component behavior from a user's perspective, rather than implementation details. Docusaurus is built on React, making these tools a natural fit.
*   **Alternatives considered**: Cypress (for end-to-end testing, but might be overkill for initial unit/integration focus), Enzyme (older React testing utility).