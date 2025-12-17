# Personalization Quick Reference

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install google-generativeai

# 2. Add to .env
GEMINI_API_KEY=your_key_here

# 3. Test
python tests/test_gemini_personalization.py

# 4. Run backend
uvicorn main:app --reload
```

## 🎯 API Endpoint

```bash
POST /api/v1/personalize/{chapter_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_preferences": {
    "learning_mode": "beginner|balanced|advanced",
    "difficulty": "basic|medium|advanced",
    "focus_area": "theory|hardware|software"
  }
}
```

## 🧠 How It Works

```
User Profile → Personalization Service → Gemini AI → Validator → Personalized Content
```

## 📊 User Experience Levels

### Beginner (`softwareExperience: "beginner"`)
- ➕ Simplified language
- ➕ Step-by-step explanations
- ➕ Analogies and examples
- ➕ Line-by-line code walkthrough
- ✅ All core concepts maintained

### Advanced (`softwareExperience: "advanced"`)
- ➕ Technical depth
- ➕ Best practices
- ➕ Research references
- ➕ Performance optimization
- ➕ Architectural tradeoffs
- ✅ All fundamentals maintained

## 🔒 Syllabus Compliance

**Protected Concepts:**
- ROS 2: nodes, topics, services, actions
- Gazebo: simulation, URDF, SDF
- Unity: digital twin
- Isaac: Isaac Sim, Isaac SDK
- VLA: Vision-Language-Action
- Physical AI: embodied intelligence

**Validation:**
```python
validator = SyllabusComplianceValidator()
is_valid, message = validator.validate_content(original, personalized)
# If invalid → returns original content
```

## ⚡ Performance

- **Target:** <500ms for 95% requests
- **Cache:** 5-minute TTL
- **Fallback:** Original content on error
- **Monitoring:** All requests logged

```python
# Get performance stats
from src.services.personalization_service import personalization_service
stats = personalization_service.get_performance_stats()
print(f"Avg response time: {stats['avg_response_time']:.2f}ms")
print(f"P95: {stats['p95_response_time']:.2f}ms")
print(f"Under 500ms: {stats['percent_under_500ms']:.1f}%")
```

## 🧪 Testing

```bash
# Run tests
pytest tests/test_gemini_personalization.py -v

# Test specific function
python -m pytest tests/test_gemini_personalization.py::test_singleton_service_exists

# Run with coverage
pytest tests/test_gemini_personalization.py --cov=src/services
```

## 🐛 Debugging

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check if Gemini is configured
from src.services.gemini_personalization_service import gemini_personalization_service
print(gemini_personalization_service.model)  # Should show Gemini model

# Test simplification directly
content = "ROS 2 provides nodes, topics, and services."
result = gemini_personalization_service.simplify_for_beginners(content)
print(result)
```

## 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY not found` | Add to `.env` file |
| `Module not found` | `pip install google-generativeai` |
| `Validation fails` | Check logs - will return original content |
| `Slow response` | Check network, Gemini quota, cache hit rate |

## 📁 File Structure

```
backend/src/services/
├── gemini_personalization_service.py  # AI engine
├── personalization_service.py         # Main service (uses Gemini)
└── auth_service.py                     # Authentication

backend/tests/
├── test_gemini_personalization.py     # Unit tests
└── test_personalization_integration.py # Integration tests
```

## 🎨 Customization

### Adjust Prompts
Edit `gemini_personalization_service.py`:
```python
self.syllabus_context = """
Your custom instructions here...
"""
```

### Add Core Concepts
```python
CORE_CONCEPTS = {
    "new_module": ["concept1", "concept2"],
    # ...
}
```

### Tune Caching
```python
self.cache_ttl = 600  # 10 minutes instead of 5
```

## 📚 Code Examples

### Use in API Route:
```python
from src.services.personalization_service import personalization_service

@router.post("/{chapter_id}")
async def personalize(chapter_id: str, user_profile: UserProfile):
    content = await personalization_service.personalize_content(
        chapter_id=chapter_id,
        user_profile=user_profile,
        user_preferences={"learning_mode": "beginner"}
    )
    return {"content": content}
```

### Direct Gemini Usage:
```python
from src.services.gemini_personalization_service import gemini_personalization_service

# Simplify
simple = gemini_personalization_service.simplify_for_beginners(content)

# Enhance
advanced = gemini_personalization_service.enhance_for_advanced(content)

# Apply preferences
adapted = gemini_personalization_service.apply_user_preferences(
    content,
    learning_mode="hands-on",
    difficulty="medium",
    focus_area="software"
)
```

## 🔍 Monitoring

```python
# Log analysis
grep "Personalization" logs/backend.log
grep "SyllabusCompliance" logs/backend.log
grep "validation failed" logs/backend.log

# Performance metrics
python -c "
from src.services.personalization_service import personalization_service
stats = personalization_service.get_performance_stats()
for key, value in stats.items():
    print(f'{key}: {value}')
"
```

## 🚨 Error Handling Flow

```
1. Request comes in
   ↓
2. Validate authentication
   ↓
3. Read original content
   ↓
4. Call Gemini API
   ↓ (on error)
5. Log error + return original
   ↓ (on success)
6. Validate syllabus compliance
   ↓ (if invalid)
7. Log warning + return original
   ↓ (if valid)
8. Cache and return personalized content
```

## 📖 Resources

- Setup Guide: `../PERSONALIZATION_SETUP.md`
- Implementation Summary: `../PERSONALIZATION_IMPLEMENTATION_SUMMARY.md`
- Spec: `../specs/005-personalization-urdu/spec.md`
- Plan: `../specs/005-personalization-urdu/plan.md`
- Tasks: `../specs/005-personalization-urdu/tasks.md`

---

**Last Updated:** 2025-12-17
**Status:** Production Ready ✅
