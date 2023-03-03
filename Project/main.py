import math

import pygame
import random

pygame.init()


class INFO:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    RED = 25, 229, 49
    RED2 = 255, 0, 0
    GREEN = 235, 255, 0
    BACKGROUND_COLOR = (255, 254, 255)
    PaddingX = 0
    PaddingY = 50
    GRADIENTS = [
        (235, 80, 140),
        (181, 42, 77),
        (124, 67, 90),
        (59, 42, 63)
    ]
    FONT = pygame.font.SysFont('Verdana', 11)
    FONT2 = pygame.font.SysFont('Verdana', 11)
    FONT3 = pygame.font.SysFont('Verdana', 11)

    def __init__(self, width, height, numbers):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Algorithms Visualizer")
        self.set_list(numbers)

    # defining the environment
    def set_list(self, numbers):
        self.numbers = numbers
        self.minVal = min(numbers)
        self.maxVal = max(numbers)
        self.blockWidth = round((self.width - self.PaddingX) / len(numbers))
        self.blockHeight = ((self.height - self.PaddingY) // (self.maxVal - self.minVal))
        self.startX = self.PaddingX // 2

    def GenerateRandomList(self, n, mx, mn):
        tmp_list = []
        for _ in range(n):
            value = random.randint(mn, mx)
            tmp_list.append(value)
        return tmp_list

    def Draw(self, drawInfo, algoName, asc, number):
        drawInfo.window.fill(drawInfo.BACKGROUND_COLOR)

        title = drawInfo.FONT3.render(
            f"{algoName} - {'Ascending' if asc else 'Descending'}  | Number of elements : {number} ",
            1, drawInfo.RED2)
        drawInfo.window.blit(title, (drawInfo.width / 2 - title.get_width() / 2, 4))

        controls = drawInfo.FONT.render(
            "R - Reset | Space - Start | A - change sort mode |  DOWN - Speed Up  |  UP - Speed Down | 0 - remove elements | 1 - Add elements",
            1, drawInfo.BLACK)
        drawInfo.window.blit(controls, (drawInfo.width / 2 - controls.get_width() / 2, 36))
        controls = drawInfo.FONT.render(
            "I - Insertion Sort | B - Bubble Sort | S - Selection Sort | O - Odd Even Sort | H - Heap Sort | C - cocktail Sort",
            1, drawInfo.BLACK)
        drawInfo.window.blit(controls, (drawInfo.width / 2 - controls.get_width() / 2, 68))

        self.drawList(drawInfo)
        pygame.display.update()

    def drawList(self, drawInfo, colorpos=None, clearBg=False):
        if colorpos is None:
            colorpos = {}
        nums = drawInfo.numbers
        if clearBg:
            clear_rect = (drawInfo.PaddingX // 2, drawInfo.PaddingY, drawInfo.width - drawInfo.PaddingX,
                          drawInfo.height)
            pygame.draw.rect(drawInfo.window, drawInfo.BACKGROUND_COLOR, clear_rect)
        for i, val in enumerate(nums):
            x = drawInfo.startX + i * drawInfo.blockWidth
            y = drawInfo.height - (val - drawInfo.minVal) * drawInfo.blockHeight
            color = drawInfo.GRADIENTS[i % 4]
            if i in colorpos:
                color = colorpos[i]
            pygame.draw.rect(drawInfo.window, color, (x, y, drawInfo.blockWidth, drawInfo.height))
        if clearBg:
            pygame.display.update()

    def bubbleSort(self, drawInfo, asc=True):
        nums = drawInfo.numbers
        for i in range(len(nums) - 1):
            for j in range(len(nums) - 1 - i):
                num1 = nums[j]
                num2 = nums[j + 1]
                if (num1 > num2 and asc) or (num1 < num2 and not asc):
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    self.drawList(drawInfo, {j: drawInfo.GREEN, j + 1: drawInfo.RED}, True)
                    yield True
        return nums

    def insertionSort(self, drawInfo, asc=True):
        nums = drawInfo.numbers
        for i in range(1, len(nums)):
            now = nums[i]
            while True:
                ascSort = i > 0 and nums[i - 1] > now and asc
                decSort = i > 0 and nums[i - 1] < now and not asc

                if not ascSort and not decSort:
                    break
                nums[i] = nums[i - 1]
                i -= 1
                nums[i] = now
                self.drawList(drawInfo, {i: drawInfo.GREEN, i - 1: drawInfo.RED}, True)
                yield True
        return nums

    def SelectionSort(self, drawInfo, asc=True):
        A = drawInfo.numbers
        for i in range(len(A)):
            min_idx = i
            for j in range(i + 1, len(A)):
                if A[min_idx] > A[j] and asc:
                    min_idx = j
                elif A[min_idx] < A[j] and not asc:
                    min_idx = j
                self.drawList(drawInfo, {i: drawInfo.GREEN, j: drawInfo.RED}, True)
                yield True
            A[i], A[min_idx] = A[min_idx], A[i]
            self.drawList(drawInfo, {i: drawInfo.GREEN, min_idx: drawInfo.RED}, True)
            yield True
        return A

    def odd_even_sort(self, drawInfo, asc=True):
        nums = drawInfo.numbers
        isSorted = 0
        while isSorted == 0:
            isSorted = 1
            for i in range(1, len(nums) - 1, 2):
                if nums[i] > nums[i + 1] and asc:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    self.drawList(drawInfo, {i: drawInfo.GREEN, i + 1: drawInfo.RED}, True)
                    yield True
                    isSorted = 0
                elif nums[i] < nums[i + 1] and not asc:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    self.drawList(drawInfo, {i: drawInfo.GREEN, i + 1: drawInfo.RED}, True)
                    yield True
                    isSorted = 0
            for i in range(0, len(nums) - 1, 2):
                if nums[i] > nums[i + 1] and asc:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    self.drawList(drawInfo, {i: drawInfo.GREEN, i + 1: drawInfo.RED}, True)
                    yield True
                    isSorted = 0
                if nums[i] < nums[i + 1] and not asc:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    self.drawList(drawInfo, {i: drawInfo.GREEN, i + 1: drawInfo.RED}, True)
                    yield True
                    isSorted = 0

        return nums

    def heapify(self, arr, N, i, drawInfo, asc=True):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < N and arr[largest] < arr[l] and asc:
            largest = l
        if l < N and arr[largest] > arr[l] and not asc:
            largest = l
        if r < N and arr[largest] < arr[r] and asc:
            largest = r
        if r < N and arr[largest] > arr[r] and not asc:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.drawList(drawInfo, {i: drawInfo.GREEN, largest: drawInfo.RED}, True)
            yield True
            yield from (self.heapify(arr, N, largest, drawInfo, asc))
            yield True

    def heapSort(self, drawInfo, asc=True):
        N = len(drawInfo.numbers)
        arr = drawInfo.numbers
        for i in range(N // 2 - 1, -1, -1):
            yield True
            yield from self.heapify(arr, N, i, drawInfo, asc)
            yield True
        for i in range(N - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.drawList(drawInfo, {i: drawInfo.GREEN, 0: drawInfo.RED}, True)
            yield True
            yield from self.heapify(arr, i, 0, drawInfo, asc)
            yield True
        return arr

    def cocktailSort(self, drawInfo, asc=True):
        n = len(drawInfo.numbers)
        a = drawInfo.numbers
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if a[i] > a[i + 1] and asc or (a[i] < a[i + 1] and not asc):
                    a[i], a[i + 1] = a[i + 1], a[i]
                    self.drawList(drawInfo, {i: drawInfo.GREEN, i + 1: drawInfo.RED}, True)
                    yield True
                    swapped = True

            if not swapped:
                break
            swapped = False
            end = end - 1
            for i in range(end - 1, start - 1, -1):
                if a[i] > a[i + 1] and asc or (a[i] < a[i + 1] and not asc):
                    a[i], a[i + 1] = a[i + 1], a[i]
                    self.drawList(drawInfo, {i: drawInfo.GREEN, i + 1: drawInfo.RED}, True)
                    yield True
                    swapped = True
            start = start + 1

    # showing the Screen
    def main(self):
        working = True
        clock = pygame.time.Clock()
        n = 100
        mxV = 600
        mnV = 2
        nums = self.GenerateRandomList(n, mxV, mnV)
        drawInfo = INFO(1280, 700, nums)
        sorting = False
        asc = True
        sorting_now = self.bubbleSort
        sorting_name = "Bubble Sort"
        sorting_gen = None
        speed = 60
        while working:
            clock.tick(speed)
            if sorting:
                try:
                    next(sorting_gen)
                except StopIteration:
                    sorting = False
            else:
                self.Draw(drawInfo, sorting_name, asc, n)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_r:
                    nums = self.GenerateRandomList(n, mxV, mnV)
                    drawInfo.set_list(nums)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_gen = sorting_now(drawInfo, asc)
                elif event.key == pygame.K_a and not sorting:
                    asc ^= 1
                elif event.key == pygame.K_UP:
                    speed = min(speed + 10, 600)
                elif event.key == pygame.K_DOWN:
                    speed = max(speed - 10, 1)
                elif event.key == pygame.K_i:
                    sorting_now = self.insertionSort
                    sorting_name = "Insertion Sort"
                elif event.key == pygame.K_b:
                    sorting_now = self.bubbleSort
                    sorting_name = "Bubble Sort"
                elif event.key == pygame.K_1:
                    n = min(n + 10, 660)
                    nums = self.GenerateRandomList(n, mxV, mnV)
                    drawInfo.set_list(nums)
                    sorting = False
                elif event.key == pygame.K_0:
                    n = max(n - 10, 5)
                    nums = self.GenerateRandomList(n, mxV, mnV)
                    drawInfo.set_list(nums)
                    sorting = False
                elif event.key == pygame.K_s:
                    sorting_now = self.SelectionSort
                    sorting_name = "Selection Sort"
                elif event.key == pygame.K_o:
                    sorting_now = self.odd_even_sort
                    sorting_name = "Odd Even Sort"
                elif event.key == pygame.K_h:
                    sorting_now = self.heapSort
                    sorting_name = "Heap Sort"
                elif event.key == pygame.K_c:
                    sorting_now = self.cocktailSort
                    sorting_name = "cocktail Sort"
        pygame.quit()


lst = [random.randint(100000, 100000), random.randint(-45, 100)]

tmp = INFO(1000, 600, lst)
if __name__ == "__main__":
    tmp.main()
