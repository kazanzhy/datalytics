rm(list=ls())

library(data.table)


events <- fread('~/R/GoToHack2/course-217-events.csv', header = T)
structure <- fread('~/R/GoToHack2/course-217-structure.csv', header = T)

# Соединяем две таблицы по step_id
setkey(events, step_id)
setkey(structure, step_id)
data <- merge(events, structure, by = "step_id")

# Записываем начало прохождения курса
data <- data[, .(user_id, step_id, action, step_cost, time, start = min(time)), by = user_id]

# Выбираем нужные переменные и только те степы, за которые начисляются баллы и только тех юзеров, которые сдали степ
data <- data[step_cost > 0 & action == 'passed', .(user_id, start, step_id, action, step_cost, time)]

# Взвращает вектор с текущим количеством баллов
get_points <- function(x) {
  p <- vector()
  for (i in 1:length(x)) {
    p[i] <- sum(x[1:i])
  }
  return(p)
}
# Сортируем по юзерам и по времени прохождения степов
data <- data[order(user_id, time)]
# Добавляем переменную с текущим количеством баллов каждого юзера
data <- data[, .(user_id, start, step_id, step_cost, time, current_points = get_points(step_cost)), by  = user_id]

# Смотрим в какой момент юзер получил 24 балл и высчитываем длительность прохождения курса
d <- data[current_points == 24, .(user_id, start, time, duration = (time - start))]

paste(head(d[order(duration)], 10)$user_id, collapse = ',')















