# Research: Floating RAG Chatbot UI for Docusaurus Book

## Decision: Floating Chatbot Component Architecture
**Rationale**: Using a React component that renders globally across all Docusaurus pages provides the most straightforward approach to implement the floating chatbot functionality without modifying existing book content.

## Decision: Positioning Strategy
**Rationale**: CSS fixed positioning with bottom/right coordinates ensures the chatbot icon remains visible during scrolling while staying in the bottom-right corner as specified in requirements.

## Decision: State Management
**Rationale**: React useState hook provides simple and efficient state management for the open/closed state of the chat interface without requiring complex state management libraries.

## Decision: Styling Approach
**Rationale**: CSS modules or inline styles integrated with Docusaurus theme variables ensure visual consistency with the existing book design while maintaining maintainability.

## Decision: API Integration
**Rationale**: Using fetch or axios to connect with the existing FastAPI chat endpoint provides a direct integration path without requiring new backend infrastructure.

## Alternatives Considered

1. **Separate floating component vs. modifying layout**:
   - Chosen: Separate component for minimal impact on existing code
   - Alternative: Modifying Docusaurus layout directly (rejected due to high impact on existing code)

2. **CSS-in-JS vs. CSS modules vs. inline styles**:
   - Chosen: CSS modules for theme consistency
   - Alternative: Inline styles for simplicity (considered but CSS modules preferred for maintainability)

3. **Native fetch vs. axios for API calls**:
   - Chosen: Native fetch for minimal dependencies
   - Alternative: Axios for more features (considered but fetch sufficient for this use case)

## Technical Unknowns Resolved

1. **Docusaurus component integration**: Docusaurus supports global components via the theme configuration or layout integration.

2. **Theme variable access**: Docusaurus provides CSS variables and theme context that can be accessed by custom components.

3. **Performance impact mitigation**: Lazy loading and conditional rendering will be used to minimize initial page load impact.