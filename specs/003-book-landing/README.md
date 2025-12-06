# Book Landing Page with Glassmorphism Aesthetic

## Overview
This feature implements a visually stunning landing page for the "Physical AI & Humanoid Robotics" textbook with a dark glassmorphism aesthetic. The design features a central glass card with book information, glowing background spheres, and a modern UI that creates a compelling first impression for visitors.

## Features
- **Dark Glassmorphism Design**: Uses `backdrop-filter: blur(25px)` for a frosted glass effect
- **Glowing Background Spheres**: 3 large, animated spheres with radial gradients using Electric Cyan (#00E0FF) and Neon Magenta (#D600FF)
- **Responsive Layout**: Fully responsive design that works on mobile, tablet, and desktop
- **Search Functionality**: Integrated search that allows users to find specific chapters
- **Navigation**: Direct links to chapters, login, and signup pages
- **Call-to-Action**: Prominent "START READING" button with gradient styling

## Components
- `GlassmorphismCard`: The central card with book information and styling
- `BackgroundSpheres`: Animated background elements with glowing effects
- `NavigationLinks`: Top-right navigation links with icons
- `CTAButton`: Gradient button to start reading the book
- `SearchInput`: Glassmorphism-styled search input with real-time results

## Styling
- Custom CSS for glassmorphism effects
- Theme colors: Deep void navy/black (#020510) background with Electric Cyan and Neon Magenta accents
- Responsive design using media queries
- Animated elements for dynamic visual appeal

## API Integration
- Search functionality integrated with the book content API
- Follows the contract specified in `contracts/search-api.yaml`

## Accessibility
- Proper contrast ratios for text readability
- Semantic HTML structure
- Keyboard navigation support

## Performance
- Optimized animations using CSS transforms and opacity
- Efficient rendering of background elements
- Lazy loading for components where appropriate

## How to Run
1. Navigate to the `book_frontend` directory
2. Install dependencies with `npm install`
3. Start the development server with `npm run start`
4. Visit `http://localhost:3000` to see the landing page

## Testing
Run tests with `npm run test` to verify all components are working correctly.