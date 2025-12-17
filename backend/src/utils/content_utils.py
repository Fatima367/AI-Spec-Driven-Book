"""
Content utilities for reading and writing MDX files
"""

import os
import shutil
from typing import Optional
import re


def get_content_directory():
    """
    Get the absolute path to the content directory (book_frontend/docs)
    """
    # Get the project root directory (three levels up from this file: backend/src/utils)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_dir)))
    # Ensure we get the absolute path
    content_dir = os.path.abspath(os.path.join(project_root, "book_frontend", "docs"))
    return content_dir

async def read_content_file(chapter_id: str) -> str:
    """
    Read content from an MDX file based on chapter ID
    Handles multiple content structures:
    - Direct files: intro.mdx, hardware-lab.mdx
    - Directory with index: module1-ros2/index.mdx, capstone/index.mdx
    - Nested files: part1/chapter1.1.mdx
    """
    content_dir = get_content_directory()

    # List of possible file paths to check in order
    possible_paths = [
        # Nested path (e.g., part1/chapter1.1 -> part1/chapter1.1.mdx)
        os.path.join(content_dir, f"{chapter_id}.mdx"),
        os.path.join(content_dir, f"{chapter_id}.md"),
        # Directory with index file (e.g., module1-ros2 -> module1-ros2/index.mdx)
        os.path.join(content_dir, chapter_id, "index.mdx"),
        os.path.join(content_dir, chapter_id, "index.md"),
    ]

    # Additional path patterns that might be used
    # Handle cases where chapter_id includes 'docs/' prefix
    if chapter_id.startswith('docs/'):
        clean_chapter_id = chapter_id[5:]  # Remove 'docs/' prefix
        possible_paths.extend([
            os.path.join(content_dir, f"{clean_chapter_id}.mdx"),
            os.path.join(content_dir, f"{clean_chapter_id}.md"),
            os.path.join(content_dir, clean_chapter_id, "index.mdx"),
            os.path.join(content_dir, clean_chapter_id, "index.md"),
        ])

    # Handle cases where path has extra components
    # e.g., if the path is something like "docs/module1-ros2" instead of just "module1-ros2"
    if '/' in chapter_id:
        parts = chapter_id.split('/')
        if len(parts) > 1:
            # Try different combinations by removing the first part (likely 'docs')
            if parts[0] == 'docs':
                reduced_path = '/'.join(parts[1:])
                possible_paths.extend([
                    os.path.join(content_dir, f"{reduced_path}.mdx"),
                    os.path.join(content_dir, f"{reduced_path}.md"),
                    os.path.join(content_dir, reduced_path, "index.mdx"),
                    os.path.join(content_dir, reduced_path, "index.md"),
                ])

            # Also try removing the last part if it might be a file extension or index reference
            if parts[-1] in ['index', 'index.mdx', 'index.md']:
                reduced_path = '/'.join(parts[:-1])
                possible_paths.extend([
                    os.path.join(content_dir, reduced_path, "index.mdx"),
                    os.path.join(content_dir, reduced_path, "index.md"),
                ])

            # Additional fallback: try various combinations of the path parts
            # This handles cases like "part2/chapter2.1" -> check for "part2/chapter2.1.mdx" but also "part2/chapter2.1/index.mdx"
            for i in range(1, len(parts)):
                partial_path = '/'.join(parts[:i])
                remaining_path = '/'.join(parts[i:])
                if partial_path and remaining_path:
                    possible_paths.extend([
                        os.path.join(content_dir, partial_path, f"{remaining_path}.mdx"),
                        os.path.join(content_dir, partial_path, f"{remaining_path}.md"),
                        os.path.join(content_dir, partial_path, remaining_path, "index.mdx"),
                        os.path.join(content_dir, partial_path, remaining_path, "index.md"),
                    ])

    # Try each possible path in local environment
    for file_path in possible_paths:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content

    # If file is not found locally, try to fetch from the deployed frontend
    # This handles the case where the backend is deployed separately and doesn't have local content files
    try:
        from urllib.parse import urljoin
        import aiohttp

        # Get the deployed frontend URL from environment variable
        frontend_url = os.getenv('FRONTEND_URL', 'https://physical-ai-n-humanoid-robotics.vercel.app')

        # Try to fetch content from the frontend
        # Format: https://physical-ai-n-humanoid-robotics.vercel.app/docs/part1/chapter1.1.mdx
        # or https://physical-ai-n-humanoid-robotics.vercel.app/docs/module1-ros2/index.mdx
        urls_to_try = [
            f"{frontend_url}/docs/{chapter_id}.mdx",
            f"{frontend_url}/docs/{chapter_id}.md",
            f"{frontend_url}/docs/{chapter_id}/",
            f"{frontend_url}/docs/{chapter_id}"
        ]

        for url in urls_to_try:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            # For HTML responses (like index pages), we might need to extract the actual content
                            # This is a simple check - in a real implementation, we'd want more sophisticated parsing
                            if url.endswith('/') or url == f"{frontend_url}/docs/{chapter_id}":
                                # This is likely an HTML page, not raw MDX content
                                # For personalization, we might need to extract just the content portion
                                # For now, let's just return the content if it's available
                                pass
                            return content
            except Exception:
                continue  # Try the next URL

    except ImportError:
        # aiohttp is not available, skip the remote fetch
        pass
    except Exception:
        # If there's an error with remote fetching, continue to raise the original error
        pass

    # If no file found locally or remotely, raise error with helpful message
    raise FileNotFoundError(f"Content file not found for chapter: {chapter_id}. Tried paths: {possible_paths}")

