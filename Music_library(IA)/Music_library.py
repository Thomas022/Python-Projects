"""An incremental object-oriented Python music library exercise.

The prints come from the demo and tests that run when you execute the file directly. Importing
  its classes skips those, so you can try them yourself without changing the file.

  In Terminal, run:

  cd ~/Desktop
  python3 -i -c "from music_library import Track, Song, Episode, Audiobook, Playlist"

  At the >>> prompt, try:

  song = Song("Imagine", "John Lennon", 183, "Rock")
  song.title
  song.duration_formatted

  playlist = Playlist("My Favorites")
  playlist.add_track(song)
  playlist.total_duration_formatted

Docstrings describe classes and methods; comments explain individual steps.
"""


class Track:
    """Represent an audio track with validated metadata and playback counters."""

    # Class attribute: shared by every Track and its subclass instances.
    total_plays = 0

    def __init__(self, title: str, artist: str, duration: int):
        """Initialize a track; reject empty title/artist or nonpositive seconds."""
        # Validate all constructor inputs before assigning instance attributes.
        if not title:
            raise ValueError("Title must not be empty.")
        if not artist:
            raise ValueError("Artist must not be empty.")
        if duration <= 0:
            raise ValueError("Duration must be greater than 0 seconds.")

        # A single underscore marks nonpublic data by convention, not enforcement.
        self._title = title
        self._artist = artist
        self._duration = duration
        # Instance attribute: each new track starts with its own count of zero.
        self.play_count = 0

    # Properties replace the original getter methods: use track.title, not title().
    @property
    def title(self):
        """Return the title through a read-only property."""
        return self._title

    @property
    def artist(self):
        """Return the artist through a read-only property."""
        return self._artist

    @property
    def duration(self):
        """Return the duration in seconds, or validate a new positive duration."""
        return self._duration

    # Assignment such as track.duration = 400 calls this setter automatically.
    @duration.setter
    def duration(self, value: int):
        """Return the duration in seconds, or validate a new positive duration."""
        if value <= 0:
            raise ValueError("Duration must be positive")
        self._duration = value

    @property
    def duration_formatted(self):
        """Return minutes and seconds as M:SS without providing a setter."""
        # divmod gives whole minutes and leftover seconds; :02d pads seconds.
        minutes, seconds = divmod(self._duration, 60)
        return f"{minutes}:{seconds:02d}"

    def __str__(self):
        """Return a human-readable description used by print(track)."""
        return f"{self._title} by {self._artist} ({self.duration_formatted})"

    def __repr__(self):
        """Return a Track constructor expression with safely quoted strings."""
        # !r preserves Python quoting and escaping in constructor arguments.
        return f"Track({self._title!r}, {self._artist!r}, {self._duration!r})"

    def play(self):
        """Count this play globally and individually, then print a playback message."""
        Track.total_plays += 1
        self.play_count += 1
        print(f"Now playing: {self._title} by {self._artist}")

    def get_info(self):
        """Return, rather than print, the title, artist, and M:SS duration."""
        # divmod gives whole minutes and leftover seconds; :02d pads seconds.
        minutes, seconds = divmod(self._duration, 60)
        return f"{self._title} by {self._artist} ({minutes}:{seconds:02d})"

    def extend_duration(self, extra_seconds: int):
        """Add extra seconds to the stored duration and print the new total."""
        self._duration += extra_seconds
        print(f"New total duration: {self._duration} seconds")


class Song(Track):
    """Extend Track with a genre and song-specific descriptions and playback."""

    def __init__(self, title: str, artist: str, duration: int, genre: str):
        """Initialize inherited track metadata, then store the genre."""
        # Reuse the parent constructor and its validation before adding new data.
        super().__init__(title, artist, duration)
        self._genre = genre

    @property
    def genre(self):
        """Return the protected genre through a read-only property."""
        return self._genre

    def __str__(self):
        """Append the genre to the readable parent description."""
        return f"{super().__str__()} - Genre: {self._genre}"

    def __repr__(self):
        """Return a Song constructor expression including genre."""
        return f"Song({self._title!r}, {self._artist!r}, {self._duration!r}, {self._genre!r})"

    def play(self):
        """Increment both counters and print the song genre with its metadata."""
        Track.total_plays += 1
        self.play_count += 1
        print(f"Now playing {self._genre} song: {self._title} by {self._artist}")

    def get_info(self):
        """Extend the parent information string with the song genre."""
        # Extend the parent result instead of duplicating its formatting logic.
        info = super().get_info()
        return f"{info} - Genre: {self._genre}"


