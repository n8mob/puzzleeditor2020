import os
import re


def find_for_pattern(pattern, migrations_dir='puzzles/migrations'):
  # List all migration files
  migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']

  # Regex pattern to find RenameModel operation for puzzles_puzzle
  regex = re.compile(pattern)

  # Iterate through migration files
  matching_files = []

  for migration_file in migration_files:
    path = os.path.join(migrations_dir, migration_file)
    with open(path, 'r') as file:
      content = file.read()
      if regex.search(content):
        print(f"Table 'main.puzzles_puzzle' renamed in migration: {migration_file}")
        matching_files.append(path)

  return matching_files


def find_rename(model_name):
  return find_for_pattern(rf'RenameModel.*old_name=[\'"]puzzles_{model_name}[\'"]')


def find_create(model_name):
  return find_for_pattern(rf'CreateModel.*name=[\'"]puzzles_{model_name}[\'"]')


if __name__ == '__main__':
  files_where_create = find_create('puzzle')
  files_where_rename = find_rename('puzzle')

  if files_where_rename:
    print('renamed in:')
    for rename in files_where_rename:
      print(rename)
  else:
    print('no renaming found')

