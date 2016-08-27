import heapq

nums = [1, 5, 2, 6, 0, 3, 9]
print(nums)
heapq.heapify(nums)
print(nums)
heap = list(nums)
print(type(nums))
print(type(heap))

heapq.heapify(heap)
print(heap)
