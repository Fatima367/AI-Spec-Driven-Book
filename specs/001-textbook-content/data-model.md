# Data Model: Textbook Content Structure

## Entities Overview

The textbook content structure is primarily file-based with a few user-related data elements for personalization features.

## Chapter Entity

**Definition**: A section of the textbook with specific learning content

**Attributes**:
- id: Unique identifier for the chapter
- title: Title of the chapter
- module: Module the chapter belongs to (Introduction, Module 1-4, Capstone, Hardware Lab)
- content: The MDX content including all required elements
- wordCount: Number of words in the chapter (500-1000)
- learningObjectives: Array of learning objectives for the chapter
- codeExamples: Array of code blocks relevant to the chapter topic
- diagrams: Array of Mermaid diagrams or other visual elements
- simulationSection: Content for "Try it yourself" simulation section
- buttons: Personalization buttons included at the top

**Relationships**: Belongs to a Module entity

## Module Entity

**Definition**: A collection of related chapters covering a specific topic area

**Attributes**:
- id: Unique identifier for the module
- title: Title of the module (e.g., "Module 1: The Robotic Nervous System (ROS 2)")
- chapters: Array of Chapter entities
- category: Sidebar category (Foundations, ROS2, Simulation, NVIDIA Isaac, Humanoids, VLA, Hardware, Capstone)

**Relationships**: Contains multiple Chapter entities

## Sidebar Category Entity

**Definition**: A grouping mechanism in Docusaurus that organizes chapters by topic area

**Attributes**:
- id: Unique identifier for the category
- title: Display title for the category
- position: Order in the sidebar navigation
- chapters: Array of Chapter entities belonging to this category

## Hardware Specification Entity

**Definition**: Technical requirements for workstation and edge computing hardware needed for the course

**Attributes**:
- id: Unique identifier for the hardware spec
- type: Type of hardware (Workstation, Edge Kit)
- category: Subcategory (e.g., "RTX 4070+", "Jetson Orin")
- requirements: Detailed technical specifications
- recommendations: Recommended configurations
- warnings: Critical requirements that must be met

## User Profile Entity (for personalization)

**Definition**: User information used for content personalization

**Attributes**:
- id: Unique user identifier
- background: Software/hardware background information
- preferences: Content complexity preferences
- language: Preferred language settings

**Relationships**: Associated with personalization features in chapters

## File Structure Model

The textbook content is organized as a file-based structure:

```
book_frontend/docs/
├── intro.mdx
├── module1-ros2/
│   ├── index.mdx
│   └── _category_.json
├── module2-digital-twin/
│   ├── index.mdx
│   └── _category_.json
├── module3-ai-robot-brain/
│   ├── index.mdx
│   └── _category_.json
├── module4-vla/
│   ├── index.mdx
│   └── _category_.json
├── capstone/
│   ├── index.mdx
│   └── _category_.json
├── hardware-lab.mdx
└── _category_.json
```

Each `_category_.json` file defines the category title and position in the sidebar.