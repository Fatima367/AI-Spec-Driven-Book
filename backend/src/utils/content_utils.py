"""
Content utilities for reading and writing MDX files
"""

import os
import shutil
from typing import Optional
import re

async def read_content_file(chapter_id: str) -> str:
    """
    Read content from an MDX file based on chapter ID
    """
    content_dir = "book_frontend/docs"
    file_path = os.path.join(content_dir, f"{chapter_id}.mdx")

    if not os.path.exists(file_path):
        # Try other common file extensions
        for ext in ['.mdx', '.md']:
            file_path = os.path.join(content_dir, f"{chapter_id}{ext}")
            if os.path.exists(file_path):
                break
        else:
            raise FileNotFoundError(f"Content file not found for chapter: {chapter_id}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content

async def write_content_file(file_name: str, content: str) -> bool:
    """
    Write content to an MDX file
    """
    content_dir = "book_frontend/docs"
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
    content_dir = "book_frontend/docs"

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
    content_dir = "book_frontend/docs"

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
    content_dir = "book_frontend/docs"
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