class Episode(Track):
    """Extend Track with a podcast host and episode number."""

    def __init__(self, title: str, artist: str, duration: int, host: str, episode_number: int):
        """Initialize inherited metadata and the public podcast attributes."""
        # Reuse the parent constructor and its validation before adding new data.
        super().__init__(title, artist, duration)
        self.host = host
        self.episode_number = episode_number

    def __str__(self):
        """Include the episode number and host in the readable description."""
        return f"{super().__str__()} - Episode {self.episode_number}, hosted by {self.host}"

    def __repr__(self):
        """Return an Episode constructor expression including host and number."""
        return (
            f"Episode({self._title!r}, {self._artist!r}, {self._duration!r}, "
            f"{self.host!r}, {self.episode_number!r})"
        )

    def play(self):
        """Increment both counters and announce the podcast episode and host."""
        Track.total_plays += 1
        self.play_count += 1
        print(f"Now playing podcast: {self._title} - Episode {self.episode_number}, hosted by {self.host}")


class Audiobook(Track):
    """Extend Track with a narrator, chapter count, and current chapter."""

    def __init__(self, title: str, artist: str, duration: int, narrator: str, chapter_count: int):
        """Initialize the audiobook metadata and start at chapter one."""
        # Reuse the parent constructor and its validation before adding new data.
        super().__init__(title, artist, duration)
        self.narrator = narrator
        self.chapter_count = chapter_count
        # Chapter numbering starts at one rather than zero.
        self.current_chapter = 1

    def __str__(self):
        """Include current chapter, total chapters, and narrator for display."""
        return (
            f"{super().__str__()} - Chapter {self.current_chapter} of {self.chapter_count}, "
            f"narrated by {self.narrator}"
        )

    def __repr__(self):
        """Return an Audiobook constructor expression with narrator and chapter count."""
        return (
            f"Audiobook({self._title!r}, {self._artist!r}, {self._duration!r}, "
            f"{self.narrator!r}, {self.chapter_count!r})"
        )

    def next_chapter(self):
        """Advance one chapter unless already at the last chapter."""
        # This boundary check prevents advancing past the final chapter.
        if self.current_chapter < self.chapter_count:
            self.current_chapter += 1

    def play(self):
        """Increment both counters and announce the current audiobook chapter."""
        Track.total_plays += 1
        self.play_count += 1
        print(
            f"Now playing audiobook: {self._title} - "
            f"Chapter {self.current_chapter} of {self.chapter_count}, "
            f"narrated by {self.narrator}"
        )


