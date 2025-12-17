"""
Personalization Service for adapting content based on user profile
Integrates with Gemini AI for intelligent content adaptation
"""
import os
import time
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from ..utils.content_utils import read_content_file, get_content_directory
from ..utils.logging_utils import log_personalization_request, log_error, log_performance_metrics, log_info
import hashlib
from .gemini_personalization_service import gemini_personalization_service


def get_personalization_content_directory():
    """
    Get the content directory for personalization service
    """
    from ..utils.content_utils import get_content_directory
    return get_content_directory()

class PersonalizationService:
    def __init__(self):
        self.content_dir = get_personalization_content_directory()
        # Performance tracking
        self.response_times = []
        # Caching
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes in seconds

    def _generate_cache_key(self, chapter_id: str, user_profile: Any, user_preferences: Optional[Dict] = None) -> str:
        """
        Generate a unique cache key based on chapter_id, user profile, and preferences
        """
        # Create a hash of the user profile and preferences to use as part of the cache key
        profile_str = f"{getattr(user_profile, 'softwareExperience', '')}-{getattr(user_profile, 'hardwareExperience', '')}-{getattr(user_profile, 'technicalBackground', '')}"
        preferences_str = str(user_preferences) if user_preferences else ""

        # Combine all components and hash them
        key_str = f"{chapter_id}-{profile_str}-{preferences_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: dict) -> bool:
        """
        Check if the cached entry is still valid (not expired)
        """
        if not cache_entry or 'timestamp' not in cache_entry:
            return False

        # Check if the cache entry has expired
        cache_time = cache_entry['timestamp']
        current_time = datetime.now(timezone.utc)
        time_diff = (current_time - cache_time).total_seconds()

        return time_diff < self.cache_ttl

    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """
        Get content from cache if it exists and is valid
        """
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if self._is_cache_valid(cache_entry):
                from ..utils.logging_utils import log_info
                log_info(f"Cache hit for key: {cache_key[:8]}...")
                return cache_entry['content']
            else:
                # Remove expired cache entry
                del self.cache[cache_key]

        return None

    def _set_in_cache(self, cache_key: str, content: str):
        """
        Set content in cache with current timestamp
        """
        self.cache[cache_key] = {
            'content': content,
            'timestamp': datetime.now(timezone.utc)
        }
        from ..utils.logging_utils import log_info
        log_info(f"Cache set for key: {cache_key[:8]}...")

    async def personalize_content(
        self,
        chapter_id: str,
        user_profile: Any,
        user_preferences: Optional[Dict] = None
    ) -> str:
        """
        Personalize chapter content based on user profile and preferences
        """
        start_time = time.time()
        user_id = getattr(user_profile, 'id', 'unknown')

        # Generate cache key
        cache_key = self._generate_cache_key(chapter_id, user_profile, user_preferences)

        # Try to get from cache first
        cached_content = self._get_from_cache(cache_key)
        if cached_content:
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            # Log the cache hit as a successful request
            log_personalization_request(chapter_id, user_id, response_time, success=True)
            from ..utils.logging_utils import log_info
            log_info(f"Returning cached content for chapter {chapter_id}")
            return cached_content

        try:
            # Verify user session is still valid before processing
            if not self._is_valid_session(user_profile):
                raise ValueError("User session has expired")

            # Read the original content
            original_content = await read_content_file(chapter_id)

            # Apply personalization logic based on user profile
            # This is a simplified version - in a real implementation, this would
            # involve more sophisticated content adaptation based on user preferences
            software_exp = getattr(user_profile, 'softwareExperience', 'beginner')
            hardware_exp = getattr(user_profile, 'hardwareExperience', 'beginner')
            tech_background = getattr(user_profile, 'technicalBackground', 'general')

            # Apply personalization based on experience level
            personalized_content = self._apply_personalization(
                original_content,
                software_exp,
                hardware_exp,
                tech_background,
                user_preferences
            )

            # Calculate response time
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.response_times.append(response_time)

            # Store in cache
            self._set_in_cache(cache_key, personalized_content)

            # Log the personalization request
            log_personalization_request(chapter_id, user_id, response_time, success=True)

            # Check if response time is above threshold
            if response_time > 500:
                from ..utils.logging_utils import log_warning
                log_warning(f"Personalization response time exceeded 500ms: {response_time:.2f}ms for chapter {chapter_id}", "Performance")

            return personalized_content
        except Exception as e:
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            log_personalization_request(chapter_id, user_id, response_time, success=False, error=str(e))
            log_error(e, f"personalize_content for chapter {chapter_id}")
            raise

    def _is_valid_session(self, user_profile: Any) -> bool:
        """
        Check if user session is still valid (not expired)
        """
        try:
            # Check if user profile exists and has valid timestamp
            if not user_profile:
                return False

            # If user profile has an updated_at field, verify it's not too old
            # (This would be based on your session timeout policy)
            if hasattr(user_profile, 'updated_at'):
                updated_at = getattr(user_profile, 'updated_at')
                if updated_at:
                    # Calculate time difference (assuming 24 hour session timeout)
                    now = datetime.now(timezone.utc)
                    time_diff = now - updated_at if isinstance(updated_at, datetime) else now
                    max_session_duration = 24 * 60 * 60  # 24 hours in seconds
                    return time_diff.total_seconds() < max_session_duration

            # If no timestamp, assume session is valid
            return True
        except Exception:
            # If there's an error checking session validity, return False
            return False

    def _apply_personalization(
        self,
        content: str,
        software_exp: str,
        hardware_exp: str,
        tech_background: str,
        user_preferences: Optional[Dict]
    ) -> str:
        """
        Apply personalization logic to content based on user profile
        """
        # This is a simplified personalization algorithm
        # In a real implementation, this would be more sophisticated
        if software_exp == "beginner" or hardware_exp == "beginner":
            # For beginners, add more explanations and simpler language
            content = self._simplify_content(content)
        elif software_exp == "advanced" or hardware_exp == "advanced":
            # For advanced users, add more technical depth
            content = self._enhance_content(content)

        # Apply any specific preferences if provided
        if user_preferences:
            content = self._apply_user_preferences(content, user_preferences)

        return content

    def _simplify_content(self, content: str) -> str:
        """
        Simplify content for beginners using Gemini AI
        """
        log_info("Simplifying content for beginner using Gemini AI")
        try:
            return gemini_personalization_service.simplify_for_beginners(content)
        except Exception as e:
            log_error(e, "simplify_content_with_gemini")
            # Return original content if Gemini fails
            return content

    def _enhance_content(self, content: str) -> str:
        """
        Enhance content for advanced users using Gemini AI
        """
        log_info("Enhancing content for advanced user using Gemini AI")
        try:
            return gemini_personalization_service.enhance_for_advanced(content)
        except Exception as e:
            log_error(e, "enhance_content_with_gemini")
            # Return original content if Gemini fails
            return content

    def _apply_user_preferences(self, content: str, preferences: Dict) -> str:
        """
        Apply specific user preferences to content using Gemini AI
        """
        # Extract preferences
        learning_mode = preferences.get('learning_mode', 'balanced')
        difficulty = preferences.get('difficulty', 'medium')
        focus_area = preferences.get('focus_area', 'theory')

        log_info(f"Applying user preferences: learning_mode={learning_mode}, difficulty={difficulty}, focus_area={focus_area}")

        try:
            # Use Gemini to apply preferences
            return gemini_personalization_service.apply_user_preferences(
                content,
                learning_mode=learning_mode,
                difficulty=difficulty,
                focus_area=focus_area
            )
        except Exception as e:
            log_error(e, "apply_user_preferences_with_gemini")
            # Return original content if Gemini fails
            return content

    def get_performance_stats(self) -> dict:
        """
        Get performance statistics for personalization service
        """
        if not self.response_times:
            return {
                "total_requests": 0,
                "avg_response_time": 0,
                "p95_response_time": 0,
                "p99_response_time": 0,
                "requests_under_500ms": 0,
                "requests_over_500ms": 0
            }

        sorted_times = sorted(self.response_times)
        total_requests = len(sorted_times)

        # Calculate percentiles
        p95_idx = int(0.95 * total_requests)
        p99_idx = int(0.99 * total_requests)

        p95_time = sorted_times[min(p95_idx, total_requests - 1)] if p95_idx < total_requests else 0
        p99_time = sorted_times[min(p99_idx, total_requests - 1)] if p99_idx < total_requests else 0

        # Calculate requests under/over threshold
        requests_under_500ms = sum(1 for t in sorted_times if t <= 500)
        requests_over_500ms = total_requests - requests_under_500ms

        avg_response_time = sum(sorted_times) / total_requests if total_requests > 0 else 0

        return {
            "total_requests": total_requests,
            "avg_response_time": avg_response_time,
            "p95_response_time": p95_time,
            "p99_response_time": p99_time,
            "requests_under_500ms": requests_under_500ms,
            "requests_over_500ms": requests_over_500ms,
            "percent_under_500ms": (requests_under_500ms / total_requests) * 100 if total_requests > 0 else 0
        }

    def clear_performance_stats(self):
        """
        Clear performance statistics
        """
        self.response_times = []

# Create a singleton instance of the service
personalization_service = PersonalizationService()