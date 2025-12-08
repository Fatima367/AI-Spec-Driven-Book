import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { searchBookContent, mockSearchBookContent } from '../../services/searchService';

/**
 * A reusable Search Input component
 * Designed to match the glassmorphism aesthetic of the book landing page
 */
const SearchInput = ({
  placeholder = 'Search Chapters',
  value = '',
  onChange,
  className = '',
  disabled = false,
  onSearch,
  useMock = true,  // Whether to use mock search or real API
  ...props
}) => {
  const [inputValue, setInputValue] = React.useState(value);
  const [isLoading, setIsLoading] = React.useState(false);
  const [searchResults, setSearchResults] = React.useState([]);
  const [focusedResultIndex, setFocusedResultIndex] = React.useState(-1);
  const searchId = React.useId(); // Unique ID for accessibility

  React.useEffect(() => {
    setInputValue(value);
  }, [value]);

  const handleChange = (e) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    if (onChange) {
      onChange(newValue);
    }
  };

  const performSearch = async () => {
    if (!inputValue.trim()) return;

    setIsLoading(true);

    try {
      let results;
      if (useMock) {
        // Use mock search for development
        results = mockSearchBookContent(inputValue, 5);
      } else {
        // Use real API
        results = await searchBookContent(inputValue, 5);
      }

      setSearchResults(results.results);
      setFocusedResultIndex(-1); // Reset focused index

      if (onSearch) {
        onSearch(results);
      }
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
      setFocusedResultIndex(-1);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      performSearch();
    } else if (searchResults.length > 0) {
      // Handle navigation through search results
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setFocusedResultIndex(prev =>
          prev < searchResults.length - 1 ? prev + 1 : 0
        );
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setFocusedResultIndex(prev =>
          prev > 0 ? prev - 1 : searchResults.length - 1
        );
      } else if (e.key === 'Escape') {
        setSearchResults([]);
        setFocusedResultIndex(-1);
      }
    }
  };

  const handleClickSearch = () => {
    performSearch();
  };

  const baseClasses = clsx(
    'search-input',
    { 'search-input--disabled': disabled },
    className
  );

  return (
    <div
      className="search-input-container"
      role="search"
    >
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <input
          type="text"
          id={`search-input-${searchId}`}
          placeholder={placeholder}
          value={inputValue}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={disabled || isLoading}
          className={baseClasses}
          aria-label="Search book chapters"
          aria-autocomplete="list"
          aria-controls={`search-results-${searchId}`}
          aria-expanded={searchResults.length > 0}
          style={{
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderTopRightRadius: '0',
            borderBottomRightRadius: '0',
            padding: '12px 20px',
            color: 'white',
            fontSize: '1rem',
            width: '100%',
            outline: 'none',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
          }}
          {...props}
        />
        <button
          onClick={handleClickSearch}
          disabled={disabled || isLoading}
          aria-label={isLoading ? "Search in progress" : "Perform search"}
          style={{
            backgroundColor: 'rgba(0, 224, 255, 0.2)', // Electric Cyan with opacity
            border: '1px solid rgba(0, 224, 255, 0.3)',
            borderLeft: 'none',
            borderTopRightRadius: '50px',
            borderBottomRightRadius: '50px',
            padding: '12px 20px',
            color: '#00E0FF', // Electric Cyan
            cursor: (disabled || isLoading) ? 'not-allowed' : 'pointer',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
          }}
        >
          {isLoading ? '...' : 'Search'}
        </button>
      </div>

      {/* Display search results if any */}
      {searchResults.length > 0 && (
        <div
          id={`search-results-${searchId}`}
          role="listbox"
          aria-label="Search results"
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            backgroundColor: 'rgba(2, 5, 16, 0.9)',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            border: '1px solid rgba(0, 224, 255, 0.3)',
            borderRadius: '8px',
            zIndex: 30,
            maxHeight: '300px',
            overflowY: 'auto',
            marginTop: '5px'
          }}
        >
          {searchResults.map((result, index) => (
            <a
              key={result.id || index}
              href={result.url}
              role="option"
              aria-selected={focusedResultIndex === index}
              id={`search-result-${searchId}-${index}`}
              style={{
                display: 'block',
                padding: '10px 15px',
                color: 'white',
                textDecoration: 'none',
                borderBottom: index !== searchResults.length - 1 ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
                backgroundColor: focusedResultIndex === index
                  ? 'rgba(0, 224, 255, 0.2)'
                  : 'transparent',
              }}
              onMouseDown={(e) => e.preventDefault()} // Prevent loss of focus when clicking
            >
              <div style={{ fontWeight: 'bold' }}>{result.title}</div>
              <div style={{ fontSize: '0.9rem', color: '#A0A0B0', marginTop: '4px' }}>
                {result.chapter}
              </div>
            </a>
          ))}
        </div>
      )}

      <style jsx>{`
        .search-input-container {
          position: relative;
          display: inline-block;
          width: 100%;
        }

        .search-input {
          transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .search-input:focus {
          border-color: #00E0FF;
          box-shadow: 0 0 0 2px rgba(0, 224, 255, 0.2);
        }

        .search-input--disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
};

SearchInput.propTypes = {
  placeholder: PropTypes.string,
  value: PropTypes.string,
  onChange: PropTypes.func,
  className: PropTypes.string,
  disabled: PropTypes.bool,
  onSearch: PropTypes.func,
  useMock: PropTypes.bool,
};

export default SearchInput;