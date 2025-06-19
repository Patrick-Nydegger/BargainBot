library(DBI)
library(RMariaDB)
library(ggplot2)
library(lubridate)

con <- dbConnect(RMariaDB::MariaDB(),
                 user = "BargainBot",
                 password = "%BargainBot",
                 dbname = "manuel projekt v4",
                 host = "localhost")

daten <- dbGetQuery(con, "
  SELECT s.timestamp, c.categoryname, ps.amount
  FROM shoppinglist s
  JOIN product_shoppinglist ps ON s.shoppinglist_id = ps.shoppinglistshoppinglist_id
  JOIN product p ON ps.productproduct_id = p.product_id
  JOIN productcategory c ON p.productcategoryproductcategory_id = c.productcategory_id
")

dbDisconnect(con)

daten$monat <- floor_date(as.Date(daten$timestamp), unit = "month")
daten <- subset(daten, monat >= as.Date("2024-08-01") & monat <= as.Date("2025-05-31"))

summary <- aggregate(amount ~ monat + categoryname, data = daten, FUN = sum)

ggplot(summary, aes(x = monat, y = amount, color = categoryname)) +
  geom_line(size = 0.75) +
  geom_point(size = 1) +
  scale_x_date(date_breaks = "month", date_labels = "%b %Y") +
  labs(title = "Produktmenge pro Monat und Kategorie",
       x = "Monat", y = "Eingekaufte Menge", color = "Kategorie") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45),
        plot.title = element_text(face = "bold", hjust = 0.5))