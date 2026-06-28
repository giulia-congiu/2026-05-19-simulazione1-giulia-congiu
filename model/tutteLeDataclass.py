"""
╔══════════════════════════════════════════════════════════════════╗
║         CHINOOK — DATACLASS PER TUTTE LE TABELL   ║
╚══════════════════════════════════════════════════════════════════╝

Regole ORM del professore:
- Una dataclass per ogni entità principale
- Le tabelle n:m (PlaylistTrack) di solito NON hanno dataclass
- Le FK si possono omettere o includere se servono per il grafo
- __eq__ e __hash__ sulla PRIMARY KEY
- __str__ leggibile per la UI

PlaylistTrack è inclusa come eccezione (può servire).
"""

from dataclasses import dataclass
from datetime import datetime


# ================================================================
# ARTIST
# ================================================================

@dataclass
class Artist:
    ArtistId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __hash__(self):
        return hash(self.ArtistId)


# ================================================================
# ALBUM
# ================================================================

@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int       # FK → Artist

    def __str__(self):
        return f"{self.Title}"

    def __eq__(self, other):
        return self.AlbumId == other.AlbumId

    def __hash__(self):
        return hash(self.AlbumId)


# ================================================================
# TRACK
# ================================================================

@dataclass
class Track:
    TrackId: int
    Name: str
    AlbumId: int         # FK → Album
    MediaTypeId: int     # FK → MediaType
    GenreId: int         # FK → Genre
    Composer: str
    Milliseconds: int
    Bytes: int
    UnitPrice: float

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.TrackId == other.TrackId

    def __hash__(self):
        return hash(self.TrackId)


# ================================================================
# GENRE
# ================================================================

@dataclass
class Genre:
    GenreId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.GenreId == other.GenreId

    def __hash__(self):
        return hash(self.GenreId)


# ================================================================
# MEDIATYPE
# ================================================================

@dataclass
class MediaType:
    MediaTypeId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.MediaTypeId == other.MediaTypeId

    def __hash__(self):
        return hash(self.MediaTypeId)


# ================================================================
# PLAYLIST
# ================================================================

@dataclass
class Playlist:
    PlaylistId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"

    def __eq__(self, other):
        return self.PlaylistId == other.PlaylistId

    def __hash__(self):
        return hash(self.PlaylistId)


# ================================================================
# PLAYLISTTRACK (tabella n:m — di solito non serve come dataclass)
# ================================================================

@dataclass
class PlaylistTrack:
    PlaylistId: int      # FK → Playlist
    TrackId: int         # FK → Track

    def __str__(self):
        return f"Playlist {self.PlaylistId} - Track {self.TrackId}"

    def __eq__(self, other):
        return self.PlaylistId == other.PlaylistId and self.TrackId == other.TrackId

    def __hash__(self):
        return hash((self.PlaylistId, self.TrackId))


# ================================================================
# CUSTOMER
# ================================================================

@dataclass
class Customer:
    CustomerId: int
    FirstName: str
    LastName: str
    Company: str
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str
    SupportRepId: int    # FK → Employee

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

    def __eq__(self, other):
        return self.CustomerId == other.CustomerId

    def __hash__(self):
        return hash(self.CustomerId)


# ================================================================
# EMPLOYEE
# ================================================================

@dataclass
class Employee:
    EmployeeId: int
    LastName: str
    FirstName: str
    Title: str
    ReportsTo: int       # FK → Employee (self-referencing)
    BirthDate: datetime
    HireDate: datetime
    Address: str
    City: str
    State: str
    Country: str
    PostalCode: str
    Phone: str
    Fax: str
    Email: str

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

    def __eq__(self, other):
        return self.EmployeeId == other.EmployeeId

    def __hash__(self):
        return hash(self.EmployeeId)


# ================================================================
# INVOICE
# ================================================================

@dataclass
class Invoice:
    InvoiceId: int
    CustomerId: int      # FK → Customer
    InvoiceDate: datetime
    BillingAddress: str
    BillingCity: str
    BillingState: str
    BillingCountry: str
    BillingPostalCode: str
    Total: float

    def __str__(self):
        return f"Invoice {self.InvoiceId} - {self.Total}€"

    def __eq__(self, other):
        return self.InvoiceId == other.InvoiceId

    def __hash__(self):
        return hash(self.InvoiceId)


# ================================================================
# INVOICELINE
# ================================================================

@dataclass
class InvoiceLine:
    InvoiceLineId: int
    InvoiceId: int       # FK → Invoice
    TrackId: int         # FK → Track
    UnitPrice: float
    Quantity: int

    def __str__(self):
        return f"InvoiceLine {self.InvoiceLineId} - Qty: {self.Quantity}"

    def __eq__(self, other):
        return self.InvoiceLineId == other.InvoiceLineId

    def __hash__(self):
        return hash(self.InvoiceLineId)


# ================================================================
# NOTE RAPIDE PER IL DAO
# ================================================================

"""
Nel DAO, per creare un oggetto da una riga del cursor:

    result.append(Artist(row["ArtistId"], row["Name"]))

    result.append(Customer(
        row["CustomerId"], row["FirstName"], row["LastName"],
        row["Company"], row["Address"], row["City"],
        row["State"], row["Country"], row["PostalCode"],
        row["Phone"], row["Fax"], row["Email"],
        row["SupportRepId"]
    ))

Oppure con **row (se i nomi dei campi corrispondono esattamente):

    result.append(Artist(**row))

Ricorda: cursor = conn.cursor(dictionary=True) per avere row come dict.
"""