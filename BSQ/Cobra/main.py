from utils import parser


def find_largest_square(bsq_map: list[list[str]], height: int, width: int) -> tuple[int, int, int]:
    dp = [[0] * (width + 1) for _ in range(height + 1)]
    max_size = 0
    max_i = max_j = 0

    for i in range(1, height + 1):
        for j in range(1, width + 1):
            if bsq_map[i-1][j-1] == '.':
                dp[i][j] = min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1]) + 1
                if dp[i][j] > max_size:
                    max_size = dp[i][j]
                    max_i, max_j = i, j

    return max_size, max_i, max_j


def mark_largest_square(bsq_map: list[list[str]], size: int, max_i: int, max_j: int) -> None:
    for i in range(max_i - size, max_i):
        for j in range(max_j - size, max_j):
            bsq_map[i][j] = 'x'


def print_bsq_map(bsq_map: list[list[str]]) -> None:
    for row in bsq_map:
        print(''.join(row))


def check_bsq_map(bsq_map: list[list[str]]) -> bool:
    if not bsq_map:
        return False

    width = len(bsq_map[0])
    for row in bsq_map:
        if len(row) != width or any(cell not in {'o', '.'} for cell in row):
            return False

    return True


def main() -> None:
    height, width, bsq_map = parser()
    if not check_bsq_map(bsq_map):
        print('Map is invalid!')
        return
    mark_largest_square(bsq_map, *find_largest_square(bsq_map, height, width))
    print_bsq_map(bsq_map)


if __name__ == '__main__':
    main()
