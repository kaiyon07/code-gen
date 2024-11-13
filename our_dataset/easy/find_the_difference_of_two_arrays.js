/**
 * @param {number[]} nums1
 * @param {number[]} nums2
 * @return {number[][]}
 */
var findDifference = function(nums1, nums2) {
    let set1 = new Set(nums1);
    let set2 = new Set(nums2);
    let uniqueToNums1 = Array.from(set1).filter(x => !set2.has(x));
    let uniqueToNums2 = Array.from(set2).filter(x => !set1.has(x));

    return [uniqueToNums1, uniqueToNums2];
};