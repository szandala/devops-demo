# Specjalistyczne Platformy Programistyczne - Demo repo

## Setup
Laboratorium dotyczy utworzenia prostych usług:
- frontend w React'ie
- backend we Flasku
- baza danych MongoDB


## Pełny projekt
Pełny projekt jest dość rozbudowany, ale idąc po kolei...

### Prerekwizyty:
- zbudować obrazy `backend` i `frontend`
- Zpushować je na [DockerHub](https://hub.docker.com/) jako obrazy publiczne

UWAGA: `frontend` jest uruchaminy w wersji debuggowej - zmienna `REACT_APP_BACKEND_URL` jest wtedy czytany ze środowiska - jakbyśmy chcieli poprawnie ją obsłużyć to powinna być podana jako BUILD_ARG i "wkompilowana" w aplikację. To jest notka na przyszłość.

**Wszystkie zasoby powinny być w namespace: `student-<nr_albumu>`.**

### 3.0:
Napisać manifesty, które tworzą namespace `student-<nr_albumu>` a w nim:
- Deployment (2+ repliki), który uruchomi `backend`
- Deployment (2+ repliki), który uruchomi `frontend`
- ClusterIP serwis, który będzie przed deploymentem `backend`
- StatefullSet (1 replika), która uruchomi `mongodb`
- Headless serwis, który będzie przed StatefullSetem z `mongodb`

Zmienne:
- `backend`:
    - `MONGODB_HOST` - adres headless serwisu, który prowadzi na SS mongodb
- `mongodb`:
    - `MONGO_INITDB_ROOT_PASSWORD` - ustaw na `example`

**UWAGA:**\
Nie ma dostępu do aplikacji z zewnatrz (spoza klastra).

### 3.5:
Zmienne pobierane są z `ConfigMapy`.\
Zmienne *poufne*, jak hasła i nazwy użytkowników, pobierane są z `Secreta`.
Deployment `backend` ma skofigurowany healthchecki. Proby - `Startup`, sprawdzajacy od 15 sekundy, oraz `Readiness` który co 10 sekund pyta `curl http://backend:5000/up`

### 4.0:
StatefullSet `mongodb` ma 3 repliki:
- 1 read-write
- 2x read-only

RW jest wskazywana przez serwis Headless, którego URL jest zapisany w zmiennej `MONGODB_RW_HOST`.\
RO i RW (bez Helma trudno tylko RO zrobić) są wskazywane przez inny serwis Headless, którego URL jest zapisany w zmiennej `MONGODB_RO_HOST`.\
Zmienne zastepują `MONGODB_HOST`.

### 4.5:
Mongo korzysta z persistent Volume'ów (wykorzystaj `persistentVolumeClaimTemplate`).

### 5.0:
Mamy Job, który co 2 godziny, począwszy od 1:30, (czyli 1:30, 3:30, 5:30,...), od poniedziałku do piątku wykonuje backup na bazy danych mongo. Backup ma być na kolejny persistentVolume, tym razem bez claim template.

### 5.5:
Zrobienie z tego tzw. *charta Helm'owego*, który w `values.yml`:
- definiuje obrazy
- może opcjonalnie korzystać z `imagePullSecrets`
- definiuje ilość poszczególnych replik.
- definiuje rozmiary
- pozwala podawać wszystkie zmienne, które są potrzebne. Ale np. `MONGODB_RO_HOST` jest automatycznie definiowany
- pozwala redefniować parametry czasowe Probe'ów
- pozwala dodać opcjonalny `Ingress`*

*`Ingress` wymaga `IngressControllera` - oddzielne zadanie, zależne od Kubernetesa, którego mamy (docker-desktop, kind, etc.)

**Helm trzeba obronić 10 czerwca 2024 na zajęciach.**
