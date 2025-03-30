# Music Metadata Editor

A command-line Python script designed to help organize your music collection by renaming audio files and editing their metadata interactively. This script scans a specified directory for audio files (MP3 and OGG), displays their current metadata (artist, title, album), and then prompts the user to enter new information. It updates the embedded metadata tags using the `mutagen` library and renames the file based on the new artist and title. Processed files are moved into a `DONE` subdirectory within the original directory to keep things tidy.
