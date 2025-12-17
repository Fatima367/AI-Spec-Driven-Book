# Personalization Feature Setup Guide

This guide will help you set up and test the AI-powered personalization feature for the Physical AI & Humanoid Robotics textbook.

## Prerequisites

- Python 3.10+
- Node.js 18+
- Gemini API Key from Google AI Studio

## Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install the new `google-generativeai` package along with other dependencies.

## Step 2: Configure Environment Variables

Update your `backend/.env` file with your Gemini API key:

```env
# Existing variables...
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=your_database_url

# Add Gemini API Key for personalization
GEMINI_API_KEY=your_gemini_api_key_here
```

### How to Get Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your `.env` file

## Step 3: Verify Installation

Run the test script to verify the personalization service is working:

```bash
cd backend
python -m pytest tests/test_gemini_personalization.py -v
```

Or run the standalone test:

```bash
cd backend
python tests/test_gemini_personalization.py
```

## Step 4: Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend should start successfully and log:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 5: Test Personalization API

You can test the personalization endpoint using curl or Postman:

```bash
# First, login to get a token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Use the token to test personalization
curl -X POST http://localhost:8000/api/v1/personalize/intro \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"user_preferences":{"learning_mode":"beginner"}}'
```

## Step 6: Test in Frontend

1. Start the frontend development server:
```bash
cd book_frontend
npm start
```

2. Navigate to any chapter (e.g., `http://localhost:3000/docs/intro`)

3. Login with your credentials

4. Click the "Personalize for Me" button

5. You should see:
   - Loading state: "Personalizing..."
   - Success message: "Content has been personalized for you based on your profile!"
   - The personalized content will be displayed

## How Personalization Works

### For Beginner Users
If your profile has `softwareExperience: "beginner"` OR `hardwareExperience: "beginner"`:

**Before:**
```markdown
ROS 2 (Robot Operating System 2) is a middleware framework for robotics applications.
It provides nodes, topics, and services for inter-process communication.
```

**After (Simplified):**
```markdown
Let's learn about ROS 2, which stands for Robot Operating System 2. Think of it as a
communication system that helps different parts of a robot talk to each other.

ROS 2 uses three main building blocks:
- **Nodes**: Think of these as individual workers, each doing a specific job
- **Topics**: These are like message boards where nodes can post and read messages
- **Services**: These are like asking a question and waiting for an answer

In simpler terms, imagine your robot as a team where each team member (node) can share
information through message boards (topics) or ask questions (services) to get help.
```

### For Advanced Users
If your profile has `softwareExperience: "advanced"` OR `hardwareExperience: "advanced"`:

**After (Enhanced):**
```markdown
ROS 2 (Robot Operating System 2) is a middleware framework for robotics applications,
built on top of DDS (Data Distribution Service) for real-time, distributed communication.

Key architectural improvements over ROS 1:
- **Nodes**: Process-level components with improved QoS (Quality of Service) policies
- **Topics**: DDS-based pub/sub with configurable reliability, durability, and history
- **Services**: Synchronous RPC with timeout handling and async clients
- **Actions**: Long-running tasks with feedback and preemption support

**Performance Considerations:**
- Use intra-process communication for same-process nodes (zero-copy transport)
- Configure QoS policies based on network characteristics
- Consider node composition for reduced overhead
- Profile with ros2 topic hz and ros2 topic bw for throughput analysis

**Best Practices:**
- Use lifecycle nodes for managed startup/shutdown
- Implement proper error handling with rclcpp exceptions
- Follow REP 2003 for package organization
- Use parameter files for configuration management
```

### Syllabus Compliance

All personalized content is validated to ensure:
- ✅ Core ROS 2 concepts maintained (nodes, topics, services, actions)
- ✅ Gazebo/Unity simulation concepts preserved
- ✅ NVIDIA Isaac platform concepts intact
- ✅ VLA (Vision-Language-Action) concepts maintained
- ✅ All code examples preserved (with enhanced explanations)
- ✅ Learning outcomes from course syllabus maintained

If validation fails, the original content is returned.

## Troubleshooting

### Error: "GEMINI_API_KEY not found"
**Solution:** Make sure you've added `GEMINI_API_KEY` to your `backend/.env` file

### Error: "Module 'google.generativeai' not found"
**Solution:** Run `pip install google-generativeai` in the backend directory

### Error: "Invalid or expired token"
**Solution:** Login again to get a fresh authentication token

### Personalization takes too long (>5 seconds)
**Solution:**
- Check your internet connection
- Verify Gemini API quota limits
- The system uses caching (5 minutes) to speed up subsequent requests

### Validation fails - "Missing core concepts"
This means the AI-generated content removed essential syllabus concepts. The system will:
1. Log a warning
2. Return the original content instead
3. This is expected behavior to maintain educational integrity

## Performance Metrics

The system tracks personalization performance:
- Target: <500ms response time for 95% of requests
- Caching: 5-minute TTL for personalized content
- Monitoring: All requests are logged with timing data

To view performance stats:
```python
from backend.src.services.personalization_service import personalization_service
stats = personalization_service.get_performance_stats()
print(stats)
```

## Architecture

```
User Profile (beginner/advanced)
    ↓
PersonalizationService
    ↓
GeminiPersonalizationService (AI-powered)
    ↓
SyllabusComplianceValidator
    ↓
Personalized Content (cached)
```

## Next Steps

1. Test with different user profiles (beginner, intermediate, advanced)
2. Try different learning preferences (visual, hands-on, theoretical)
3. Monitor performance metrics
4. Review logs for any validation failures
5. Adjust Gemini prompts if needed for better results

## Support

For issues or questions:
- Check logs in `backend/logs/`
- Review test output: `pytest tests/test_gemini_personalization.py -v`
- Ensure Gemini API key is valid and has quota remaining
- Verify user profile has required fields (softwareExperience, hardwareExperience)
