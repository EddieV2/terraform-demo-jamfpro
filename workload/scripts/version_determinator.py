import os
import subprocess
import re
import sys

def get_latest_tag():
    """
    Retrieve the latest Git tag.

    Returns:
        str: The latest Git tag, or None if no tags are found.
    """
    try:
        return subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0', '--match', 'v*'], stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_changed_files(latest_tag):
    """
    Get a list of files changed since the latest tag or all files if no tag exists.

    Args:
        latest_tag (str): The latest Git tag, or None if no tags exist.

    Returns:
        list: A list of changed file paths.
    """
    if latest_tag:
        try:
            return subprocess.check_output(['git', 'diff', '--name-only', latest_tag, 'HEAD']).decode().split('\n')
        except subprocess.CalledProcessError:
            print("Error: Unable to get changed files. Using all files instead.")
    
    # If no tag exists or there's an error, return all tracked files
    return subprocess.check_output(['git', 'ls-files']).decode().split('\n')

def read_file_content(file_path):
    """
    Read the content of a file with UTF-8 encoding.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.

    Raises:
        UnicodeDecodeError: If the file cannot be decoded using UTF-8.
        IOError: If there's an issue reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file {file_path} with UTF-8 encoding.")
        raise
    except IOError as e:
        print(f"Error: Unable to read file {file_path}. {str(e)}")
        raise

def parse_resource(content):
    """
    Parse Terraform resource blocks from the given content.

    Args:
        content (str): The content of a Terraform file.

    Returns:
        dict: A dictionary of resources, their types, names, and fields.
    """
    resources = {}
    current_resource = None
    for line in content.split('\n'):
        resource_match = re.match(r'resource\s+"(\w+)"\s+"(\w+)"\s*{', line)
        if resource_match:
            current_resource = (resource_match.group(1), resource_match.group(2))
            resources[current_resource] = {}
        elif current_resource and '=' in line:
            field, value = map(str.strip, line.split('=', 1))
            resources[current_resource][field] = value.rstrip(',')
        elif line.strip() == '}':
            current_resource = None
    return resources

def is_new_resource_type(changed_files, config_directory):
    """
    Check if any new resource type is introduced in the changed files.

    Args:
        changed_files (list): List of changed file paths.
        config_directory (str): The directory containing Terraform configurations.

    Returns:
        bool: True if a new resource type is found, False otherwise.
    """
    existing_resources = set()
    new_resources = set()

    for root, _, files in os.walk(config_directory):
        for file in files:
            if file.endswith('.tf'):
                content = read_file_content(os.path.join(root, file))
                existing_resources.update(resource[0] for resource in parse_resource(content))

    for file in changed_files:
        if file.endswith('.tf') and file.startswith(config_directory):
            content = read_file_content(file)
            new_resources.update(resource[0] for resource in parse_resource(content))

    return bool(new_resources - existing_resources)

def is_new_resource_iteration(changed_files, config_directory):
    """
    Check if a new iteration of an existing resource type is introduced.

    Args:
        changed_files (list): List of changed file paths.
        config_directory (str): The directory containing Terraform configurations.

    Returns:
        bool: True if a new iteration is found, False otherwise.
    """
    existing_resources = {}
    new_resources = {}

    for root, _, files in os.walk(config_directory):
        for file in files:
            if file.endswith('.tf'):
                content = read_file_content(os.path.join(root, file))
                for (resource_type, resource_name), _ in parse_resource(content).items():
                    existing_resources.setdefault(resource_type, set()).add(resource_name)

    for file in changed_files:
        if file.endswith('.tf') and file.startswith(config_directory):
            content = read_file_content(file)
            for (resource_type, resource_name), _ in parse_resource(content).items():
                new_resources.setdefault(resource_type, set()).add(resource_name)

    for resource_type, new_names in new_resources.items():
        if resource_type in existing_resources:
            if new_names - existing_resources[resource_type]:
                return True

    return False

def is_field_changed(changed_files, config_directory):
    """
    Check if any fields have been added or removed from existing resources.

    Args:
        changed_files (list): List of changed file paths.
        config_directory (str): The directory containing Terraform configurations.

    Returns:
        bool: True if fields have changed, False otherwise.
    """
    existing_resources = {}
    new_resources = {}

    for root, _, files in os.walk(config_directory):
        for file in files:
            if file.endswith('.tf'):
                content = read_file_content(os.path.join(root, file))
                existing_resources.update(parse_resource(content))

    for file in changed_files:
        if file.endswith('.tf') and file.startswith(config_directory):
            content = read_file_content(file)
            new_resources.update(parse_resource(content))

    for resource, new_fields in new_resources.items():
        if resource in existing_resources:
            if set(new_fields.keys()) != set(existing_resources[resource].keys()):
                return True

    return False

def is_field_value_changed(changed_files, config_directory):
    """
    Check if any field values have changed in existing resources.

    Args:
        changed_files (list): List of changed file paths.
        config_directory (str): The directory containing Terraform configurations.

    Returns:
        bool: True if field values have changed, False otherwise.
    """
    existing_resources = {}
    new_resources = {}

    for root, _, files in os.walk(config_directory):
        for file in files:
            if file.endswith('.tf'):
                content = read_file_content(os.path.join(root, file))
                existing_resources.update(parse_resource(content))

    for file in changed_files:
        if file.endswith('.tf') and file.startswith(config_directory):
            content = read_file_content(file)
            new_resources.update(parse_resource(content))

    for resource, new_fields in new_resources.items():
        if resource in existing_resources:
            for field, value in new_fields.items():
                if field in existing_resources[resource] and value != existing_resources[resource][field]:
                    return True

    return False

def determine_version_increment(config_directory):
    """
    Determine the type of version increment based on the changes in Terraform files.

    Args:
        config_directory (str): The directory containing Terraform configurations.

    Returns:
        str: The type of version increment ('major', 'minor', or 'patch').
    """
    latest_tag = get_latest_tag()
    changed_files = get_changed_files(latest_tag)

    # If this is the first run (no tags), treat it as a major version
    if not latest_tag:
        print("No existing tags found. Treating as initial major version.")
        return 'major'

    if is_new_resource_type(changed_files, config_directory):
        return 'major'
    if is_new_resource_iteration(changed_files, config_directory):
        return 'minor'
    if is_field_changed(changed_files, config_directory):
        return 'minor'
    if is_field_value_changed(changed_files, config_directory):
        return 'patch'

    return 'patch'  # Default to patch if no conditions are met

def set_output(name, value):
    """
    Set a GitHub Actions output variable.

    Args:
        name (str): The name of the output variable.
        value (str): The value to set.
    """
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as fh:
        print(f'{name}={value}', file=fh)

def set_env(name, value):
    """
    Set a GitHub Actions environment variable.

    Args:
        name (str): The name of the environment variable.
        value (str): The value to set.
    """
    with open(os.environ['GITHUB_ENV'], 'a', encoding='utf-8') as fh:
        print(f'{name}={value}', file=fh)

def main():
    """
    Main function to determine and set the new version based on Terraform changes.

    Usage:
        python version_determinator.py <config_directory>

    Args:
        config_directory (str): The directory containing Terraform configurations.

    Exits:
        0: Success
        1: Incorrect number of arguments or invalid directory
    """
    if len(sys.argv) != 2:
        print("Usage: python version_determinator.py <config_directory>", file=sys.stderr)
        sys.exit(1)

    config_directory = sys.argv[1]
    if not os.path.isdir(config_directory):
        print(f"Error: {config_directory} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    increment_type = determine_version_increment(config_directory)

    latest_tag = get_latest_tag()
    if latest_tag:
        version_match = re.match(r'v(\d+)\.(\d+)\.(\d+)', latest_tag)
        if version_match:
            major, minor, patch = map(int, version_match.groups())
        else:
            print(f"Warning: Latest tag {latest_tag} does not match expected format. Starting from 0.0.0.")
            major, minor, patch = 0, 0, 0
    else:
        print("No existing tags found. Starting from version 0.0.0.")
        major, minor, patch = 0, 0, 0

    if increment_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif increment_type == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"v{major}.{minor}.{patch}"
    
    # Set GitHub Actions output
    set_output('version', new_version)
    
    # Set environment variable
    set_env('NEW_VERSION', new_version)
    
    # Print to stdout for logging purposes
    print(f"New version determined: {new_version}")

if __name__ == "__main__":
    main()