# -- 1. Elenca tutti gli artisti
# select *
# from artist;
#
#
# -- 2. Elenca gli artisti che hanno almeno un album
# select distinct a.*
# from artist a, album a2
# where a.ArtistId = a2.ArtistId;
#
#
# -- 3. Elenca tutti gli album con il nome dell'artista
# select distinct a.Name artista, a2.Title
# from artist a, album a2
# where a.ArtistId = a2.ArtistId;
#
#
# -- 4. Elenca tutte le tracce con artista e album
# select distinct a.Name artista, a2.Title, t.Name
# from artist a, album a2, track t
# where a.ArtistId = a2.ArtistId
# and t.AlbumId = a2.AlbumId;
#
#
# -- 5. Elenca tutte le tracce con genere
# select t.Name, g.Name
# from track t, genre g
# where t.GenreId = g.GenreId;
#
#
# -- 6. Elenca tutte le tracce con media type
# select t.Name, m.Name
# from track t, mediatype m
# where t.MediaTypeId = m.MediaTypeId;
#
#
# -- 7. Elenca tutti gli artisti che hanno almeno una traccia Rock
# select distinct a.Name, a.ArtistId
# from artist a, album a2, track t, genre g
# where t.GenreId = g.GenreId
# and t.AlbumId = a2.AlbumId
# and a2.ArtistId = a.ArtistId
# and g.Name = 'Rock';
#
#
# -- 8. Elenca tutti i generi presenti negli album di un artista
# select distinct a.Name, a2.Title, g.Name
# from artist a, album a2, track t, genre g
# where a.ArtistId = a2.ArtistId
# and a2.AlbumId = t.AlbumId
# and t.GenreId = g.GenreId;
#
#
# -- 9. Elenca tutti gli album che contengono almeno una traccia Jazz
# select distinct a.Title
# from album a, track t, genre g
# where a.AlbumId = t.AlbumId
# and t.GenreId = g.GenreId
# and g.Name = 'Jazz';
#
#
# -- 10. Elenca tutti gli artisti che hanno almeno una traccia acquistata
# select distinct a.Name
# from artist a, album a2, track t, invoiceline i
# where a.ArtistId = a2.ArtistId
# and a2.AlbumId = t.AlbumId
# and t.TrackId = i.TrackId;
#
#
# -- 11. Elenca tutti i clienti che hanno acquistato almeno una traccia Rock
# select distinct c.CustomerId
# from customer c, invoice i, invoiceline i2, track t, genre g
# where c.CustomerId = i.CustomerId
# and i.InvoiceId = i2.InvoiceId
# and i2.TrackId = t.TrackId
# and t.GenreId = g.GenreId
# and g.Name = 'Rock';
#
#
# -- 12. Elenca tutti i clienti che hanno acquistato almeno un brano dello stesso artista
# select distinct c.CustomerId
# from customer c, invoice i, invoiceline i2, track t, album a
# where c.CustomerId = i.CustomerId
# and i.InvoiceId = i2.InvoiceId
# and i2.TrackId = t.TrackId
# and t.AlbumId = a.AlbumId;
#
#
# -- 13. Numero di album per artista
# select a.Name, count(*)
# from artist a, album a2
# where a.ArtistId = a2.ArtistId
# group by a.ArtistId;
#
#
# -- 14. Numero di tracce per album
# select a.Title, count(*)
# from album a, track t
# where a.AlbumId = t.AlbumId
# group by a.Title;
#
#
# -- 15. Numero di tracce per genere
# select g.Name, count(*)
# from track t, genre g
# where g.GenreId = t.GenreId
# group by g.GenreId;
#
#
# -- 16. Durata totale delle tracce per artista
# select a2.Name, sum(t.Milliseconds)
# from track t, album a, artist a2
# where a.ArtistId = a2.ArtistId
# and a.AlbumId = t.AlbumId
# group by a2.Name;
#
#
# -- 17. Prezzo medio delle tracce per genere
# select g.Name, avg(t.UnitPrice)
# from track t, genre g
# where g.GenreId = t.GenreId
# group by g.GenreId;
#
#
# -- 18. Numero di clienti che hanno acquistato almeno un brano di ciascun artista
# select a2.Name, count(distinct i.CustomerId)
# from invoice i, invoiceline i2, track t, album a, artist a2
# where a2.ArtistId = a.ArtistId
# and a.AlbumId = t.AlbumId
# and t.TrackId = i2.TrackId
# and i2.InvoiceId = i.InvoiceId
# group by a2.ArtistId
#
#
# -- 19. Tutti gli artisti acquistati dal cliente X
# select distinct a2.Name
# from invoice i, invoiceline i2, track t, album a, artist a2
# where a2.ArtistId = a.ArtistId
# and a.AlbumId = t.AlbumId
# and t.TrackId = i2.TrackId
# and i2.InvoiceId = i.InvoiceId
# and i.CustomerId = 37;
#
#
# -- 20. Tutti i generi acquistati dal cliente X
# select distinct g.Name
# from invoice i, invoiceline i2, track t, genre g
# where g.GenreId = t.GenreId
# and t.TrackId = i2.TrackId
# and i2.InvoiceId = i.InvoiceId
# and i.CustomerId = 54;
#
#
# PARTE 2
# -- 1
# -- nodi

