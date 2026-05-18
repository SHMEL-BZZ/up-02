from model.fishing_model import FishLake

def find_optimal_q(N, M, K, prepro, pdeath, steps_warmup, steps_eval, trials):
    """
    Перебирает заданные значения q, для каждого проводит несколько
    независимых прогонв и вычисляет средний улов.
    
    Возвращает словарь {q: (средний_улов, средняя_численность)} и значение q_opt,
    при котором средний улов максимален, а популяция не вымирает (средняя численность > 0).
    
    Параметры:
        q_values — список проверяемых q 
        steps_warmup — число шагов для стабилизации
        steps_eval — число шагов для оценки среднего улова
        trials — число повторных прогонов для усреднения 
    """
    # спизок значений q от 0 до 1 с шагом 0.05
    q_values = [i/20 for i in range(21)]
    
    results = {}
    for q in q_values:
        total_catch = 0.0
        total_pop = 0.0
        for _ in range(trials):
            lake = FishLake(N, M, K, prepro, pdeath, q)
            # Период стабилизации
            for _ in range(steps_warmup):
                lake.step()
            # Оценочный период
            catch_sum = 0
            pop_sum = 0
            for _ in range(steps_eval):
                catch_sum += lake.step()
                pop_sum += lake.population
            total_catch += catch_sum / steps_eval
            total_pop += pop_sum / steps_eval
        
        avg_catch = total_catch / trials
        avg_pop = total_pop / trials
        results[q] = (avg_catch, avg_pop)
    
    # Выбор оптимального q: максимум среднего улова, популяция > 0
    valid_q = [(q, res[0]) for q, res in results.items() if res[1] > 0]
    if not valid_q:
        q_opt = None  # популяция вымирает при всех q
    else:
        q_opt = max(valid_q, key=lambda x: x[1])[0]
    
    return results, q_opt

