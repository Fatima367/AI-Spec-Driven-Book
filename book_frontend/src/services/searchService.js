/**
 * Search API service function for the book landing page
 * Implements the contract from contracts/search-api.yaml
 */

/**
 * Searches across all book content
 * @param {string} query - The search query string
 * @param {number} limit - Maximum number of results to return (default: 10)
 * @returns {Promise<Object>} Search results with format matching the contract
 */
export const searchBookContent = async (query, limit = 10) => {
  // Validate input parameters
  if (!query || typeof query !== 'string' || query.trim().length === 0) {
    throw new Error('Search query is required and must be a non-empty string');
  }

  if (typeof limit !== 'number' || limit <= 0) {
    limit = 10; // Default to 10 if invalid limit provided
  }

  try {
    // In a real implementation, this would call the actual search API
    // For now, we'll simulate the API call with mock data
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        limit: limit,
      }),
    });

    if (!response.ok) {
      throw new Error(`Search API request failed with status ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error performing search:', error);
    
    // Return mock data in case of error
    // In a real implementation, we would handle the error appropriately
    return {
      results: [],
      total: 0,
    };
  }
};

/**
 * Mock search function for frontend testing
 * This simulates the search behavior without requiring a backend API
 */
export const mockSearchBookContent = (query, limit = 10) => {
  // In a real implementation, this would search through actual book content
  // For now, we'll return some mock results based on the query
  const mockResults = [
    {
      id: '1',
      title: 'Introduction to Physical AI',
      content: 'Physical AI represents a paradigm shift from traditional AI models confined to digital environments to intelligent systems that operate in the three-dimensional world we inhabit.',
      url: '/docs/intro',
      chapter: 'Introduction',
      score: 0.95
    },
    {
      id: '2',
      title: 'ROS 2: The Robotic Nervous System',
      content: 'You\'ll master the middleware that enables robot control, learning ROS 2 Nodes, Topics, and Services.',
      url: '/docs/module1-ros2/',
      chapter: 'Module 1: ROS 2',
      score: 0.87
    },
    {
      id: '3',
      title: 'Digital Twin Simulations',
      content: 'Simulation environments that provide physics engines and realistic rendering for robot development.',
      url: '/docs/module2-digital-twin/',
      chapter: 'Module 2: Digital Twin',
      score: 0.82
    },
    {
      id: '4',
      title: 'AI-Robot Brain with NVIDIA Isaac',
      content: 'Advanced perception and training with NVIDIA Isaac Sim for photorealistic simulation and synthetic data generation.',
      url: '/docs/module3-ai-robot-brain/',
      chapter: 'Module 3: AI-Robot Brain',
      score: 0.78
    },
    {
      id: '5',
      title: 'Vision-Language-Action Models',
      content: 'Systems that understand natural language commands and translate them into physical actions.',
      url: '/docs/module4-vla/',
      chapter: 'Module 4: VLA',
      score: 0.75
    }
  ];

  // Filter results based on query (simple text matching)
  const filteredResults = mockResults.filter(result => 
    result.title.toLowerCase().includes(query.toLowerCase()) || 
    result.content.toLowerCase().includes(query.toLowerCase()) ||
    result.chapter.toLowerCase().includes(query.toLowerCase())
  );

  // Limit the number of results
  const limitedResults = filteredResults.slice(0, limit);

  return {
    results: limitedResults,
    total: filteredResults.length,
  };
};

export default {
  searchBookContent,
  mockSearchBookContent,
};