# select distinct a.Name
# from artist a, album a2 , track t , playlisttrack p
# where a.ArtistId = a2.ArtistId
# and a2.AlbumId = t.AlbumId
# and t.TrackId = p.TrackId

# -- archi
# SELECT pt.PlaylistId, a.ArtistId
# FROM playlisttrack pt, track t, album a
# WHERE pt.TrackId = t.TrackId
# AND t.AlbumId = a.AlbumId
# GROUP BY pt.PlaylistId, a.ArtistId


# -- 2
# #NODI: clienti che hanno acquistato almeno 1 traccia rock
# #Arco: due clienti sono collegati se hanno acquistato almeno un genere in comune.
# # Verso: dal cliente che ha acquistato più tracce al cliente che ne ha acquistate meno.
# # In caso di parità inserire entrambi gli archi.
# # Peso: somma del numero di tracce acquistate dai due clienti.

# select distinct c.CustomerId
# from invoice i , invoiceline i2 , customer c , track t , genre g
# where i.InvoiceId = i2.InvoiceId
# and i2.TrackId = t.TrackId
# and t.GenreId = g.GenreId
# and g.Name = 'Rock'
# and i.CustomerId = c.CustomerId
# order by c.CustomerId

# select g.Name , c.CustomerId
# from invoice i , invoiceline i2 , customer c , track t , genre g
# where i.InvoiceId = i2.InvoiceId
# and i2.TrackId = t.TrackId
# and t.GenreId = g.GenreId
# and i.CustomerId = c.CustomerId
# group by g.Name , c.CustomerId


# -- 3
# #Costruire un grafo non orientato.
# # Nodi: album contenenti almeno 5 tracce.
# # Arco: due album sono collegati se almeno un cliente ha acquistato tracce di entrambi.
# # Peso: numero di clienti in comune.

# select al.Title
# from album al, track t
# where al.AlbumId = t.AlbumId
# group by al.Title
# having count(t.TrackId)>=5

# select i.CustomerId , a.Title
# from invoice i ,invoiceline i2 , track t , album a
# where a.AlbumId = t.AlbumId
# and t.TrackId = i2.TrackId
# and i.InvoiceId = i2.InvoiceId
# group by i.CustomerId , a.Title


# -- 4
# #Costruire un grafo orientato.
# #Nodi: tutti i dipendenti.
# #Arco: esiste un arco dal responsabile al subordinato.
# #Peso: differenza di età tra i due.
# select *
# from employee e

# select e2.EmployeeId, e.EmployeeId, ABS(TIMESTAMPDIFF(YEAR, e.BirthDate, e2.BirthDate)) peso
# from employee e , employee e2
# where e.ReportsTo = e2.EmployeeId


# -- 5
# #Costruire un grafo non orientato.
# #Nodi: tutti i dipendenti.
# #Arco: due dipendenti sono collegati se hanno lo stesso responsabile.
# #Peso: numero totale di clienti gestiti dai due dipendenti.

# select *
# from employee e

