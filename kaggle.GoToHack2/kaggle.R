rm(list=ls())
#################################################################################################################
# Загрузка данных и описание их
#################################################################################################################
# Загружаем нужные библиотеки и ставим локацию файлов
library(data.table)
library(class)
library(ggplot2)
files_location <- '~/R/GoToHack2/kaggle/'

# В файле user_activity.csv даны полные логи за первые 2 недели у некоторых пользователей курса. 
user_activity <- fread(paste(files_location, 'user_activity.csv', sep = ''), header = T)
# В файле targets.csv - ответы: прошёл ли очередной пользователь свой курс. 
targets <- fread(paste(files_location, 'targets.csv', sep = ''), header = T)
# Структура курса
structure <- fread(paste(files_location, 'structure.csv', sep = ''), header = T)
# В файле user_activity_test.csv содержатся логи для пользователей, ответы про которых неизвестны. 
user_activity_test <- fread(paste(files_location, 'user_activity_test.csv', sep = ''), header = T)
# Для всех id пользователей ones_only.csv программа выдаст вердикт -- закончит он курс или нет.
# We expect the solution file to have 4,255 predictions.
ones_only <- fread(paste(files_location, 'ones_only.csv', sep = ''), header = T)

# Добавляем переменную - позицию степа
step_pos <- structure[, .(step_pos = module_position * 1000 + lesson_position * 100 + step_position), by = step_id]
setkey(user_activity, step_id)
setkey(user_activity_test, step_id)
setkey(step_pos, step_id)
user_activity <- merge(user_activity, step_pos, by = "step_id")
user_activity_test <- merge(user_activity_test, step_pos, by = "step_id")
#################################################################################################################
# Обработка известных данных в предикторы 
#################################################################################################################
was_before <- function(steps) {
  # Rаждое значение TRUE, если пользователь возвращался к степу, иначе FALSE
  ans <- vector()
  # Будем идти только по уникальным степам
  unique_steps <- unique(steps)
  for (j in 1:length(unique_steps)) {
    # Альтернативный айди текущего степа
    current_step <- unique_steps[j]
    # Альтернативный айди следующего степа
    next_step <- unique_steps[which(unique_steps == current_step) + 1]
    # Если этот степ встреяается более одного раза в списке просмотренных, то ищем первый и последний точки вхождения
    if (sum(current_step == steps) > 1) {
      first_in <- min(which(current_step == steps))
      last_in <- max(which(current_step == steps))
      ans[j] <- next_step %in% steps[first_in:last_in]
    } else {
      ans[j] <- F
    }
    return(sum(ans))
  }
}

preprocessing <- function(data, users) {
  # Кол-во полученных баллов за 2 недели
  two_week_score <- data[action == 'passed', .(two_week_score = sum(step_cost)), by = user_id]
  # Среднее время выполнения задания
  mean_decision_time <- data[action %in% c('discovered', 'passed') & step_cost > 0]
  mean_decision_time <- mean_decision_time[, .(decision_time = max(time) - min(time)), by = .(user_id, step_id)][decision_time > 0]
  mean_decision_time <- mean_decision_time[, .(mean_decision_time = mean(decision_time)), by = user_id]
  # Количество просмотренных степов
  discovered_steps <- data[action == 'discovered', .(discovered_steps = length(step_id)), by = user_id]
  # Количество решенных задач на программирование
  passed_code_tasks <- data[action == 'passed' & step_type == 'code', .(passed_code_tasks = length(step_id)), by = user_id]
  # Сложность степов. Величина, котора больше если юзер решил степы, которые решили мало людей
  users_number <- length(unique(data$user_id))
  step_hardless <- data[action == 'passed' & step_cost > 0, .(step_hardless = users_number/length(user_id)), by = step_id]
  setkey(step_hardless, step_id)
  data <- merge(data, step_hardless, by = 'step_id', all = T)
  step_hardless <- data[, .(step_hardless = sum(step_hardless, na.rm = T)), by = user_id]
  # Количество возвратов к предыдущим степам
  returns <- data[order(user_id, time), .(step_pos = unique(step_pos)), by = .(user_id, step_id, time)]
  returns <- returns[filter(step_pos, c(-1,1)) != 0]
  returns <- returns[, .(returns = was_before(step_pos)), by = user_id]
  # Делаем один дататейбл со всеми предикторами
  setkey(users, user_id)
  setkey(two_week_score, user_id)
  setkey(mean_decision_time, user_id)
  setkey(discovered_steps, user_id)
  setkey(passed_code_tasks, user_id)
  setkey(step_hardless, user_id)
  setkey(returns, user_id)
  data <- merge(users, two_week_score, by = 'user_id', all = T)
  data <- merge(data, mean_decision_time, by = 'user_id', all = T)
  data <- merge(data, discovered_steps, by = 'user_id', all = T)
  data <- merge(data, passed_code_tasks, by = 'user_id', all = T)
  data <- merge(data, step_hardless, by = 'user_id', all = T)
  data <- merge(data, returns, by = 'user_id', all = T)
  
  # Ставим нули, где данные о юзере неизвестны
  data[is.na(data)] <- 0
  return(data)
}

#################################################################################################################
# Предсказание 
#################################################################################################################
# Создаем данные вообще со всеми юзерами, на случай если не все данные о исследуемых в user_activity_test
train_data <- preprocessing(user_activity, targets[, .(user_id, passed)])
test_data <- preprocessing(user_activity_test, ones_only)

# Создаем модель, а потом смотрик какие переменные влияют на результат
# К моему удивлению влияние количества набранных баллов статистически недостоверно 
fit <- glm(passed ~ ., train_data[, c(2, 4, 5, 6, 7, 8), with = F], family = 'binomial')
predicted <- predict(fit, newdata = test_data[, c(4, 5, 6, 7, 8), with = F], type = "response")

# Я выбрал вероятность > 0,2 т.к. при таком параметре процент тех, кто вероятно закончит курс равен ~ 3,7 %, у исходных данных - 3,9 %
ones_only$passed <- as.numeric(predicted > 0.2)

write.csv(ones_only, file = 'prediction.csv', row.names = F)
