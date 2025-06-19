library(DBI)
library(RMariaDB)

con <- dbConnect(RMariaDB::MariaDB(),
                 user = "BargainBot",
                 password = "%BargainBot",
                 dbname = "manuel projekt v4",
                 host = "localhost")

daten <- dbGetQuery(con, "
  SELECT s.name AS filiale, sp.price AS preis
  FROM store_product sp
  JOIN store s ON sp.storestore_id = s.store_id
")

dbDisconnect(con)

boxplot(preis ~ filiale, data = daten,
        col = "cadetblue",
        main = "Preisverteilung pro Laden",
        xlab = "Laden",
        ylab = "Preis (CHF)",
        las = 1)