# select e1.EmployeeId, e2.EmployeeId, COUNT(DISTINCT c1.CustomerId) + COUNT(DISTINCT c2.CustomerId) as peso
# from employee e1 , employee e2 , customer c1, customer c2
# where e2.ReportsTo = e1.ReportsTo
# and e1.EmployeeId = c1.SupportRepId
# and e2.EmployeeId = c2.SupportRepId
# and e1.EmployeeId > e2.EmployeeId
# and e1.ReportsTo is not null
# group by e1.EmployeeId, e2.EmployeeId


# -- 6
# #Costruire un grafo non orientato.
# #Nodi: tutti i generi acquistati almeno una volta.
# #Arco: due generi sono collegati se almeno un cliente ha acquistato entrambi.
# #Peso: numero di clienti.

# select distinct g.Name
# from genre g , track t , invoiceline i
# where i.TrackId = t.TrackId
# and t.GenreId = g.GenreId


# SELECT g1.Name, g2.Name, COUNT(DISTINCT i1.CustomerId) as peso
# FROM invoice i1, invoiceline il1, track t1, genre g1,
#     invoice i2, invoiceline il2, track t2, genre g2
# WHERE i1.InvoiceId = il1.InvoiceId
# AND il1.TrackId = t1.TrackId
# AND t1.GenreId = g1.GenreId
# AND i2.InvoiceId = il2.InvoiceId
# AND il2.TrackId = t2.TrackId
# AND t2.GenreId = g2.GenreId
# AND i1.CustomerId = i2.CustomerId
# AND g1.GenreId < g2.GenreId
# GROUP BY g1.Name, g2.Name


# -- 7
# #Costruire un grafo non orientato.
# #Nodi: tutte le playlist.
# #Arco: due playlist sono collegate se condividono almeno una traccia.
# #Peso: numero di tracce condivise.
# select *
# from playlist p
#
# select p2.PlaylistId , p.PlaylistId, count(distinct p2.TrackId) as peso
# from playlisttrack p , playlisttrack p2
# where p2.PlaylistId < p.PlaylistId
# and p2.TrackId = p.TrackId
# group by p2.PlaylistId , p.PlaylistId


# -- 8
# #Costruire un grafo orientato.
# #Nodi: tutti i media type.
# #Arco: due media type sono collegati se almeno un cliente ha acquistato entrambi.
# #Verso: dal media type con più acquisti verso quello con meno acquisti.
# #Peso: somma degli acquisti. = poplarità

# select *
# from mediatype m

# SELECT pop1.MediaTypeId, pop2.MediaTypeId,
#       pop1.acquisti + pop2.acquisti as peso,
#       pop1.acquisti as pop1_acq, pop2.acquisti as pop2_acq
# FROM (
#    SELECT t.MediaTypeId, COUNT(*) as acquisti
#    FROM invoiceline il, track t
#    WHERE il.TrackId = t.TrackId
#    GROUP BY t.MediaTypeId
# ) pop1,
# (
#    SELECT t.MediaTypeId, COUNT(*) as acquisti
#    FROM invoiceline il, track t
#    WHERE il.TrackId = t.TrackId
#    GROUP BY t.MediaTypeId
# ) pop2
# WHERE pop1.MediaTypeId < pop2.MediaTypeId
# AND EXISTS (
#    SELECT 1
#    FROM invoice i1, invoiceline il1, track t1,
#         invoice i2, invoiceline il2, track t2
#    WHERE i1.InvoiceId = il1.InvoiceId
#    AND il1.TrackId = t1.TrackId
#    AND t1.MediaTypeId = pop1.MediaTypeId
#    AND i2.InvoiceId = il2.InvoiceId
#    AND il2.TrackId = t2.TrackId
#    AND t2.MediaTypeId = pop2.MediaTypeId
#    AND i1.CustomerId = i2.CustomerId
# )

# #meglio FARLO su pyhton
# SELECT i.CustomerId, t.MediaTypeId
# FROM invoice i, invoiceline il, track t
# WHERE i.InvoiceId = il.InvoiceId
# AND il.TrackId = t.TrackId
# GROUP BY i.CustomerId, t.MediaTypeId


# #Regola:
# #Peso = conteggio dell'elemento condiviso (tracce in comune, clienti in comune, playlist in comune)
# #→ funziona in SQL con COUNT(DISTINCT) nel self-join.

