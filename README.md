# Projektas "Skelbiame"

## Sistemos paskirtis
Šio projekto tikslas yra sukurti svetainę, kurioje naudotojams būtu galima įkelti skelbimus.

Šią svetainę sudaro dvi dalys: internetinė aplikacija ir aplikacijų programavimo sąsaja.
Svečias galės prisiregistruoti prie svetainės ir peržiūrėti skelbimus ir komentarus po jais. Prisiregistravęs naudotojas galės sukurti savo skelbimus, pateikti komentarus skelbimams ir įvertinti vartotojų patikimumą. Administratorius galės pašalinti skelbimus, komentarus ir vartotojus.Administratorius dar galės sukurti ir pašalinti skelbimų kategorijas. Svetainės skelbimai bus suskirtstyti į kategorijas. Kiekvienas skelbimas turės komentarus.


## Funkciniai reikalavimai

Neprisijungęs vartotojas galės:
  1. Prisiregistruoti ar prisijungti prie paskyros
  2. Peržiūrėti visus skelbimus.
  3. Peržiūrėti skelbimą detaliau.
  4. Peržiūrėti skelbimo komentarus.
  5. Peržiūrėti vartotojo duomenys.

Prisijungęs vartotojas galės:
  1. Atsijungti nuo paskyros.
  2. Peržiūrėti visus skelbimus.
  3. Peržiūrėti skelbimą detaliau.
  4. Peržiūrėti skelbimo komentarus.
  5. Peržiūrėti vartotojo duomenys.
  6. Sukurti, redaguoti ir pašalinti savo skelbimus.
  7. Sukurti, redaguoti ir pašalinti savo komentarus.
  8. Įvertinti skelbimus, pakeisti ir pašalinti savo įvertinimus.
  9. Redaguoti ir pašalinti savo paskyrą.

Administratorius galės:
  1. Šalinti skelbimus.
  2. Šalinti komentarus.
  3. Šalinti paskyras.
  4. Sukurti ir pašalinti kategorijas

## Sistemos architektūra
![deployment](https://github.com/Faustels/Saitynai/assets/73067153/50bcc6ae-5db2-4366-b05f-e7e87aa572f7)


## Projekto API užklausos
|Užklausa|Aprašymas|
| --- | --- |
| GET users | Grąžina visus vartotojus |
| POST users | Sukuria vartotoją |
| GET users/{id} | Grąžina vartotojo duomenis |
| PUT users/{id} | Pakeičia visus vartotojo duomenis |
| PATCH users/{id} | Pakeičia parinktus vartotojo duomenis |
| DELETE users/{id} | Ištrina vartotoją |
| GET tags | Grąžina visas kategorijas |
| POST tags | Sukuria kategoriją |
| DELETE tags | Pašalina kategoriją |
| GET adverts | Grąžina visus skelbimus |
| GET tags/{tag}/adverts | Grąžina visus skelbimus tarp kategorijos |
| POST adverts | Sukuria skelbimą |
| GET adverts/{id} | Grąžina skelbimo duomenis |
| PUT adverts/{id} | Pakeičia skelbimo duomenis |
| PATCH adverts/{id} | Pakeičia parinktus skelbimo duomenis |
| DELETE adverts/{id} | Pašalina skelbimą |
| GET comments | Grąžina visus komentarus |
| GET tags/{tag}/comments | Grąžina visus kategorijos komentarus |
| GET adverts/{id}/comments | Grąžina skelbimo komentarus |
| POST adverts/{id}/comments | Sukurią skelbimui komentarą |
| GET comments/{id} | Grąžina komentarą |
| PUT comments/{id} | Pakeičia komentaro tekstą |
| DELETE comments/{id} | Pašalina komentarą |
| GET adverts/{id}/ratings/list | Grąžina visus skelbimo įvertinimus |
| GET adverts/{id}/ratings | Grąžina susumuota skelbimo įvertinimą ir vartotojo duotą įvertinimą skelbimui |
| POST adverts/{id}/ratings | Sukuria įvertinimą |
| GET ratings/{id} | Grąžina įvertinimą |
| PUT adverts/{id}/ratings | Pakeičia įvertinimą |
| DELETE adverts/{id}/ratings | Pašalina įvertinimą |
| POST token | Grąžina JWT refresh ir access token |
| POST token/refresh | Grąžina JWT access token | 

## Išvados 
Dirbant su šiuo projektu man pavyko realizuoti REST principais veikiančia API sąsaja ir sukurti naudotojo sąsaja realizuotam API.
