import random
import math

# Tạo ngẫu nhiên N thành phố trên mặt phẳng 2D
def generate_cities(n, seed=42):
    random.seed(seed)
    cities = []
    for _ in range(n):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        cities.append((x, y))
    return cities

# Tính khoảng cách Euclid giữa 2 thành phố
def distance(c1, c2):
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

# Độ dài tổng hành trình (vòng khép kín)
def tour_length(tour, cities):
    total = 0.0
    n = len(tour)
    for i in range(n):
        c1 = cities[tour[i]]
        c2 = cities[tour[(i + 1) % n]]  # quay lại thành phố đầu
        total += distance(c1, c2)
    return total

# Khởi tạo quần thể: danh sách các hoán vị
def init_population(pop_size, num_cities):
    population = []
    base = list(range(num_cities))
    for _ in range(pop_size):
        individual = base[:]
        random.shuffle(individual)
        population.append(individual)
    return population

# Chọn lọc Tournament
def tournament_selection(population, cities, k=3):
    # chọn ngẫu nhiên k cá thể rồi lấy cá thể tốt nhất (tour ngắn nhất)
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: tour_length(ind, cities))
    return selected[0][:]  # copy


# OX Crossover (Order Crossover)
def ox_crossover(parent1, parent2):
    size = len(parent1)
    child = [None] * size

    # chọn đoạn [start, end]
    start, end = sorted(random.sample(range(size), 2))

    # copy đoạn từ parent1
    for i in range(start, end + 1):
        child[i] = parent1[i]

    # điền các gene còn lại theo thứ tự xuất hiện trong parent2
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            # tìm thành phố trong parent2 chưa xuất hiện trong child
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]

    return child

# Đột biến: hoán đổi vị trí 2 thành phố
def swap_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]

def ga_tsp(
    cities,
    pop_size=100,
    generations=500,
    crossover_rate=0.9,
    mutation_rate=0.1,
    tournament_k=3
):
    num_cities = len(cities)
    population = init_population(pop_size, num_cities)

    best_individual = None
    best_fitness = float("inf")

    for gen in range(generations):
        new_population = []

        # đánh giá quần thể hiện tại, cập nhật best
        for ind in population:
            length = tour_length(ind, cities)
            if length < best_fitness:
                best_fitness = length
                best_individual = ind[:]

        # in thông tin sau mỗi 50 thế hệ
        if (gen + 1) % 50 == 0 or gen == 0:
            print(f"Generation {gen+1:4d} - Best tour length: {best_fitness:.4f}")

        # tạo thế hệ mới
        while len(new_population) < pop_size:
            # chọn bố mẹ bằng tournament
            parent1 = tournament_selection(population, cities, k=tournament_k)
            parent2 = tournament_selection(population, cities, k=tournament_k)

            # crossover
            if random.random() < crossover_rate:
                child1 = ox_crossover(parent1, parent2)
                child2 = ox_crossover(parent2, parent1)
            else:
                child1, child2 = parent1[:], parent2[:]

            # mutation
            swap_mutation(child1, mutation_rate)
            swap_mutation(child2, mutation_rate)

            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population

    # sau cùng, đánh giá lại best (phòng trường hợp chưa cập nhật)
    for ind in population:
        length = tour_length(ind, cities)
        if length < best_fitness:
            best_fitness = length
            best_individual = ind[:]

    return best_individual, best_fitness

if __name__ == "__main__":
    # tạo 20 thành phố ngẫu nhiên
    cities = generate_cities(20, seed=2024)

    best_tour, best_len = ga_tsp(
        cities,
        pop_size=100,
        generations=500,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_k=3
    )

    print("\nBest tour found:")
    print(best_tour)
    print(f"Best tour length: {best_len:.4f}")
