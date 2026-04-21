using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace LeetCodeProblems.LeetcodeProblems
{
    public class Utilities
    {
        public static void Heapify(int[] arr, int n, int i)
        {
            int largest = i;
            int l = 2 * i + 1;
            int r = 2 * i + 2;

            if (l < n && arr[l] > arr[largest])
            {
                largest = l;
            }

            if (r < n && arr[r] > arr[largest])
            {
                largest = r;
            }

            if (largest != i)
            {
                int swap = arr[i];
                arr[i] = arr[largest];
                arr[largest] = swap;

                Heapify(arr, n, largest);
            }
        }

        public static void HeapSortArr(int[] arr)
        {
            int n = arr.Length;

            for (int i = n / 2 - 1; i >= 0; i--)
            {
                Heapify(arr, n, i);
            }

            for (int i = n - 1; i >= 0; i--)
            {
                int temp = arr[0];
                arr[0] = arr[i];
                arr[i] = temp;

                Heapify(arr, i, 0);
            }
        }

        public static void BuildHeap(int[] arr, int n)
        {
            int startIndx = (n / 2) - 1;
            for (int i = startIndx; i >= 0; i--)
            {
                Heapify(arr, n, i);
            }
        }

        public class Deque
        {
            private int[] data;
            private int front, rear, size, capacity;

            public Deque(int capacity)
            {
                this.capacity = capacity;
                data = new int[capacity];
                front = -1;
                rear = -1;
                size = 0;
            }

            public bool IsFull()
            {
                return size == capacity;
            }

            public bool IsEmpty()
            {
                return size == 0;
            }

            public void InsertFront(int value)
            {
                if(IsFull())
                {
                    Console.WriteLine("DQ is Full!");
                    return;
                }
                if(front == -1)
                {
                    front = rear = 0;
                }
                else if (front == 0)
                {
                    front = capacity - 1;
                }
                else
                {
                    front--;
                }
                data[front] = value;
                size++;
            }

            public void InsertRear(int value)
            {
                if (IsFull())
                {
                    Console.WriteLine("DQ is Full!");
                    return;
                }
                if (rear == -1)
                {
                    front = rear = 0;
                }
                else if (rear == capacity - 1)
                {
                    rear = 0;
                }
                else
                {
                    rear++;
                }
                data[rear] = value;
                size++;
            }

            public int DeleteFront()
            {
                if (IsEmpty())
                {
                    Console.WriteLine("DQ is Full!");
                    return - 1;
                }
                int value = data[front];
                if(front == rear)
                {
                    front = rear = -1;
                }
                else if (front == capacity - 1)
                {
                    front = 0;
                }
                else
                {
                    front++;
                }
                size--;
                return value;
            }

            public int DeleteRear()
            {
                if (IsEmpty())
                {
                    Console.WriteLine("DQ is Full!");
                    return -1;
                }
                int value = data[rear];
                if (front == rear)
                {
                    front = rear = -1;
                }
                else if (rear == 0)
                {
                    rear = capacity - 1;
                }
                else
                {
                    rear--;
                }
                size--;
                return value;
            }

            public int GetRear()
            {
                if(IsEmpty())
                {
                    Console.WriteLine("DQ is Empty");
                    return -1;
                }
                return data[rear];
            }

            public int GetFront()
            {
                if (IsEmpty())
                {
                    Console.WriteLine("DQ is Empty");
                    return -1;
                }
                return data[front];
            }

            public void DisplayDQ()
            {
                if(IsEmpty())
                {
                    Console.WriteLine("DQ is empty");
                    return;
                }
                Console.WriteLine("DQ Elemets: ");
                int i = front;
                while(true)
                {
                    Console.WriteLine(data[i] + " ");
                    if (i == rear) break;
                    i = (i + 1) % capacity;
                }
                Console.WriteLine();
            }
        }
    }
}
