# Quickstart Guide: Textbook Content Structure

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager
- Git

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Spec-Driven-Book
   ```

2. **Navigate to the book frontend directory**
   ```bash
   cd book_frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

The textbook will be available at `http://localhost:3000`

## Creating New Chapters

1. **Create a new MDX file** in the appropriate module directory:
   ```
   book_frontend/docs/module1-ros2/new-chapter.mdx
   ```

2. **Follow the required structure**:
   ```md
   ---
   title: Chapter Title
   sidebar_position: 1
   ---

   import { PersonalizeButton, UrduTranslationButton } from '@site/src/components/PersonalizationButtons';

   <PersonalizeButton />
   <UrduTranslationButton />

   # Chapter Title

   ## Learning Objectives
   - Objective 1
   - Objective 2

   ## Content
   Your chapter content here...

   ## Try it yourself
   Simulation or hands-on exercise instructions...
   ```

3. **Add to sidebar** by updating the `_category_.json` file in the module directory or updating `sidebars.js`.

## Adding Mermaid Diagrams

Include Mermaid diagrams in your MDX files:
```md
import Mermaid from '@theme/Mermaid';

<Mermaid chart={`graph TD;
    A[ROS 2 Node] --> B[ROS 2 Node];
    A --> C[Topic];
    B --> C;
    D[Service] --> A;
    D --> B;
`} />
```

## Using Admonitions for Hardware Requirements

Use Docusaurus admonitions for hardware specs:
```md
:::tip
Recommended workstation: NVIDIA RTX 4070 Ti (12GB VRAM) or higher
:::

:::danger
Critical requirement: Minimum 64GB RAM DDR5 for complex scene rendering
:::
```

## Running the Build

To build the static site for deployment:
```bash
npm run build
```

The built site will be in the `build/` directory and can be served statically or deployed to GitHub Pages.