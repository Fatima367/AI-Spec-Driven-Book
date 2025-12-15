import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Learn Physical AI with Humanoid Robotics',
  favicon: 'img/FavIcon-logo2.png',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    // v4: true, // Temporarily disabled due to theme resolution issues
  },

  url: 'https://physical-ai-n-humanoid-robotics.vercel.app/', // <--- Update this with your actual Vercel deployment URL
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel root deployment, it should often be '/'
  baseUrl: '/',

  // Add the mermaid theme
  themes: ['@docusaurus/theme-mermaid'],

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Fatima367', // Usually your GitHub org/user name.
  projectName: 'AI-Spec-Driven-Book', // Usually your repo name.

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'], // Adding Urdu locale
    localeConfigs: {
      en: {
        label: 'English',
      },
      ur: {
        label: 'اردو',
      },
    },
  },

  plugins: [
    './src/plugins/personalization-plugin',
    './src/plugins/auth-plugin',
  ],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Exclude draft files but include Urdu files for direct access
          exclude: ['**/_*.{md,mdx}'],
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Fatima367/AI-Spec-Driven-Book/tree/main/book_frontend',
          // Use different sidebars based on locale
          sidebarItemsGenerator: async ({ defaultSidebarItemsGenerator, ...args }) => {
            if (args.locale === 'ur') {
              // For Urdu locale, use the urduSidebar
              const sidebarConfig = await import('./sidebars.ts');
              const urduSidebar = sidebarConfig.default.urduSidebar;
              return urduSidebar;
            }
            // For other locales, use default behavior
            return defaultSidebarItemsGenerator(args);
          },
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Fatima367/AI-Spec-Driven-Book/tree/main/book_frontend',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: [
            './src/css/custom.css',
            './src/styles/globals.css',
            './src/styles/glassmorphism.css'
          ],
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/Textbook Cover Physical AI & Humanoid Robotics.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Textbook Logo',
        src: 'img/FavIcon-logo2.png',
      },
      hideOnScroll: false, // Disable navbar hiding on scroll
      items: [
        {
          to: '/docs/intro',
          label: 'Book',
          position: 'left',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          to: '/login',
          label: 'Login',
          position: 'right',
        },
        {
          to: '/signup',
          label: 'Signup',
          position: 'right',
        },
        {
          href: 'https://github.com/Fatima367/AI-Spec-Driven-Book',
          label: 'GitHub',
          position: 'right',
        },

      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Book Content',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Module 1: ROS2',
              to: '/docs/module1-ros2/',
            },
            {
              label: 'Module 2: Digital Twin',
              to: '/docs/module2-digital-twin/',
            },
            {
              label: 'Module 3: AI Robot Brain',
              to: '/docs/module3-ai-robot-brain/',
            },
            {
              label: 'Module 4: VLA',
              to: '/docs/module4-vla/',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Documentation',
              to: '/docs/',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/gemini-book/AI-Spec-Driven-Book',
            },
          ],
        },
        {
          title: 'Legal',
          items: [
            {
              label: 'Privacy Policy',
              to: '/privacy',
            },
            {
              label: 'Terms of Service',
              to: '/terms',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Made by Fatima Faisal.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;