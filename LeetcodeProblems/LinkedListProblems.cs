using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace LeetCodeProblems.LeetcodeProblems
{
    public class LinkedListProblems
    {
        // Utilities
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
        public class ListNode
        {
            public int val;
            public ListNode next;
            public ListNode(int val = 0, ListNode next = null)
            {
                this.val = val;
                this.next = next;
            }
        }

        public static ListNode AddTwoNums(ListNode l1, ListNode l2)
        {
            if (l1 == null && l2 == null)
            {
                return null;
            }
            if (l1 == null)
            {
                return l2;
            }
            if (l2 == null)
            {
                return l1;
            }

            ListNode dummyHead = new ListNode();
            ListNode currentRes = dummyHead;
            int carry = 0;

            while (l1 != null || l2 != null || carry != 0)
            {
                int val1 = (l1 != null) ? l1.val : 0;
                int val2 = (l2 != null) ? l2.val : 0;

                int sum = 0;
                sum = val1 + val2 + carry;
                carry = sum / 10;

                currentRes.next = new ListNode(sum % 10);
                currentRes = currentRes.next;

                if (l1 != null)
                {
                    l1 = l1.next;
                }
                if (l2 != null)
                {
                    l2 = l2.next;
                }
            }

            return dummyHead.next;
        }

        public static ListNode MergeKLists(ListNode[] lists)
        {
            if (lists == null) return null;
            else
            {
                ListNode sortedlist = new ListNode();
                ListNode crrList = sortedlist;
                List<int> arr = new List<int>();
                // 1. Copy the data of the given lists into an array step by step
                foreach (ListNode head in lists)
                {
                    ListNode crr = head;
                    while(crr!= null)
                    {
                        arr.Add(crr.val);
                        crr = crr.next;
                    }
                }
                // 2. Sort the array by using Heap Sort
                int[] sortarr = arr.ToArray();
                HeapSortArr(sortarr);
                foreach(int i in sortarr)
                {
                    Console.WriteLine(i);
                }
                // 3. Build a new list with the sorted array and return it
                foreach (int i in sortarr)
                {
                    crrList.next = new ListNode(i);
                    crrList = crrList.next;
                }
                return sortedlist;
            }
        }
    }
}
