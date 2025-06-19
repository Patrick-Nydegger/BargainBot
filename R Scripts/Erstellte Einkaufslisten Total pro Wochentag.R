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

daten$wochentag <- wday(as.Date(daten$timestamp), label = TRUE, abbr = FALSE, week_start = 1)
daten <- subset(daten, as.Date(timestamp) >= as.Date("2024-08-01"))

summary <- aggregate(timestamp ~ wochentag, data = daten, FUN = length)
colnames(summary) <- c("wochentag", "anzahl_einkaeufe")

ggplot(summary, aes(x = wochentag, y = anzahl_einkaeufe)) +
  geom_col(fill = "steelblue") +
  geom_text(aes(label = anzahl_einkaeufe), vjust = -0.3, size = 3) +
  labs(title = "Erstellte Einkaufslisten nach Wochentag",
       x = "Wochentag", y = "Anzahl Einkaufslisten") +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", hjust = 0.5))