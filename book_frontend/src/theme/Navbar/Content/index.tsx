import React, {type ReactNode} from 'react';
import clsx from 'clsx';
import {
  useThemeConfig,
  ErrorCauseBoundary,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import {
  splitNavbarItems,
  useNavbarMobileSidebar,
} from '@docusaurus/theme-common/internal';
import NavbarItem, {type Props as NavbarItemConfig} from '@theme/NavbarItem';
import NavbarColorModeToggle from '@theme/Navbar/ColorModeToggle';
import SearchBar from '@theme/SearchBar';
import NavbarMobileSidebarToggle from '@theme/Navbar/MobileSidebar/Toggle';
import NavbarLogo from '@theme/Navbar/Logo';
import NavbarSearch from '@theme/Navbar/Search';
import { useAuth } from '../../../contexts/AuthContext'; // Import auth hook

import styles from './styles.module.css';

function useNavbarItems() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().navbar.items as NavbarItemConfig[];
}

function NavbarItems({items}: {items: NavbarItemConfig[]}): ReactNode {
  return (
    <>
      {items.map((item, i) => (
        <ErrorCauseBoundary
          key={i}
          onError={(error) =>
            new Error(
              `A theme navbar item failed to render.
Please double-check the following navbar item (themeConfig.navbar.items) of your Docusaurus config:
${JSON.stringify(item, null, 2)}`,
              {cause: error},
            )
          }>
          <NavbarItem {...item} />
        </ErrorCauseBoundary>
      ))}
    </>
  );
}

function NavbarContentLayout({
  left,
  right,
}: {
  left: ReactNode;
  right: ReactNode;
}) {
  return (
    <div className="navbar__inner">
      <div
        className={clsx(
          ThemeClassNames.layout.navbar.containerLeft,
          'navbar__items',
        )}>
        {left}
      </div>
      <div
        className={clsx(
          ThemeClassNames.layout.navbar.containerRight,
          'navbar__items navbar__items--right',
        )}>
        {right}
      </div>
    </div>
  );
}

export default function NavbarContent(): ReactNode {
  const mobileSidebar = useNavbarMobileSidebar();
  const { user, isLoading, isAuthenticated, signOut } = useAuth(); // Get authentication state

  const items = useNavbarItems();
  const [leftItems, rightItems] = splitNavbarItems(items);

  // Separate static navbar items from auth-related items
  const staticRightItems = rightItems.filter(item => {
    return !(item.to === '/login' || item.to === '/signup' ||
             item.href === '/login' || item.href === '/signup');
  });

  // Filter out auth-related items for the unauthenticated state
  const authRelatedItems = rightItems.filter(item =>
    item.to === '/login' || item.to === '/signup' ||
    item.href === '/login' || item.href === '/signup'
  );

  const searchBarItem = items.find((item) => item.type === 'search');

  // Handle logout with proper error handling
  const handleLogout = async () => {
    if (signOut) {
      try {
        await signOut();
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
  };

  return (
    <NavbarContentLayout
      left={
        // TODO stop hardcoding items?
        <>
          {!mobileSidebar.disabled && <NavbarMobileSidebarToggle />}
          <NavbarLogo />
          <NavbarItems items={leftItems} />
        </>
      }
      right={
        // TODO stop hardcoding items?
        // Ask the user to add the respective navbar items => more flexible
        <>
          {/* Authentication controls - show either login/signup or logout based on auth status */}
          <div className="navbar__item">
            {isAuthenticated ? (
              <button
                onClick={handleLogout}
                style={{
                  color: 'white',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  padding: 'var(--ifm-navbar-item-padding-vertical) var(--ifm-navbar-item-padding-horizontal)',
                  fontSize: 'var(--ifm-font-size-base)',
                }}
              >
                Logout
              </button>
            ) : (
              <div style={{ display: 'flex', gap: '15px' }}>
                <NavbarItems items={authRelatedItems} />
              </div>
            )}
          </div>

          {/* Render other static items (like GitHub) regardless of auth status */}
          <NavbarItems items={staticRightItems} />
          <NavbarColorModeToggle className={styles.colorModeToggle} />
          {!searchBarItem && (
            <NavbarSearch>
              <SearchBar />
            </NavbarSearch>
          )}
        </>
      }
    />
  );
}
