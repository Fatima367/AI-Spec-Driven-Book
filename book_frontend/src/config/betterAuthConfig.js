/**
 * BetterAuth configuration for the Physical AI & Humanoid Robotics textbook application
 * This configuration defines the authentication endpoints and database connection
 */

// This would be used in a Node.js environment with BetterAuth
// Since we're using a Python backend, this serves as documentation of the API contract

const betterAuthConfig = {
  database: {
    url: process.env.DATABASE_URL || "postgresql://username:password@localhost:5432/your_db",
    type: "postgresql"
  },
  // Define the API endpoints that match our Python FastAPI implementation
  api: {
    baseUrl: process.env.API_BASE_URL || "https://ai-spec-driven-book-backend.up.railway.app/api/v1",
    prefix: "/auth"
  },
  // User schema extensions for background information
  user: {
    fields: {
      // Standard fields
      email: true,
      firstName: true,
      lastName: true,
      // Extended fields for background data
      softwareExperience: true,
      hardwareExperience: true,
      technicalBackground: true,
      primaryProgrammingLanguage: true,
      backgroundCompleted: true,
      // Personalization fields
      learningMode: true,
      difficultyLevel: true,
      focusArea: true
    }
  },
  // Session configuration
  session: {
    expiresIn: 24 * 60 * 60, // 24 hours
    updateAge: 24 * 60 * 60, // 24 hours
  },
  // Email verification settings
  emailVerification: {
    enabled: true,
  },
  // Password settings
  password: {
    enabled: true,
    // Minimum requirements
    minLength: 8,
    requireSpecialChars: false,
  },
  // OAuth providers (if needed)
  socialProviders: {
    // google: {
    //   clientId: process.env.GOOGLE_CLIENT_ID,
    //   clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    // },
  },
  // Rate limiting
  rateLimit: {
    window: 15 * 60 * 1000, // 15 minutes
    max: 100, // 100 requests per window
  },
  // Hooks for custom logic
  hooks: {
    createUser: async (user) => {
      // Custom logic for creating user with background data
      console.log("Creating user with background data:", user);
    },
    updateUser: async (user) => {
      // Custom logic for updating user background data
      console.log("Updating user with background data:", user);
    }
  }
};

module.exports = betterAuthConfig;