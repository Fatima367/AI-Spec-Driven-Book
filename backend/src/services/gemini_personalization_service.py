"""
Gemini-based Personalization Service for adapting content based on user profile
Uses Google's Gemini API to intelligently simplify or enhance content while maintaining syllabus compliance
"""
import os
try:
    import google.genai as genai
    GENAI_AVAILABLE = True
except ImportError:
    try:
        import google.generativeai as genai  # Fallback to deprecated version
        GENAI_AVAILABLE = True
    except ImportError:
        genai = None
        GENAI_AVAILABLE = False

from typing import Dict, Any, Optional
from ..utils.logging_utils import log_info, log_warning, log_error
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and genai:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        log_info("Google GenAI configured successfully")
    except Exception as e:
        log_warning(f"Failed to configure Google GenAI: {str(e)}", "Configuration")
        GENAI_AVAILABLE = False
else:
    log_warning("GEMINI_API_KEY not found or GenAI not available", "Configuration")
    GENAI_AVAILABLE = False


class SyllabusComplianceValidator:
    """
    Validates that personalized content maintains alignment with Physical AI & Humanoid Robotics course syllabus
    """

    # Core concepts that MUST be maintained in all personalized content
    CORE_CONCEPTS = {
        "ros2": ["ROS 2", "Robot Operating System", "nodes", "topics", "services", "actions"],
        "gazebo": ["Gazebo", "simulation", "URDF", "SDF", "physics engine"],
        "unity": ["Unity", "digital twin", "3D simulation"],
        "isaac": ["NVIDIA Isaac", "Isaac Sim", "Isaac SDK", "robot platform"],
        "vla": ["Vision-Language-Action", "VLA", "multimodal", "embodied AI"],
        "physical_ai": ["Physical AI", "embodied intelligence", "robot learning"]
    }

    def validate_content(self, original: str, personalized: str) -> tuple[bool, str]:
        """
        Validate that personalized content maintains core syllabus concepts

        Returns:
            (is_valid, message) - True if valid, False with reason if invalid
        """
        # Extract module context from original content
        relevant_modules = self._identify_relevant_modules(original)

        # Check if core concepts are maintained
        missing_concepts = []
        for module in relevant_modules:
            if module in self.CORE_CONCEPTS:
                for concept in self.CORE_CONCEPTS[module]:
                    # Check if concept exists in original but missing in personalized
                    if concept.lower() in original.lower() and concept.lower() not in personalized.lower():
                        missing_concepts.append(concept)

        if missing_concepts:
            return False, f"Missing core concepts: {', '.join(missing_concepts)}"

        return True, "Content maintains syllabus alignment"

    def _identify_relevant_modules(self, content: str) -> list[str]:
        """Identify which course modules are relevant to this content"""
        content_lower = content.lower()
        relevant = []

        for module, concepts in self.CORE_CONCEPTS.items():
            if any(concept.lower() in content_lower for concept in concepts):
                relevant.append(module)

        return relevant


