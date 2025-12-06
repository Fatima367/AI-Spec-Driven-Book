# Quick Start Guide: Book Landing Page

## Overview
This guide provides instructions for setting up, developing, and running the book landing page with glassmorphism aesthetic.

## Prerequisites
- Node.js (v18 or higher)
- npm or yarn package manager
- Git
- Basic knowledge of React and Docusaurus

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Spec-Driven-Book
```

### 2. Navigate to the Book Frontend
```bash
cd book_frontend
```

### 3. Install Dependencies
```bash
npm install
# or
yarn install
```

### 4. Run the Development Server
```bash
npm run dev
# or
yarn dev
```

The landing page will be available at `http://localhost:3000` (or the next available port).

## Project Structure
```
book_frontend/
├── src/
│   ├── components/
│   │   ├── BookLanding/
│   │   │   ├── GlassmorphismCard.jsx
│   │   │   ├── BackgroundSpheres.jsx
│   │   │   └── NavigationLinks.jsx
│   │   └── common/
│   │       ├── Button.jsx
│   │       └── SearchInput.jsx
│   ├── pages/
│   │   └── BookLandingPage.jsx
│   ├── styles/
│   │   ├── globals.css
│   │   └── glassmorphism.css
│   └── utils/
│       └── responsive.js
└── tests/
    └── ...
```

## Key Components

### BookLandingPage
The main page component that orchestrates all other components.

### GlassmorphismCard
The central UI container with the frosted glass effect. Key CSS properties:
- `background: rgba(255,255,255,0.03)`
- `backdrop-filter: blur(25px)`
- `border: 1px solid rgba(255,255,255,0.1)`

### BackgroundSpheres
Background component with 3 large, glowing, iridescent spheres using radial gradients.

## Development Workflow

### 1. Modifying Styling
- Edit `src/styles/glassmorphism.css` for glassmorphism-specific styles
- Use CSS responsive design
- Add global styles in `src/styles/globals.css`

### 2. Updating Content
- Content comes from the textbook structure spec
- Update content in the component props or data fetching layer

### 3. Adding New Features
- Create new components in the appropriate directories
- Follow the existing component structure and naming conventions
- Ensure all new code passes accessibility standards

## Testing

### Run Component Tests
```bash
npm run test
# or
yarn test
```

### Test Specific Component
```bash
npm run test -- src/components/BookLanding/GlassmorphismCard.test.js
# or
yarn test -- src/components/BookLanding/GlassmorphismCard.test.js
```

## Building for Production
```bash
npm run build
# or
yarn build
```

## Deploying
The project is designed to deploy to GitHub Pages following the constitution requirements.

## Troubleshooting

### Glassmorphism Effect Not Working
- Check if `backdrop-filter` is supported in the target browsers
- For older browsers, consider CSS fallbacks using the `@supports` rule

### Performance Issues
- Limit the number of animated elements
- Use CSS transforms and opacity for animations (avoid layout changes)
- Reduce blur intensity if performance is critical

### Responsive Issues
- Verify media queries are properly set up
- Test on various screen sizes during development
- Use responsive units (rem, %, vw, vh) instead of fixed units when possible