# #Peso = proprietà dei singoli nodi sommate (popolarità di A + popolarità di B, acquisti di A + acquisti di B)
# → non funziona nel self-join perché il prodotto cartesiano gonfia i numeri. Serve calcolarli separatamente.

# -- 9
# #Costruire un grafo orientato.
# #Nodi: tutti gli artisti con almeno una traccia acquistata.
# #Arco: due artisti sono collegati se almeno un cliente ha acquistato entrambi.
# #Verso: dall'artista con durata totale delle tracce maggiore verso quello con durata minore.
# #Peso: somma delle durate.

# select distinct a.Name
# from artist a , album a2 , track t , invoiceline i
# where a.ArtistId = a2.ArtistId
# and a2.AlbumId =t.AlbumId
# and i.TrackId = t.TrackId

# -- seleziono archi
# SELECT i.CustomerId, a.ArtistId
# FROM invoice i, invoiceline il, track t, album a
# WHERE i.InvoiceId = il.InvoiceId
# AND il.TrackId = t.TrackId
# AND t.AlbumId = a.AlbumId
# GROUP BY i.CustomerId, a.ArtistId

# -- prendo i pesi
# SELECT a.ArtistId, SUM(t.Milliseconds) as durata
# FROM artist a, album al, track t, invoiceline il
# WHERE a.ArtistId = al.ArtistId
# AND al.AlbumId = t.AlbumId
# AND t.TrackId = il.TrackId
# GROUP BY a.ArtistId

# -- 10
# -- Costruire un grafo non orientato.
# -- Nodi: clienti.
# -- Arco: due clienti sono collegati se hanno acquistato almeno una stessa traccia.
# -- Peso: numero di tracce acquistate in comune.

# -- Nodi
# SELECT DISTINCT c.CustomerId, c.FirstName, c.LastName
# FROM customer c, invoice i, invoiceline il
# WHERE c.CustomerId = i.CustomerId
# AND i.InvoiceId = il.InvoiceId

# -- Archi (SQL — self-join corta)
# SELECT i1.CustomerId, i2.CustomerId, COUNT(DISTINCT il1.TrackId) as peso
# FROM invoiceline il1, invoice i1, invoiceline il2, invoice i2
# WHERE il1.InvoiceId = i1.InvoiceId
# AND il2.InvoiceId = i2.InvoiceId
# AND il1.TrackId = il2.TrackId
# AND i1.CustomerId < i2.CustomerId
# GROUP BY i1.CustomerId, i2.CustomerId


# -- 11
# -- Costruire un grafo non orientato.
# -- Nodi: artisti.
# -- Arco: due artisti sono collegati se appartengono allo stesso genere.
# -- Peso: numero di generi condivisi.

# -- Nodi
# SELECT DISTINCT a.ArtistId, a.Name
# FROM artist a, album al, track t
# WHERE a.ArtistId = al.ArtistId
# AND al.AlbumId = t.AlbumId

# -- Query per Python (CASO D)
# SELECT t.GenreId, a.ArtistId
# FROM artist a, album al, track t
# WHERE a.ArtistId = al.ArtistId
# AND al.AlbumId = t.AlbumId
# GROUP BY t.GenreId, a.ArtistId


# -- 12
# -- Costruire un grafo orientato.
# -- Nodi: album acquistati almeno una volta.
# -- Arco: due album sono collegati se almeno un cliente ha acquistato entrambi.
# -- Verso: dall'album con più vendite verso quello con meno vendite.
# -- Peso: somma delle vendite.

# -- Nodi
# SELECT DISTINCT a.AlbumId, a.Title
# FROM album a, track t, invoiceline il
# WHERE a.AlbumId = t.AlbumId
# AND t.TrackId = il.TrackId

# -- Query per Python (CASO E)
# SELECT i.CustomerId, t.AlbumId
# FROM invoice i, invoiceline il, track t
# WHERE i.InvoiceId = il.InvoiceId
# AND il.TrackId = t.TrackId
# GROUP BY i.CustomerId, t.AlbumId


# -- 13
# -- Costruire un grafo non orientato.
# -- Nodi: playlist.
# -- Arco: due playlist sono collegate se contengono almeno un genere musicale in comune.
# -- Peso: numero di generi condivisi.