class GeminiPersonalizationService:
    """
    Uses Gemini API to personalize educational content based on user experience level
    while maintaining strict syllabus compliance
    """

    def __init__(self):
        self.validator = SyllabusComplianceValidator()
        if GENAI_AVAILABLE and genai:
            try:
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                self.available = True
            except Exception as e:
                log_warning(f"Failed to initialize GenAI model: {str(e)}", "Configuration")
                self.available = False
        else:
            self.available = False

        # System instruction for maintaining syllabus compliance
        self.syllabus_context = """
You are personalizing content for the "Physical AI & Humanoid Robotics" course textbook.

CRITICAL REQUIREMENTS - MUST MAINTAIN:
1. All ROS 2 (Robot Operating System) concepts: nodes, topics, services, actions, publishers, subscribers
2. All Gazebo & Unity simulation concepts: URDF, SDF, physics engines, digital twins
3. All NVIDIA Isaac platform concepts: Isaac Sim, Isaac SDK, robot AI
4. All VLA (Vision-Language-Action) concepts: multimodal learning, embodied AI
5. All code examples and practical exercises (keep them intact or simplify explanation, not the code)
6. All learning outcomes from the course syllabus

DO NOT:
- Remove or skip any core technical concepts
- Omit code examples or practical exercises
- Change the fundamental learning objectives
"""

    def simplify_for_beginners(self, content: str, tech_background: str = "general") -> str:
        """
        Simplify content for users with beginner experience level
        Adds more explanations, breaks down complex concepts, uses simpler language
        """
        if not self.available:
            log_warning("GenAI not available, returning original content", "simplify_for_beginners")
            return content

        prompt = f"""
{self.syllabus_context}

TASK: Adapt this Physical AI & Robotics textbook content for BEGINNER-level learners.
User's technical background: {tech_background}

ADAPTATION REQUIREMENTS:
1. Simplify technical jargon (but keep the terms and explain them clearly)
2. Add step-by-step breakdowns of complex concepts
3. Include beginner-friendly analogies and real-world examples
4. Explain WHY things work the way they do, not just WHAT they are
5. Add transition phrases like "In simpler terms...", "Think of it this way...", "To understand this..."
6. Break long paragraphs into smaller, digestible chunks
7. PRESERVE all code examples but add line-by-line explanations
8. MAINTAIN all core ROS 2, Gazebo, Isaac, and VLA concepts - just explain them better

IMPORTANT: Keep all technical terms but make them accessible. Don't dumb down - build up understanding.

ORIGINAL CONTENT:
{content}

ADAPTED CONTENT (maintain MDX format):
"""

        try:
            response = self.model.generate_content(prompt)
            personalized_content = response.text

            # Validate syllabus compliance
            is_valid, message = self.validator.validate_content(content, personalized_content)
            if not is_valid:
                log_warning(f"Personalization validation failed: {message}", "SyllabusCompliance")
                # Return original content if validation fails
                return content

            log_info("Content simplified for beginner successfully with syllabus compliance")
            return personalized_content

        except Exception as e:
            log_error(e, "simplify_for_beginners")
            # Return original content on error
            return content

    def enhance_for_advanced(self, content: str, tech_background: str = "advanced") -> str:
        """
        Enhance content for users with advanced experience level
        Adds technical depth, advanced concepts, implementation details
        """
        if not self.available:
            log_warning("GenAI not available, returning original content", "enhance_for_advanced")
            return content

        prompt = f"""
{self.syllabus_context}

TASK: Adapt this Physical AI & Robotics textbook content for ADVANCED-level learners.
User's technical background: {tech_background}

ADAPTATION REQUIREMENTS:
1. Add technical depth and implementation details
2. Include advanced optimization techniques and best practices
3. Reference research papers and cutting-edge developments
4. Discuss architectural tradeoffs and design decisions
5. Add performance considerations and scalability concerns
6. Include advanced code patterns and professional practices
7. Mention edge cases and production deployment considerations
8. MAINTAIN all fundamental concepts (don't skip basics, just add depth)

IMPORTANT: Enhance, don't replace. Advanced learners still benefit from clear fundamentals.

ORIGINAL CONTENT:
{content}

ENHANCED CONTENT (maintain MDX format):
"""

        try:
            response = self.model.generate_content(prompt)
            personalized_content = response.text

            # Validate syllabus compliance
            is_valid, message = self.validator.validate_content(content, personalized_content)
            if not is_valid:
                log_warning(f"Personalization validation failed: {message}", "SyllabusCompliance")
                return content

            log_info("Content enhanced for advanced user successfully with syllabus compliance")
            return personalized_content

        except Exception as e:
            log_error(e, "enhance_for_advanced")
            return content

    def apply_user_preferences(
        self,
        content: str,
        learning_mode: str = "balanced",
        difficulty: str = "medium",
        focus_area: str = "theory"
    ) -> str:
        """
        Apply specific user preferences to content adaptation
        """
        if not self.available:
            log_warning("GenAI not available, returning original content", "apply_user_preferences")
            return content

        preference_instructions = []

        if learning_mode == "visual":
            preference_instructions.append("Emphasize visual descriptions and suggest diagrams where helpful")
        elif learning_mode == "hands-on":
            preference_instructions.append("Emphasize practical exercises and code examples")
        elif learning_mode == "theoretical":
            preference_instructions.append("Emphasize theoretical foundations and mathematical explanations")

        if focus_area == "hardware":
            preference_instructions.append("Add more hardware implementation details and physical considerations")
        elif focus_area == "software":
            preference_instructions.append("Add more software architecture and code implementation details")
        elif focus_area == "theory":
            preference_instructions.append("Add more theoretical background and research context")

        if not preference_instructions:
            return content

        prompt = f"""
{self.syllabus_context}

TASK: Adapt this content with the following user preferences:
{chr(10).join(f'- {instruction}' for instruction in preference_instructions)}

MAINTAIN all core concepts and learning objectives.

ORIGINAL CONTENT:
{content}

ADAPTED CONTENT (maintain MDX format):
"""

        try:
            response = self.model.generate_content(prompt)
            personalized_content = response.text

            # Validate syllabus compliance
            is_valid, message = self.validator.validate_content(content, personalized_content)
            if not is_valid:
                log_warning(f"Preference-based personalization validation failed: {message}", "SyllabusCompliance")
                return content

            log_info(f"Content adapted with user preferences successfully")
            return personalized_content

        except Exception as e:
            log_error(e, "apply_user_preferences")
            return content


# Create singleton instance
gemini_personalization_service = GeminiPersonalizationService()
