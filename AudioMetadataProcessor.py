from os import rename, makedirs, scandir
from os.path import join, splitext, dirname, exists
from mutagen import File

class AudioMetadataProcessor:
    def __init__(self, directory):
        self.directory = directory

    def getAudioFiles(self):
        audioPaths = []
        with scandir(self.directory) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(('.mp3', '.ogg')):
                    audioPaths.append(entry.path)
        
        return audioPaths

    def printCurrentMetadata(self, filePath):
        audio = File(filePath, easy = True)
        if audio is None:
            print(f'Unsupported file type or unable to read metadata: {filePath}')
            return None

        # Define the relevant metadata keys.
        print(f'Current metadata for: {filePath}')
        for key in ['artist', 'title', 'album']:
            value = audio.get(key, ['[Not Found]'])
            print(f'    {key.capitalize()}: {value}')
        
        return audio

    def promptForNewMetadata(self):
        fields = {'artist': None, 'title': None, 'album': None, 'featuredArtists': None}
        keys = ['artist', 'title', 'album', 'featuredArtists']
        prompts = {'artist': 'Enter new artist name: ', 'title': 'Enter new song title: ', 'album': 'Enter new album: ',
                   'featuredArtists': 'Enter featured artists (comma separated, leave blank if none): '}
        
        # Routine enabling mistake correction.
        index = 0
        while index < len(keys):
            key = keys[index]
            userInput = input(prompts[key]).strip()
            if userInput.lower() == 'back':
                if index > 0:
                    index -= 1
                    print(f'Returning to previous field: {keys[index].capitalize()}')
                    continue
                else:
                    print('Already at the first field; cannot go back further.')
                    continue
            else:
                if key == 'featuredArtists':
                    fields[key] = [artist.strip() for artist in userInput.split(',') if artist.strip()] if userInput else []
                else:
                    fields[key] = userInput
                index += 1
        
        return fields['artist'], fields['title'], fields['album'], fields['featuredArtists']

    def updateAudioMetadata(self, filePath, audio, newArtist, newTitle, newAlbum, featuredArtists):
        combinedTitle = f'{newArtist} - {newTitle}'
        audio['albumartist'] = [newArtist]
        audio['title'] = [combinedTitle]
        audio['album'] = [newAlbum]
        if featuredArtists:
            contributingArtists = newArtist + ''.join(f' ft. {artist}' for artist in featuredArtists)
        else:
            contributingArtists = newArtist
        audio['artist'] = [contributingArtists]
        
        # Rename the file using the primary artist and song title.
        # Preserve original file extension.
        try:
            audio.save()
            print('Metadata updated successfully.')
        except Exception as e:
            print(f'Error saving metadata for {filePath}: {e}')
        ext = splitext(filePath)[1]
        newFileName = f'{newArtist} - {newTitle}{ext}'
        doneDirectory = join(dirname(filePath), 'DONE')
        if not exists(doneDirectory):
            makedirs(doneDirectory)
        newFilePath = join(doneDirectory, newFileName)

        try:
            rename(filePath, newFilePath)
            print(f'File renamed to: {newFileName}')
        except Exception as e:
            print(f'Error renaming file {filePath}: {e}')
        
        return newFilePath

    def processFile(self, filePath):
        audio = self.printCurrentMetadata(filePath)
        if audio is None:
            return
        print('Please provide new metadata values.')
        newArtist, newTitle, newAlbum, featuredArtists = self.promptForNewMetadata()
        self.updateAudioMetadata(filePath, audio, newArtist, newTitle, newAlbum, featuredArtists)

    def processAllFiles(self):
        audioFiles = self.getAudioFiles()
        if not audioFiles:
            print('No MP3 or OGG files found in the directory.')
            return
        for filePath in audioFiles:
            self.processFile(filePath)

if __name__ == '__main__':
    directory = r'C:\Users\giann\Downloads\Songs'
    processor = AudioMetadataProcessor(directory)
    processor.processAllFiles()