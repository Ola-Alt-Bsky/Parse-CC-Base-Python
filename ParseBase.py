import json
from os import path, mkdir


def parse_to_json(lines):
    info = {}

    last_season = None
    last_episode = None
    last_attribute = None
    last_content = None
    last_specific = None

    for line in lines:
        starts_with_star = line.startswith('*')
        starts_with_space = line.startswith(' ')
        amount_leading_space = len(line) - len(line.lstrip())

        if not (starts_with_star or starts_with_space):  # Season
            line = line[:-1]
            info[line] = {}
            last_season = line
        elif starts_with_star:  # Episode
            line = line[:-1].replace('*', '').strip()
            info[last_season][line] = {}
            last_episode = line
        elif starts_with_space and amount_leading_space == 3:  # Attributes
            line = line[:-1].replace('*', '').strip()

            if line == 'Songs':
                info[last_season][last_episode][line] = {}
            else:
                info[last_season][last_episode][line] = []

            last_attribute = line
        elif starts_with_space and amount_leading_space == 6:  # Content
            line = line[:-1].replace('*', '').strip()

            if last_attribute == 'Songs':
                info[last_season][last_episode][last_attribute][line] = {}
            else:
                info[last_season][last_episode][last_attribute].append(line)

            last_content = line
        elif starts_with_space and amount_leading_space == 9:  # Specific
            line = line[:-1].replace('*', '').strip()

            if last_content == 'Scene Specific':
                info[last_season][last_episode][last_attribute][last_content][line] = {}
            else:
                info[last_season][last_episode][last_attribute][last_content] = line

            last_specific = line
        elif starts_with_space and amount_leading_space == 12:
            line = line[:-1].replace('*', '').strip()
            info[last_season][last_episode][last_attribute][last_content][last_specific] = line

    # Remove extra stuff
    del info['Chapter Template']
    del info['Extra Songs']

    return info


# Read input from a .txt file
file_path = "Casual Roleplay Base.txt"  # Replace with your file path
with open(file_path, "r", encoding="utf-8-sig") as file:
    file_lines = file.readlines()

# Parse and convert to JSON
parsed_json = parse_to_json(file_lines)

# Retrieve a list of characters, locations, and songs
characters = []
locations = []
songs = []
for season in parsed_json.values():
    for episode in season.values():
        characters.extend(episode['Characters'])
        locations.extend(episode['Locations'])
        songs.append(episode['Songs']['Intro Song'])
        songs.extend(episode['Songs']['Scene Specific'].values())
        songs.append(episode['Songs']['Outro Song'])
characters = list(set(characters))
locations = list(set(locations))
songs = list(set(songs))

# Save the parsed JSON information to a folder
output_dir = "Output"
output_name = "Casual_Roleplay"
output_path = path.join(output_dir, output_name)

if not path.exists(output_dir):
    mkdir(output_dir)

with open(output_path + '.json', "w", encoding="utf-8") as json_file:
    json.dump(parsed_json, json_file, indent=4)

print(f"Parsed JSON has been saved to {output_path + '.json'}.")

# Save a list of characters, locations, and songs
with open(output_path + "_characters.txt", "w", encoding="utf-8") as characters_file:
    characters_file.write("\n".join(characters))

print(f"Characters have been saved to {output_path + '_characters.txt'}.")

with open(output_path + "_locations.txt", "w", encoding="utf-8") as locations_file:
    locations_file.write("\n".join(locations))

print(f"Locations have been saved to {output_path + '_locations.txt'}.")

with open(output_path + "_songs.txt", "w", encoding="utf-8") as songs_file:
    songs_file.write("\n".join(songs))

print(f"Songs have been saved to {output_path + '_songs.txt'}.")