class Playlist:
    """Collect Track objects, including subclasses, and play them in order."""

    def __init__(self, name: str):
        """Store the playlist name and create its own initially empty track list."""
        self.name = name
        # Create the list per instance so playlists do not share their contents.
        self._tracks = []

    def add_track(self, track: Track):
        """Append a track to the playlist in insertion order."""
        self._tracks.append(track)

    def get_total_duration(self):
        """Return the sum of track durations in seconds; return zero when empty."""
        return sum(track.duration for track in self._tracks)

    @property
    def total_duration_formatted(self):
        """Return total duration as H:MM:SS through a read-only property."""
        # Split into hours, then minutes and seconds; pad the last two fields.
        hours, remainder = divmod(self.get_total_duration(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def play_all(self):
        """Call each stored track's play method in playlist order."""
        # Polymorphism: each object selects its own overridden play implementation.
        for track in self._tracks:
            track.play()


def run_demo():
    """Demonstrate the library and verify its main behaviors."""
    # Save the baseline so repeated demo calls also verify the shared counter.
    starting_plays = Track.total_plays
    track = Track("Sound Effect", "Studio", 5)
    song = Song("Imagine", "John Lennon", 183, "Rock")
    episode = Episode("Tech Talk", "NPR", 1800, "Jane Smith", 42)
    audiobook = Audiobook("The Hobbit", "J.R.R. Tolkien", 39600, "Martin Freeman", 19)
    tracks = [track, song, episode, audiobook]

    # Access inherited properties and show both string representations.
    for item in tracks:
        print(f"Title: {item.title}, artist: {item.artist}, duration: {item.duration} seconds")
        print(f"Formatted duration: {item.duration_formatted}")
        print(item.get_info())
        print(item)  # Calls __str__ for a readable description.
        print(repr(item))  # Calls __repr__ for a constructor-style description.
        assert item.play_count == 0

    # Demonstrate the duration setter and extension method.
    track.duration = 10
    assert track.duration == 10
    track.extend_duration(5)
    assert track.duration == 15
    assert track.duration_formatted == "0:15"
    for invalid_duration in (0, -10):
        try:
            track.duration = invalid_duration
        except ValueError as error:
            print(error)
            assert str(error) == "Duration must be positive"
        else:
            raise AssertionError("Invalid duration was accepted")
        assert track.duration == 15

    # Constructor validation must reject each invalid input.
    for arguments in (("", "Studio", 5), ("Sound Effect", "", 5),
                      ("Sound Effect", "Studio", 0)):
        try:
            Track(*arguments)
        except ValueError as error:
            print(error)
        else:
            raise AssertionError("Invalid Track input was accepted")

    # Child classes expose their additional features.
    print(f"Song genre: {song.genre}")
    assert song.get_info() == "Imagine by John Lennon (3:03) - Genre: Rock"
    print(f"Episode {episode.episode_number}, hosted by {episode.host}")
    print(f"Narrator: {audiobook.narrator}, chapters: {audiobook.chapter_count}")
    audiobook.play()
    audiobook.next_chapter()
    audiobook.next_chapter()
    assert audiobook.current_chapter == 3
    audiobook.play()
    for _ in range(audiobook.chapter_count):
        audiobook.next_chapter()
    assert audiobook.current_chapter == audiobook.chapter_count
    print(f"Chapter navigation stops at chapter {audiobook.current_chapter}")

    # The same method call invokes each type's own playback behavior.
    print("Playing a mixed list:")
    for item in tracks:
        item.play()

    # Composition: a playlist contains tracks rather than inheriting from Track.
    playlist = Playlist("My Favorites")
    assert playlist.get_total_duration() == 0
    assert playlist.total_duration_formatted == "0:00:00"
    playlist.play_all()
    for item in tracks:
        playlist.add_track(item)
    print(f"Playlist: {playlist.name}")
    print(f"Total duration: {playlist.get_total_duration()} seconds")
    print(f"Formatted total: {playlist.total_duration_formatted}")
    assert playlist.get_total_duration() == 41598
    assert playlist.total_duration_formatted == "11:33:18"
    playlist.play_all()

    # Every track played twice; the audiobook also played twice during navigation.
    for item, expected_count in zip(tracks, (2, 2, 2, 4)):
        print(f"{item.title} play count: {item.play_count}")
        assert item.play_count == expected_count
    demo_plays = sum(item.play_count for item in tracks)
    assert Track.total_plays == starting_plays + demo_plays
    print(f"Total plays: {Track.total_plays} ({demo_plays} during this demo)")
    print("All demo checks passed.")


def test_validation():
    """Report whether each invalid input raises ValueError."""
    def set_invalid_duration():
        """Exercise the setter using an otherwise valid Track instance."""
        track = Track("Sound Effect", "Studio", 5)
        track.duration = -10

    # Lambdas delay construction until each case runs inside its try block.
    tests = [
        ("Empty title", lambda: Track("", "Studio", 5)),
        ("Empty artist", lambda: Track("Sound Effect", "", 5)),
        ("Zero duration", lambda: Track("Sound Effect", "Studio", 0)),
        ("Invalid duration setter", set_invalid_duration),
    ]

    for name, test in tests:
        try:
            test()
        except ValueError as error:
            print(f"PASSED: {name} - {error}")
        # A different exception is a failed test; continue to the remaining cases.
        except Exception as error:
            print(f"FAILED: {name} - expected ValueError, got {type(error).__name__}: {error}")
        else:
            print(f"FAILED: {name} - no ValueError was raised")


# Run examples when executed as a script; importing only defines the API.
if __name__ == "__main__":
    run_demo()
    test_validation()
