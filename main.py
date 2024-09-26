import random
import timeit
import sys
import copy

# Збільшення лімітів рекурсії для великих списків (для сортування злиттям)
sys.setrecursionlimit(1000000)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        # Об'єднання двох половин
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Переносимо залишки L
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Переносимо залишки R
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Переміщення елементів, які більші за ключ, на одну позицію вправо
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def timsort_builtin(arr):
    return sorted(arr)

def timsort_inplace(arr):
    arr.sort()

def generate_datasets(size):
    datasets = {
        'Random': random.sample(range(size * 10), size),
        'Sorted': list(range(size)),
        'Reverse Sorted': list(range(size, 0, -1)),
        'Duplicates': [random.choice(range(size // 10)) for _ in range(size)],
        'Nearly Sorted': list(range(size))
    }
    # Додавання невеликої кількості змін до Nearly Sorted
    for _ in range(size // 100):
        idx1 = random.randint(0, size - 1)
        idx2 = random.randint(0, size - 1)
        datasets['Nearly Sorted'][idx1], datasets['Nearly Sorted'][idx2] = datasets['Nearly Sorted'][idx2], datasets['Nearly Sorted'][idx1]
    return datasets

def measure_time(sort_func, data):
    # Використовуємо копію даних, щоб сортування не впливало на оригінал
    data_copy = copy.deepcopy(data)
    timer = timeit.Timer(lambda: sort_func(data_copy))
    # Виконуємо сортування один раз
    try:
        execution_time = timer.timeit(number=1)
    except RecursionError:
        execution_time = float('inf')
    return execution_time

def main():
    sizes = [1000, 5000, 10000]  # Розміри списків
    algorithms = {
        'Merge Sort': merge_sort,
        'Insertion Sort': insertion_sort,
        'Timsort (sorted)': timsort_builtin,
        'Timsort (list.sort())': timsort_inplace
    }

    for size in sizes:
        print(f"\n--- Розмір списку: {size} ---")
        datasets = generate_datasets(size)
        for dataset_name, data in datasets.items():
            print(f"\nНабір даних: {dataset_name}")
            results = {}
            for algo_name, algo_func in algorithms.items():
                # Для Timsort (sorted) створюємо нову копію для функції sorted
                if algo_name == 'Timsort (sorted)':
                    sort_func = lambda x: sorted(x)
                elif algo_name == 'Timsort (list.sort())':
                    sort_func = lambda x: x.sort()
                else:
                    sort_func = algo_func

                time_taken = measure_time(sort_func, data)
                results[algo_name] = time_taken

            # Вивід результатів
            print(f"{'Алгоритм':<25}{'Час (сек)':>15}")
            for algo, t in results.items():
                print(f"{algo:<25}{t:>15.6f}")
    
    print("\n--- Порівняння завершено ---")

if __name__ == "__main__":
    main()