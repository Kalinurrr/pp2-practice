import os
import pygame


class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()

        self.music_folder = music_folder
        self.playlist = self.load_tracks()
        self.current_index = 0

        self.is_playing = False
        self.is_paused = False

        self.track_start_time = 0
        self.track_length = 0

    def load_tracks(self):
        tracks = []

        if not os.path.exists(self.music_folder):
            return tracks

        for file_name in sorted(os.listdir(self.music_folder)):
            if file_name.lower().endswith((".wav", ".mp3")):
                full_path = os.path.join(self.music_folder, file_name)
                tracks.append(full_path)

        return tracks

    def get_current_track_path(self):
        if not self.playlist:
            return None
        return self.playlist[self.current_index]

    def get_current_track_name(self):
        path = self.get_current_track_path()
        if path is None:
            return "No tracks found"
        return os.path.basename(path)

    def load_current_track(self):
        if not self.playlist:
            return

        current_track = self.get_current_track_path()
        pygame.mixer.music.load(current_track)

        # Get track length
        sound = pygame.mixer.Sound(current_track)
        self.track_length = sound.get_length()

    def play(self):
        if not self.playlist:
            return

        self.load_current_track()
        pygame.mixer.music.play()

        self.is_playing = True
        self.is_paused = False
        self.track_start_time = pygame.time.get_ticks()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.track_start_time = 0

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def update(self):
        # If music finished, automatically go to next track
        if self.is_playing and not pygame.mixer.music.get_busy() and not self.is_paused:
            self.next_track()

    def get_progress_seconds(self):
        if not self.is_playing:
            return 0

        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0

        return pos_ms / 1000

    def get_progress_text(self):
        current_sec = int(self.get_progress_seconds())
        total_sec = int(self.track_length)

        current_min = current_sec // 60
        current_remain = current_sec % 60

        total_min = total_sec // 60
        total_remain = total_sec % 60

        return f"{current_min:02}:{current_remain:02} / {total_min:02}:{total_remain:02}"