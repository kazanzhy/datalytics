rm(list=ls())


library(data.table)


events <- fread('~/R/GoToHack2/course-217-events.csv', header = T)
structure <- fread('~/R/GoToHack2/course-217-structure.csv', header = T)


# Соединяем две таблицы по step_id
setkey(events, step_id)
setkey(structure, step_id)
data <- merge(events, structure, by = "step_id")


# Сортируем массив по пользователю и времени просмотра степов 
# Выбираем только записи просмотра степов(viewed) и 
# Добавляем переменную step_altid (альтернативный айди)
#max(structure$module_position)
#max(structure$lesson_position)
#max(structure$step_position)
data <- data[, .(user_id, step_id, time, step_altid = module_position * 1000 + lesson_position * 100 + step_position)]


# Это даст возможность просмотреть структуру данных и очереднесть просмотра степов
# Например для 1 пользователя наблюдаем очередность просмотра степов: 1101 1102 1104 1103 1104 ... 1113
data <- data[order(user_id, time), .(step_altid = unique(step_altid)), by = .(user_id, step_id, time)]



# Получает на вход вектор с значениями переменной step и 
# возвращает вектор такой же длины, где каждое значение TRUE если step раньше встречался и FALSE - если впервые
was_before <- function(vec){
  ans <- vector()
  sorted <- unique(sort(vec))
  for (j in 1:length(vec)) {
    # Альтернативный айди текущего степа
    current_step <- vec[j]
    # Альтернативный айди следующего степа
    next_step <- sorted[which(sorted == vec[j]) + 1]
    # Альтернативные айди степов, которые просмотрел юзер, перед просмотром данного
    prev_steps <- vec[1:(j-1)]
    # Проверяем есть ли в срезе вектора альтернативных айди, текущий и следующий
    if ((current_step %in% prev_steps) & (next_step %in% prev_steps)) {
      ans[j] <- max(which(next_step == prev_steps)) > min(which(current_step == prev_steps))
    } else {
      ans[j] <- F
    }
  }
  return(ans)
}

# Добавляем переменную before где TRUE, если step раньше встречался и FALSE - если впервые
data <- data[, .(step_id, time, step_altid, before = was_before(step_altid)), by = user_id]


# Убираем повторяющиеся степы, то есть в каждой записи уникальные юзер и степ
d <- data[, .(before = any(before)), by = .(user_id, step_id)]


# Считаем для каждого степа отношение: (сколько раз к нему возвращались) / (сколько человек его просмотрело)
d <- d[, .(before = sum(before), user_count = length(user_id)), by = .(step_id)]
d <- d[, .(step_id, before, user_count, stat = round(before * 100 / user_count, digits = 2))]

paste(head(d[order(stat, decreasing = T)]$step_id, 10), collapse = ',')

# 41684, 41604, 41097, 41481, 42593, 38872, 41686, 39735, 39740, 39717









