# Data Model: Book Landing Page

## Entities

### 1. BookLandingPage
- **Description**: The main landing page component containing all UI elements
- **Fields**:
  - id: string (unique identifier for the page)
  - title: string (book title, e.g., "Physical AI & Humanoid Robotics")
  - subtitle: string (metadata like "Sci-Fi • Bestseller • 2024")
  - synopsis: string (book description)
  - backgroundImage: string (path to background image or gradient definition)
  - theme: Theme object (color scheme and styling properties)

### 2. GlassmorphismCard
- **Description**: The central UI container with frosted glass effect
- **Fields**:
  - id: string (unique identifier)
  - backgroundColor: string (semi-transparent white rgba(255,255,255,0.03))
  - backdropFilter: string (blur effect: blur(25px))
  - borderColor: string (thin white border with 10% opacity)
  - borderRadius: string (how rounded the edges are)
  - contentAlignment: string (how content is aligned within the card)

### 3. Theme
- **Description**: Color scheme and styling properties
- **Fields**:
  - backgroundColor: string (#020510 - deep void navy/black)
  - accentColor1: string (#00E0FF - electric cyan)
  - accentColor2: string (#D600FF - neon magenta)
  - textColorPrimary: string (#FFFFFF - pure white for titles)
  - textColorSecondary: string (#A0A0B0 - muted grey-blue for synopsis)
  - gradientStart: string (start color for gradient buttons)
  - gradientEnd: string (end color for gradient buttons)

### 4. NavigationLink
- **Description**: Links in the top-right of the glass card
- **Fields**:
  - id: string (unique identifier)
  - text: string (link text: "Chapters", "Login", "Signup")
  - url: string (destination URL)
  - position: string ("top-right" of the glass card)

### 5. CTAButton
- **Description**: The "START READING" button
- **Fields**:
  - id: string (unique identifier)
  - text: string ("START READING")
  - link: string (URL to Introduction chapter)
  - gradientStart: string (electric cyan #00E0FF)
  - gradientEnd: string (deep blue)
  - borderRadius: string (fully rounded pill shape)
  - textColor: string (white)
  - fontWeight: string (bold)
  - textTransform: string (uppercase)

### 6. SearchInput
- **Description**: Search field on the right side of the glass card
- **Fields**:
  - id: string (unique identifier)
  - placeholder: string ("Search Chapters")
  - position: string ("right side of the glass card")
  - styling: string (rounded outline style)

### 7. BackgroundSphere
- **Description**: Glowing, iridescent 3D spheres in the background
- **Fields**:
  - id: string (unique identifier)
  - size: string (large, specific dimensions)
  - position: Position object (coordinates in the background)
  - gradientColors: array (colors for radial gradients, typically cyan and magenta)
  - animation: string (how the sphere glows/changes)

### 8. Position
- **Description**: Coordinates for background elements
- **Fields**:
  - x: number (x-coordinate as percentage or value)
  - y: number (y-coordinate as percentage or value)
  - zIndex: number (layering order)

## Relationships

### BookLandingPage contains:
- One GlassmorphismCard
- Multiple NavigationLink elements (Chapters, Login, Signup)
- One CTAButton
- One SearchInput
- Multiple BackgroundSphere elements (typically 3)
- One Theme

### GlassmorphismCard contains:
- All content elements: title, subtitle, synopsis
- NavigationLink elements (positioned top-right)
- CTAButton (positioned as specified)
- SearchInput (positioned right side)

## Validation Rules

### BookLandingPage
- title must not be empty
- synopsis must not exceed 500 characters (for readability)
- theme must be properly defined

### GlassmorphismCard
- backgroundColor must use proper rgba format
- backdropFilter must include blur effect
- borderColor must have 10% opacity

### CTAButton
- link must be a valid URL
- text must not be empty
- gradient colors must be defined

### NavigationLink
- text must be one of: "Chapters", "Login", "Signup"
- url must be a valid URL

### BackgroundSphere
- Must have at least 3 spheres in the background
- Gradient colors must include both electric cyan and neon magenta

## State Transitions

### BookLandingPage
- Initial State: Loading (display loading state while content loads)
- Ready State: Content loaded and displayed
- Error State: Error occurred while loading content