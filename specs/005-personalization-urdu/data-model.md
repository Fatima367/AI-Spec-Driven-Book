# Data Model: Personalization and Urdu Translation

## Entities

### User Profile
- **Entity Name**: UserProfile
- **Fields**:
  - id (string): Unique user identifier from BetterAuth
  - software_background (string): User's software background level (beginner/intermediate/advanced)
  - hardware_background (string): User's hardware background level (beginner/intermediate/advanced)
  - learning_preferences (object): User's preferred learning settings
    - difficulty_level (string): Preferred content difficulty (basic/intermediate/advanced)
    - focus_area (string): Learning focus (theory/practice)
    - learning_mode (string): Learning mode (beginner/advanced)
  - created_at (datetime): Profile creation timestamp
  - updated_at (datetime): Last profile update timestamp
- **Relationships**: One-to-many with personalization history
- **Validation Rules**: Background fields must be one of the defined values
- **State Transitions**: Profile can be updated by the user

### Chapter Content
- **Entity Name**: ChapterContent
- **Fields**:
  - id (string): Unique identifier for the chapter
  - original_content (string): Original English content
  - urdu_content (string): Urdu translated content (nullable)
  - personalization_rules (object): Rules for personalizing content based on user profile
  - file_path (string): Path to the original MDX file
  - urdu_file_path (string): Path to the Urdu MDX file (nullable)
  - created_at (datetime): Content creation timestamp
  - updated_at (datetime): Last content update timestamp
- **Relationships**: One-to-many with PersonalizedContent
- **Validation Rules**: Original content must exist, file paths must be valid
- **State Transitions**: Content can be updated when original changes

### Personalized Content
- **Entity Name**: PersonalizedContent
- **Fields**:
  - id (string): Unique identifier
  - user_id (string): Reference to UserProfile
  - chapter_id (string): Reference to ChapterContent
  - personalized_content (string): Personalized version of the chapter
  - personalization_params (object): Parameters used for personalization
  - generated_at (datetime): Timestamp when personalized content was generated
  - expires_at (datetime): Expiration timestamp for cached content
- **Relationships**: Many-to-one with UserProfile and ChapterContent
- **Validation Rules**: Must reference valid user and chapter
- **State Transitions**: Content is generated on demand and can expire

### Translation Cache
- **Entity Name**: TranslationCache
- **Fields**:
  - id (string): Unique identifier
  - chapter_id (string): Reference to ChapterContent
  - urdu_content (string): Cached Urdu translation
  - generated_at (datetime): Timestamp when translation was generated
  - expires_at (datetime): Expiration timestamp for cached translation
  - generation_status (string): Status of translation (pending/completed/failed)
- **Relationships**: Many-to-one with ChapterContent
- **Validation Rules**: Content must be valid Urdu text when status is completed
- **State Transitions**: Pending → Completed/Failed, can be regenerated when expired