# -- Nodi
# SELECT *
# FROM playlist
#
# -- Query per Python (CASO D)
# SELECT pt.PlaylistId, t.GenreId
# FROM playlisttrack pt, track t
# WHERE pt.TrackId = t.TrackId
# GROUP BY pt.PlaylistId, t.GenreId


# -- 14
# -- Costruire un grafo orientato.
# -- Nodi: dipendenti.
# -- Arco: due dipendenti sono collegati se hanno assistito almeno un cliente della stessa città.
# -- Verso: dal dipendente con più clienti gestiti verso quello con meno clienti.
# -- Peso: somma dei clienti gestiti.

# -- Nodi
# SELECT *
# FROM employee
#
# -- Query per Python (CASO E) — elemento condiviso = città
# SELECT e.EmployeeId, c.City
# FROM employee e, customer c
# WHERE e.EmployeeId = c.SupportRepId
# GROUP BY e.EmployeeId, c.City
#
#
# -- Query separata per popolarità (clienti gestiti)
# SELECT SupportRepId, COUNT(*) as nClienti
# FROM customer
# GROUP BY SupportRepId

# -- 15
# -- Costruire un grafo orientato.
# -- Nodi: artisti che hanno almeno una traccia acquistata.
# -- Arco: due artisti sono collegati se almeno un cliente ha acquistato entrambi.
# -- Verso: dall'artista più popolare a quello meno popolare; parità = entrambi.
# -- Popolarità = numero totale di tracce acquistate.
# -- Peso: somma delle due popolarità.
# -- Nodi
# SELECT DISTINCT a.ArtistId, a.Name
# FROM artist a, album al, track t, invoiceline il
# WHERE a.ArtistId = al.ArtistId
# AND al.AlbumId = t.AlbumId
# AND t.TrackId = il.TrackId
#
#
# -- Query per Python (CASO E)
# SELECT i.CustomerId, al.ArtistId
# FROM invoice i, invoiceline il, track t, album al
# WHERE i.InvoiceId = il.InvoiceId
# AND il.TrackId = t.TrackId
# AND t.AlbumId = al.AlbumId
# GROUP BY i.CustomerId, al.ArtistId
#
#
# consegne ricorsione
#
#
# 1. Bike Store (esame 10/07/2025) — Cammino da Start Product a End Product, lunghezza esattamente Lun, rispettando i versi, nodo non ripetuto, peso massimo.
#  → Ottimizzo: peso | Limite: esatto | Nodo finale: sì | Vincolo: nessuno | Primo passo fuori: no
# 2. Formula 1 (esame 15/09/2025) — Dato K, scegliere K piloti da K componenti connesse diverse, minimizzando il range di età anagrafica.
#  → NON è un cammino — è selezione da componenti connesse (R5)
# 3. Simulazione Chinook (19/05/2026) — Cammino semplice di lunghezza massima con archi a peso strettamente crescente, partendo da un artista selezionato.
#  → Ottimizzo: lunghezza | Limite: nessuno | Nodo finale: no | Vincolo: peso crescente | Primo passo fuori: no (se usi lastWeight)
# 4. Simulazione IMDB (26/05/2026) — Cammino semplice di lunghezza massima con nodi a età strettamente decrescente.
#  → Ottimizzo: lunghezza | Limite: nessuno | Nodo finale: no | Vincolo: attributo nodo decrescente | Primo passo fuori: no
# 5. Baseball — Nessun nodo finale, nessuna lunghezza fissa, pesi strettamente decrescenti, peso massimo.
#  → Ottimizzo: peso | Limite: nessuno | Nodo finale: no | Vincolo: peso decrescente | Primo passo fuori: sì (nella sol del prof)
# 6. ARTS MIA — Lunghezza esatta, nessun nodo finale, tutti i nodi con stessa classification, peso massimo.
#  → Ottimizzo: peso | Limite: esatto | Nodo finale: no | Vincolo: attributo nodo | Primo passo fuori: no
# 7. FlightDelays — Nodo finale, lunghezza massima (max t tratte), peso massimo.
#  → Ottimizzo: peso | Limite: massimo | Nodo finale: sì | Vincolo: nessuno | Primo passo fuori: no
#
