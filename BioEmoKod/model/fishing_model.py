"""
Модель популяции рыбы с учётом вылова.
Вариант 5. Динамика рыбного промысла.
"""

import numpy as np
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class SimulationResult:
    """Результат одного прогона симуляции."""
    population: List[int]    # численность по годам
    catches: List[int]       # улов по годам
    extinct: bool            # произошло ли вымирание
    extinct_year: int        # год вымирания (если произошло)
    avg_catch: float         # средний годовой улов


def simulate_single(
    N0: int = 500,
    K: int = 1000,
    r: float = 0.6,
    p_death: float = 0.1,
    strategy: str = 'proportional',
    catch_param: float = 0.0,
    years: int = 200,
    seed: Optional[int] = None
) -> SimulationResult:
    """
    Один прогон модели популяции рыбы.

    Параметры:
        N0: начальная численность
        K: ёмкость среды
        r: максимальная скорость воспроизводства
        p_death: вероятность естественной гибели
        strategy: 'proportional' (вероятность q) или 'quota' (фиксированная квота H)
        catch_param: параметр вылова (q или H)
        years: период моделирования
        seed: зерно для воспроизводимости

    Возвращает:
        SimulationResult с историей популяции, уловами и статусом
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    N = N0
    population = [N]
    catches = []
    extinct = False
    extinct_year = years

    for year in range(years):
        # --- 1. Нерест ---
        if N > 0:
            p_birth = max(0.0, r * (1.0 - N / K))
            newborns = np.random.binomial(N, p_birth)
        else:
            newborns = 0

        N += newborns

        # --- 2. Естественная гибель ---
        if N > 0:
            deaths = np.random.binomial(N, p_death)
            N = max(0, N - deaths)
        else:
            deaths = 0

        # --- 3. Промысловый вылов ---
        if N > 0:
            if strategy == 'proportional':
                q = catch_param
                caught = np.random.binomial(N, q)
            elif strategy == 'quota':
                H = int(catch_param)
                caught = min(N, H)
            else:
                raise ValueError(f"Неизвестная стратегия: {strategy}")
        else:
            caught = 0

        N = max(0, N - caught)
        population.append(N)
        catches.append(caught)

        # Проверка вымирания
        if N == 0 and not extinct:
            extinct = True
            extinct_year = year + 1
            # Заполняем оставшиеся годы нулями
            for _ in range(years - year - 1):
                population.append(0)
                catches.append(0)
            break

    # Средний годовой улов (за фактическое время существования)
    active_years = extinct_year if extinct else years
    avg_catch = sum(catches) / active_years if active_years > 0 else 0.0

    return SimulationResult(
        population=population,
        catches=catches,
        extinct=extinct,
        extinct_year=extinct_year,
        avg_catch=avg_catch
    )


def simulate_multiple(
    N0: int = 500,
    K: int = 1000,
    r: float = 0.6,
    p_death: float = 0.1,
    strategy: str = 'proportional',
    catch_param: float = 0.0,
    years: int = 200,
    num_runs: int = 10
) -> dict:
    """
    Многократный прогон модели с усреднением результатов.

    Возвращает словарь:
        avg_population: средняя численность по годам
        avg_catches: средний улов по годам
        overall_avg_catch: общий средний годовой улов
        extinction_rate: доля прогонов с вымиранием
        all_runs: список всех SimulationResult
    """
    all_results = []
    total_catch_sum = 0.0
    extinction_count = 0

    # Для усреднения динамики
    max_len = years + 1  # включая начальный год
    pop_sum = np.zeros(max_len)
    catch_sum = np.zeros(years)

    for run_id in range(num_runs):
        seed = hash(f"{strategy}_{catch_param}_{run_id}") % (2**31)
        result = simulate_single(
            N0=N0, K=K, r=r, p_death=p_death,
            strategy=strategy, catch_param=catch_param,
            years=years, seed=seed
        )
        all_results.append(result)
        total_catch_sum += result.avg_catch

        if result.extinct:
            extinction_count += 1

        # Накапливаем для среднего
        for i, val in enumerate(result.population):
            if i < max_len:
                pop_sum[i] += val
        for i, val in enumerate(result.catches):
            if i < years:
                catch_sum[i] += val

    return {
        'avg_population': (pop_sum / num_runs).tolist(),
        'avg_catches': (catch_sum / num_runs).tolist(),
        'overall_avg_catch': total_catch_sum / num_runs,
        'extinction_rate': extinction_count / num_runs,
        'all_runs': all_results
    }


def find_optimal_parameter(
    N0: int = 500,
    K: int = 1000,
    r: float = 0.6,
    p_death: float = 0.1,
    strategy: str = 'proportional',
    param_range: List[float] = None,
    years: int = 200,
    num_runs: int = 10
) -> dict:
    """
    Поиск оптимального параметра вылова (максимальный улов без вымирания).

    Возвращает:
        optimal_param: оптимальное значение q или H
        max_sustainable_catch: максимальный устойчивый улов
        all_params: список исследованных параметров
        all_catches: список средних уловов для каждого параметра
        all_extinction_rates: список долей вымираний
    """
    if param_range is None:
        if strategy == 'proportional':
            param_range = np.arange(0.0, 1.01, 0.05)
        else:
            param_range = np.arange(0, 505, 5)

    all_params = []
    all_catches = []
    all_extinction_rates = []

    best_param = None
    best_catch = 0.0

    for param in param_range:
        result = simulate_multiple(
            N0=N0, K=K, r=r, p_death=p_death,
            strategy=strategy, catch_param=float(param),
            years=years, num_runs=num_runs
        )

        all_params.append(float(param))
        all_catches.append(result['overall_avg_catch'])
        all_extinction_rates.append(result['extinction_rate'])

        # Оптимальный — максимальный улов при нулевом вымирании
        if result['extinction_rate'] == 0.0 and result['overall_avg_catch'] > best_catch:
            best_catch = result['overall_avg_catch']
            best_param = float(param)

    return {
        'optimal_param': best_param,
        'max_sustainable_catch': best_catch,
        'all_params': all_params,
        'all_catches': all_catches,
        'all_extinction_rates': all_extinction_rates
    }


# ---------- Демо-запуск ----------
if __name__ == '__main__':
    print("=== Поиск оптимального вылова (пропорциональная стратегия) ===")
    prop_result = find_optimal_parameter(
        strategy='proportional',
        param_range=np.arange(0.0, 0.51, 0.05),
        num_runs=10
    )
    print(f"Оптимальный q: {prop_result['optimal_param']:.2f}")
    print(f"Максимальный устойчивый улов: {prop_result['max_sustainable_catch']:.1f} рыб/год")

    print("\n=== Поиск оптимального вылова (стратегия квоты) ===")
    quota_result = find_optimal_parameter(
        strategy='quota',
        param_range=np.arange(0, 205, 5),
        num_runs=10
    )
    print(f"Оптимальная H: {quota_result['optimal_param']:.0f}")
    print(f"Максимальный устойчивый улов: {quota_result['max_sustainable_catch']:.1f} рыб/год")
