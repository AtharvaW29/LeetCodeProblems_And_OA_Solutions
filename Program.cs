using LeetCodeProblems.LeetcodeProblems;
using System;

namespace LeetCodeProblems
{
    class Program
    {
        public static async Task Main(string[] args)
        {
            var arrproblems = new ArrayProblems();
            // Test TwoSum
            int[] nums = { -2, -1, 4, 2, 1 };
            int target = 9;
            int[] result = arrproblems.TwoSum(nums, target);
            Console.WriteLine($"TwoSum Result: [{string.Join(", ", result)}]");

            // Test ThreeSum
            //int[] threeSumInput = {-12, 12, -5, -4, -12, 11, 9, -11, 13, 1, 12, -1, 8, 1, -9, -11, -13, -4, 10, -9, -6, -11, 1, -15, -3, 4, 0, -15, 3, 6, -4, 7, 3, -2, 10, -2, -6, 4, 2, -7, 12, -1, 7, 6, 7, 6, 2, 10, -13, -3, 8, -12, 2, -5, -12, 6, 6, -5, 6, -5, -14, 9, 9, -4, -8, 4, 2, -7, -15, -11, -7, 12, -4, 8, -5, -12, -1, 12, 5, 1, -5, -1, 5, 12, 9, 0, 3, 0, 3, -14, 2, -4, 2, -4, 0, 1, 7, -13, 9, -1, 13, -12, -11, -6, 11, -1, -10, -5, -3, 10, 3, 7, -6, -15, -4, 10, 1, 14, -12};
            //var triplets = arrproblems.ThreeSum(threeSumInput);

            // Test Profit & Loss
            int[] prices = { 1, 2 };
            var profit = arrproblems.MaxProfit(prices);

            // Duplicates
            int[] nms = { 1, 2, 3, 4 };
            var dup = arrproblems.ContainsDuplicate(nms);

            var peself = arrproblems.ProductExcept(nms);

            var sln = arrproblems.solution(nms);

            // Max Sub Array Problem
            int maxsubarr = arrproblems.MaxSubArray(nums);
            // Linked List Problems
            LinkedListProblems.ListNode l1 = new LinkedListProblems.ListNode(9);
            l1.next = new LinkedListProblems.ListNode(9);
            l1.next.next = new LinkedListProblems.ListNode(9);
            l1.next.next.next = new LinkedListProblems.ListNode(9);

            LinkedListProblems.ListNode l2 = new LinkedListProblems.ListNode(9);
            l2.next = new LinkedListProblems.ListNode(9);
            l2.next.next = new LinkedListProblems.ListNode(9);

            LinkedListProblems.ListNode resultList = LinkedListProblems.AddTwoNums(l1, l2);

            Console.WriteLine("Result List: ");
            LinkedListProblems.ListNode current = resultList;
            while (current != null)
            {
                Console.Write(current.val + " -> ");
                current = current.next;
            }
            Console.WriteLine("null");

            Console.WriteLine("Enter the Google Docs URL:");
            string googleDocUrl = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(googleDocUrl))
            {
                Console.WriteLine("No URL provided. Exiting.");
                return;
            }
            await PatternMatching.PrintGridFromGoogleDoc(googleDocUrl);
        }
    }
}