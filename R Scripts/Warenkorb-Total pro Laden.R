library(DBI)
library(RMariaDB)

con <- dbConnect(RMariaDB::MariaDB(),
                 user = "BargainBot",
                 password = "%BargainBot",
                 dbname = "manuel projekt v4",
                 host = "localhost")

warenkorb <- dbGetQuery(con, "
  SELECT 
    s.name AS store,
    p.productname,
    sp.price
  FROM store_product sp
  JOIN store s ON sp.storestore_id = s.store_id
  JOIN product p ON sp.productproduct_id = p.product_id
")

dbDisconnect(con)

gesamtpreise <- aggregate(price ~ store, data = warenkorb, sum)
gesamtpreise <- gesamtpreise[order(gesamtpreise$price), ]

balken <- barplot(gesamtpreise$price,
                  names.arg = gesamtpreise$store,
                  col = "darkorange",
                  main = "Preisvergleich: Total Einkaufsliste pro Laden",
                  ylab = "Gesamtkosten in CHF",
                  las = 1)