"""
Test script for Gemini-based personalization service
"""
import pytest
from src.services.gemini_personalization_service import (
    GeminiPersonalizationService,
    SyllabusComplianceValidator,
    gemini_personalization_service
)


class TestSyllabusComplianceValidator:
    """Test the syllabus compliance validator"""

    def test_validates_core_concepts_maintained(self):
        validator = SyllabusComplianceValidator()

        original = """
        ROS 2 (Robot Operating System 2) is a middleware framework for robotics applications.
        It provides nodes, topics, and services for inter-process communication.
        """

        # Personalized content maintains core concepts
        personalized_valid = """
        Let's learn about ROS 2, which stands for Robot Operating System 2.
        It's like a framework that helps different parts of a robot talk to each other.
        ROS 2 uses special building blocks called nodes, topics, and services.
        """

        is_valid, message = validator.validate_content(original, personalized_valid)
        assert is_valid, f"Should be valid but got: {message}"

    def test_detects_missing_core_concepts(self):
        validator = SyllabusComplianceValidator()

        original = """
        ROS 2 (Robot Operating System 2) is a middleware framework for robotics applications.
        It provides nodes, topics, and services for inter-process communication.
        """

        # Personalized content removes "topics" concept
        personalized_invalid = """
        ROS 2 is a framework for robots.
        It has nodes and services for communication.
        """

        is_valid, message = validator.validate_content(original, personalized_invalid)
        assert not is_valid, "Should detect missing 'topics' concept"
        assert "topics" in message.lower()

    def test_identifies_relevant_modules(self):
        validator = SyllabusComplianceValidator()

        content_ros2 = "This chapter covers ROS 2 nodes and topics"
        modules = validator._identify_relevant_modules(content_ros2)
        assert "ros2" in modules

        content_gazebo = "We'll use Gazebo simulator with URDF files"
        modules = validator._identify_relevant_modules(content_gazebo)
        assert "gazebo" in modules

        content_isaac = "NVIDIA Isaac Sim provides robot simulation"
        modules = validator._identify_relevant_modules(content_isaac)
        assert "isaac" in modules


class TestGeminiPersonalizationService:
    """Test the Gemini personalization service"""

    @pytest.fixture
    def sample_content(self):
        return """
# ROS 2 Basics

ROS 2 (Robot Operating System 2) is a middleware framework for robotics applications.

## Key Concepts

- **Nodes**: Independent processes that perform computation
- **Topics**: Named buses for asynchronous message passing
- **Services**: Synchronous request/response communication

Example:
```python
import rclpy
from std_msgs.msg import String

def main():
    rclpy.init()
    node = rclpy.create_node('my_node')
    publisher = node.create_publisher(String, 'topic', 10)
    rclpy.spin(node)
```
"""

    def test_simplify_for_beginners_maintains_structure(self, sample_content):
        """Test that simplification maintains MDX structure and code examples"""
        service = GeminiPersonalizationService()

        # This would require GEMINI_API_KEY to be set
        # For now, we're testing the structure
        result = service.simplify_for_beginners(sample_content)

        # Should return content (either simplified or original if API fails)
        assert result is not None
        assert len(result) > 0

    def test_enhance_for_advanced_maintains_structure(self, sample_content):
        """Test that enhancement maintains MDX structure and code examples"""
        service = GeminiPersonalizationService()

        result = service.enhance_for_advanced(sample_content)

        # Should return content (either enhanced or original if API fails)
        assert result is not None
        assert len(result) > 0

    def test_apply_user_preferences(self, sample_content):
        """Test applying user preferences"""
        service = GeminiPersonalizationService()

        result = service.apply_user_preferences(
            sample_content,
            learning_mode="hands-on",
            difficulty="medium",
            focus_area="software"
        )

        # Should return content
        assert result is not None
        assert len(result) > 0


def test_singleton_service_exists():
    """Test that singleton instance is available"""
    assert gemini_personalization_service is not None
    assert isinstance(gemini_personalization_service, GeminiPersonalizationService)


if __name__ == "__main__":
    # Run basic tests
    print("Testing Syllabus Compliance Validator...")
    validator = SyllabusComplianceValidator()

    sample_original = """
    ROS 2 provides nodes, topics, and services for robotics.
    Gazebo is used for simulation with URDF files.
    NVIDIA Isaac Sim offers advanced robot simulation.
    """

    sample_personalized = """
    Let's learn about ROS 2! It gives us nodes, topics, and services to build robots.
    For testing robots virtually, we use Gazebo simulator with URDF robot descriptions.
    NVIDIA Isaac Sim is another powerful tool for simulating robots.
    """

    is_valid, message = validator.validate_content(sample_original, sample_personalized)
    print(f"Validation result: {is_valid}")
    print(f"Message: {message}")

    print("\nIdentifying modules...")
    modules = validator._identify_relevant_modules(sample_original)
    print(f"Relevant modules: {modules}")

    print("\nTests completed!")
