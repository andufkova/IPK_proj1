# IPK 2018/2019 - projekt 1
## Varianta 2: Klient pro OpenWeatherMap API
Aneta Dufková (xdufko02)

### Popis řešeného problému
Úkolem projektu bylo vytvořit program \- klienta rozhraní OpenWeatherMap, který získává vybrané informace prostřednictvím HTTP dotazů. Pro implementaci jsem si vybrala jazyk Python.

### Využité zdroje informací
1. Informace o HTTP protokolu: https://tools.ietf.org/html/rfc7231
2. Dokumentace k API OpenWeatherMap: https://openweathermap.org/curren a https://openweathermap.org/weather-data
3. Dokumentace k Python 3: https://docs.python.org/3/library/socket.html

### Návrh řešení
Cílem bylo vytvoření lightweight klienta, proto jsem se omezila na použití knihoven `socket`, `sys` a `json`.

Prvním bodem je správná práce s knihovnou soketů. Využila jsem konstrukci `try - except` pro lepší odhalování chyb při komunikaci se serverem. Nejtěžší částí bylo sestavit správný dotaz a uvědomit si, že kvůli převodu str - bytes je zapotřebí použít funkci `encode()`.

    request = 'GET /data/2.5/weather?q=' + city + '&APPID=' + api_key + '&units=metric HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n'

Druhou částí je získání potřebných dat z odpovědi serveru. Nejdříve se musí ověřit návratový kód. Rozlišuji _200 - OK_, _4xx - klient error_, _5xx - server error_, _401 - chybný API klíč_, _404 - chybný název města_ (tyto dvě varianty řeším zvlášť, neboť budou při používání asi nejčastější) a _ostatní chyby_.
Ke zpracování obdržených dat pomohla knihovna `json`, díky ní stačilo dohledat si ve slovnících podle klíče správné hodnoty. Směr větru jsem ošetřila, protože pokud je téměř bezvětří, žádný směr se neposílá.

Ve třetí části jsem vytvořila makefile a zařídila správné zpracování argumentů. Kvůli víceslovným názvům města je v Makefile potřeba uzavřít `'$(city)'` do uvozovek. Výpisy (tzv. echoing) jsem v Makefile zrušila pomocí \@. 

### Instalace a překlad aplikace
Aplikaci není třeba instalovat ani překládat. Stačí si stáhnout dva potřebné soubory: `proj1.py` a `Makefile`.

### Spouštění aplikace
Příklad spuštění aplikace:

    make run api_key=00000000000000000000000000000000 city=’Nove Mesto na Morave’
    

_API klíč je možné získat zdarma po registraci na https://home.openweathermap.org/users/sign_up\_

### Rozšíření
Pro více informací o počasí je možné aplikaci spustit s volitelným argumentem:

    make run api_key=00000000000000000000000000000000 city=’Nove Mesto na Morave’ additional_info=yes
