rm(list=ls())

library(data.table)

events <- fread('~/R/GoToHack2/course-217-events.csv', header = T)
structure <- fread('~/R/GoToHack2/course-217-structure.csv', header = T)

# Соединяем две таблицы по step_id
setkey(events, step_id)
setkey(structure, step_id)
data <- merge(structure, events, by = "step_id")

# Сортируем массив по пользователю и времени просмотра степов 
# Добавляем переменную step_altid (альтернативный айди) который равен module_position * 1000 + lesson_position * 100 + step_position
# Это сделано так, ибо max(structure$module_position)=10, max(structure$lesson_position)=9, а max(structure$step_position) 13
data <- data[order(user_id, time), .(user_id, step_id, time, step_altid = module_position * 1000 + lesson_position * 100 + step_position)]

# Удаляем записи у которых одинаковый юзер, степ и время
# То есть случаи когда одновременно делаются записи discovered, viewed, passed 
data <- data[, .(step_altid = unique(step_altid)), by = .(user_id, step_id, time)]

# Удаляем одинаковые степы идущие последовательно через некоторое время
data <- data[filter(step_altid, c(-1,1)) != 0]


was_before <- function(steps){
  # Получает на вход вектор steps, который является вектором step_altid для каждого пользователя 
  # Возвращает вектор по длине равный длине уникальных степов для данного пользователя
  ans <- vector()
  # Rаждое значение TRUE, если пользователь возвращался к степу, иначе FALSE
  # Будем идти только по уникальным степам
  unique_steps <- unique(steps)
  for (j in 1:length(unique_steps)) {
    # Альтернативный айди текущего степа
    current_step <- unique_steps[j]
    # Альтернативный айди следующего степа
    next_step <- steps_list[which(steps_list == current_step) + 1]
    # Если этот степ встреяается более одного раза в списке просмотренных, то ищем первый и последний точки вхождения
    if (sum(current_step == steps) > 1) {
      first_in <- min(which(current_step == steps))
      last_in <- max(which(current_step == steps))
      ans[j] <- next_step %in% steps[first_in:last_in]
    } else {
      ans[j] <- F
    }
  }
  return(ans)
}

# Добавляем переменную before где TRUE, если пользователь возвращался к степу, иначе FALSE
steps_list <- sort(unique(data$step_altid))
data <- data[, .(step_id = unique(step_id), step_altid = unique(step_altid), before = was_before(step_altid)), by = user_id]

# Считаем для каждого степа отношение: (сколько раз к нему возвращались) / (сколько человек его просмотрело)
data <- data[, .(before = sum(before), user_count = length(unique(user_id))), by = .(step_id)]
data <- data[, .(step_id, before, user_count, stat = round(before * 100 / user_count, digits = 2))]

# Выводим результат
paste(head(data[order(stat, decreasing = T)]$step_id, 10), collapse = ',')


