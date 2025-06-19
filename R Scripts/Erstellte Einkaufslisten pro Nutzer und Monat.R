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
  SELECT useruser_id, timestamp
  FROM shoppinglist
")

dbDisconnect(con)

daten$timestamp <- as.Date(daten$timestamp)
daten$monat <- floor_date(daten$timestamp, "month")
daten <- subset(daten, monat >= as.Date("2024-08-01") & monat <= as.Date("2025-05-31"))

summary <- aggregate(timestamp ~ monat + useruser_id, data = daten, FUN = length)
colnames(summary) <- c("monat", "nutzer_id", "anzahl")

ggplot(summary, aes(x = monat, y = anzahl, color = as.factor(nutzer_id))) +
  geom_line(size = 0.75) +
  geom_point(size = 1) +
  scale_x_date(date_breaks = "1 month", date_labels = "%b %Y") +
  scale_y_continuous(breaks = 0:ceiling(max(summary$anzahl))) +
  labs(title = "Erstellte Einkaufslisten pro Nutzer und Monat",
       x = "Monat", y = "Anzahl Einkaufslisten", color = "Nutzer-ID") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold", hjust = 0.5))