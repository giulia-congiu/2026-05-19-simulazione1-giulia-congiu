from dataclasses import dataclass


@dataclass
class Artista:
    ArtistId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __hash__(self):
        return hash(self.ArtistId)