async def write_content_file(file_name: str, content: str) -> bool:
    """
    Write content to an MDX file
    """
    content_dir = get_content_directory()
    file_path = os.path.join(content_dir, file_name)

    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        return True
    except Exception as e:
        print(f"Error writing content file {file_path}: {str(e)}")
        return False

async def sync_urdu_content(english_file_path: str, urdu_content: str = None) -> bool:
    """
    Synchronize Urdu translation with English content
    If urdu_content is provided, update the Urdu file
    Otherwise, create a new Urdu file based on the English content
    """
    content_dir = get_content_directory()

    # Convert English file path to Urdu file path
    urdu_file_path = english_file_path.replace(content_dir, os.path.join(content_dir, "urdu"), 1)
    if not urdu_file_path.startswith(os.path.join(content_dir, "urdu")):
        # If the path doesn't contain the docs directory, add urdu prefix differently
        base_name = os.path.basename(english_file_path)
        dir_name = os.path.dirname(english_file_path)
        name, ext = os.path.splitext(base_name)
        urdu_file_path = os.path.join(dir_name, f"urdu-{name}{ext}")

    # Alternative approach: if the file is like part1/chapter1.mdx, make it part1/urdu-chapter1.mdx
    if english_file_path.startswith(content_dir):
        relative_path = os.path.relpath(english_file_path, content_dir)
        dir_path = os.path.dirname(relative_path)
        base_name = os.path.basename(relative_path)
        name, ext = os.path.splitext(base_name)
        urdu_file_path = os.path.join(content_dir, dir_path, f"urdu-{name}{ext}")

    try:
        if urdu_content is not None:
            # Write provided Urdu content to the Urdu file
            os.makedirs(os.path.dirname(urdu_file_path), exist_ok=True)
            with open(urdu_file_path, 'w', encoding='utf-8') as file:
                file.write(urdu_content)
            return True
        else:
            # Create Urdu file based on English content if it doesn't exist
            if not os.path.exists(urdu_file_path):
                # Read English content
                with open(english_file_path, 'r', encoding='utf-8') as file:
                    english_content = file.read()

                # Create basic Urdu content (initially just a placeholder)
                # In a real implementation, this would involve actual translation
                urdu_content = f"<!-- Urdu translation of {os.path.basename(english_file_path)} -->\n\n{english_content}"

                # Write to Urdu file
                os.makedirs(os.path.dirname(urdu_file_path), exist_ok=True)
                with open(urdu_file_path, 'w', encoding='utf-8') as file:
                    file.write(urdu_content)

                return True
            return True  # Urdu file already exists
    except Exception as e:
        print(f"Error synchronizing Urdu content for {english_file_path}: {str(e)}")
        return False

async def get_urdu_file_path(english_file_path: str) -> str:
    """
    Get the corresponding Urdu file path for an English file
    """
    content_dir = get_content_directory()

    if english_file_path.startswith(content_dir):
        relative_path = os.path.relpath(english_file_path, content_dir)
        dir_path = os.path.dirname(relative_path)
        base_name = os.path.basename(relative_path)
        name, ext = os.path.splitext(base_name)
        urdu_file_path = os.path.join(content_dir, dir_path, f"urdu-{name}{ext}")
        return urdu_file_path

    # Fallback approach
    dir_path = os.path.dirname(english_file_path)
    base_name = os.path.basename(english_file_path)
    name, ext = os.path.splitext(base_name)
    return os.path.join(dir_path, f"urdu-{name}{ext}")

async def check_urdu_file_exists(english_file_path: str) -> bool:
    """
    Check if the corresponding Urdu file exists for an English file
    """
    urdu_file_path = await get_urdu_file_path(english_file_path)
    return os.path.exists(urdu_file_path)

async def get_all_content_files() -> list:
    """
    Get all content files in the docs directory
    """
    content_dir = get_content_directory()
    content_files = []

    for root, dirs, files in os.walk(content_dir):
        # Skip Urdu files to avoid duplication
        dirs[:] = [d for d in dirs if not d.startswith('urdu')]

        for file in files:
            if file.endswith(('.mdx', '.md')) and not file.startswith('urdu-'):
                full_path = os.path.join(root, file)
                content_files.append(full_path)

    return content_files

async def sync_all_urdu_files() -> bool:
    """
    Synchronize all Urdu translation files with their English counterparts
    """
    try:
        content_files = await get_all_content_files()
        sync_success = True

        for english_file in content_files:
            if not await sync_urdu_content(english_file):
                print(f"Failed to sync Urdu file for: {english_file}")
                sync_success = False

        return sync_success
    except Exception as e:
        print(f"Error syncing all Urdu files: {str(e)}")
        return False