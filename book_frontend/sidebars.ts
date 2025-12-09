import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Foundations',
      link: {type: 'generated-index'},
      items: [
        'part1/chapter1.1',
        'part1/chapter1.2'
      ],
    },
    {
      type: 'category',
      label: 'ROS2',
      link: {type: 'generated-index'},
      items: [
        'module1-ros2/index',
        'part2/chapter2.1',
        'part2/chapter2.2'
      ],
    },
    {
      type: 'category',
      label: 'Simulation',
      link: {type: 'generated-index'},
      items: ['module2-digital-twin/index'],
    },
    {
      type: 'category',
      label: 'NVIDIA Isaac',
      link: {type: 'generated-index'},
      items: [
        'module3-ai-robot-brain/index',
        'part3/chapter3.1',
        'part3/chapter3.2'
      ],
    },
    {
      type: 'category',
      label: 'Humanoids',
      link: {type: 'generated-index'},
      items: [],
    },
    {
      type: 'category',
      label: 'VLA',
      link: {type: 'generated-index'},
      items: [
        'module4-vla/index',
        'part4/chapter4.1',
        'part4/chapter4.2'
      ],
    },
    {
      type: 'category',
      label: 'Hardware',
      link: {type: 'generated-index'},
      items: ['hardware-lab'],
    },
    {
      type: 'category',
      label: 'Capstone',
      link: {type: 'generated-index'},
      items: ['capstone/index'],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
