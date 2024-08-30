import os
import sys
import hashlib

def generate_hash(dir_path):
    """
    Generate a hash based on the contents of all .tf files in the given directory and its subdirectories.

    Args:
        dir_path (str): The path to the directory containing .tf files.

    Returns:
        str: The first 8 characters of the generated SHA256 hash.
    """
    sha256 = hashlib.sha256()
    for root, _, files in os.walk(dir_path):
        for file in sorted(files):  # Sort files for consistency
            if file.endswith('.tf'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)
    return sha256.hexdigest()[:8]

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
    Main function to handle command-line arguments, generate the configuration hash,
    and set GitHub Actions outputs and environment variables.

    Usage:
        python hash_generator.py <directory>

    Exits:
        0: Success
        1: Incorrect number of arguments or invalid directory
    """
    if len(sys.argv) != 2:
        print("Usage: python hash_generator.py <directory>", file=sys.stderr)
        sys.exit(1)
    
    input_directory = sys.argv[1]
    if not os.path.isdir(input_directory):
        print(f"Error: {input_directory} is not a valid directory", file=sys.stderr)
        sys.exit(1)
    
    config_hash = generate_hash(input_directory)
    
    # Set GitHub Actions output
    set_output('config_hash', config_hash)
    
    # Set environment variable
    set_env('CONFIG_HASH', config_hash)
    
    # Print to stdout for logging purposes
    print(f"Generated hash: {config_hash}")

if __name__ == "__main__":
    main()